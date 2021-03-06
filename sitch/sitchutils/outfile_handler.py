import csv
import gzip
import os
import time


class OutfileHandler(object):
    def __init__(self, base_path):
        self.base_path = base_path
        self.ensure_path_exists(self.base_path)

    def start_mcc_file(self, radio, mcc, data):
        dir_name = os.path.join(self.base_path, radio, mcc)
        file_name = os.path.join(dir_name, "all.csv")
        # temp_file_name = os.path.join(dir_name, "all.csv.gz.temp")
        field_names = ["radio", "mcc", "net", "area", "cell", "unit", "lon",
                       "lat", "range", "samples", "changeable", "created",
                       "updated", "averageSignal", "carrier"]
        self.ensure_path_exists(dir_name)
        print "Starting a new file for MCC %s" % mcc
        with open(file_name, 'w') as outfile:
            producer = csv.DictWriter(outfile, fieldnames=field_names)
            producer.writeheader()
            for row in data:
                producer.writerow(row)
        # os.rename(temp_file_name, file_name)
        return file_name

    def append_mcc_file(self, radio, mcc, data):
        dir_name = os.path.join(self.base_path, radio, mcc)
        # file_name = os.path.join(dir_name, "all.csv.gz")
        file_name = os.path.join(dir_name, "all.csv")
        field_names = ["radio", "mcc", "net", "area", "cell", "unit", "lon",
                       "lat", "range", "samples", "changeable", "created",
                       "updated", "averageSignal", "carrier"]
        self.ensure_path_exists(dir_name)
        with open(file_name, 'a') as outfile:
            producer = csv.DictWriter(outfile, fieldnames=field_names)
            for row in data:
                try:
                    producer.writerow(row)
                except ValueError as e:
                    print "ValueError!"
                    print str(row)
        # os.rename(temp_file_name, file_name)
        return file_name

    @classmethod
    def ensure_path_exists(cls, dirpath):
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
            time.sleep(1)
