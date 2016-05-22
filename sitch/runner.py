import sitchutils


def main():
    config = sitchutils.ConfigHelper()
    feed = sitchutils.FeedManager(config)
    fileout = sitchutils.OutfileHandler(config.base_path)
    print "Getting feed from OpenCellID"
    feed.write_feed_file(config)
    ocid_feed = sitchutils.OpenCellIdDataset(config.ocid_destination_file)
    s3 = sitchutils.S3Handler(config)
    detected_mccs = []
    out_file_list = []
    print "Parsing feed into MCC files.  This may take a while."
    for row in ocid_feed:
        radio = row["radio"]
        if radio != config.target_radio:
            continue
        mcc = row["mcc"]
        if row["mcc"] in detected_mccs:
            _file_name = fileout.append_mcc_file(radio, mcc, [row])
        else:
            file_name = fileout.start_mcc_file(radio, mcc, [row])
            detected_mccs.append(mcc)
            out_file_list.append(file_name)
    for outfile in out_file_list:
        print "Uploading cells to S3"
        s3.write_file_to_s3(config.base_path, outfile)

if __name__ == "__main__":
    main()
