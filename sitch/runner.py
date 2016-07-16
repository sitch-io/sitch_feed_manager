import gzip
import sitchutils
import shutil


def main():
    config = sitchutils.ConfigHelper()
    feed = sitchutils.FeedManager(config)
    fileout = sitchutils.OutfileHandler(config.base_path)
    # Getting carrier reference from Twilio
    twilio_c = sitchutils.TwilioCarriers(config.twilio_sid,
                                         config.twilio_token)
    mcc_mnc_carriers = twilio_c.get_providers_for_country(config.iso_country)
    carrier_enricher = sitchutils.CarrierEnricher(mcc_mnc_carriers)
    # print "Getting feed from OpenCellID"
    feed.write_feed_file(config)
    ocid_feed = sitchutils.OpenCellIdDataset(config.ocid_destination_file)
    s3 = sitchutils.S3Handler(config)
    detected_mccs = []
    out_file_list = []
    files_to_ship = []
    print "Parsing feed into MCC files.  This may take a while."
    for row in ocid_feed:
        radio = row["radio"]
        # if radio != config.target_radio:
        #    continue
        mcc = row["mcc"]
        if row["mcc"] in detected_mccs:
            row["carrier"] = carrier_enricher.get_carrier(row["mcc"],
                                                          row["net"])
            _file_name = fileout.append_mcc_file(radio, mcc, [row])
        else:
            file_name = fileout.start_mcc_file(radio, mcc, [row])
            detected_mccs.append(mcc)
            out_file_list.append(file_name)
    for outfile in out_file_list:
        print "Gzipping file, prepping for publication"
        uncomp_file = outfile
        comp_file = str(uncomp_file + '.gz')
        with open(uncomp_file, 'rb') as in_file, gzip.open(comp_file,
                                                           'wb') as out_file:
            shutil.copyfileobj(in_file, out_file)
        print "Uploading %s to S3" % comp_file
        s3.write_file_to_s3(config.base_path, comp_file)

if __name__ == "__main__":
    main()
