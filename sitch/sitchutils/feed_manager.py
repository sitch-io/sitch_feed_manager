import requests


class FeedManager(object):
    def __init__(self, config):
        self.ocid_key = config.ocid_key
        self.feed_url = "http://opencellid.org/downloads/?apiKey=%s&filename=cell_towers.csv.gz" % self.ocid_key
        self.outfile = config.ocid_destination_file

    def write_feed_file(self, config):
        payload = {"key": self.ocid_key}
        response = requests.post(self.feed_url, data=payload, stream=True)
        with open(self.outfile, 'wb') as feed_file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    feed_file.write(chunk)
