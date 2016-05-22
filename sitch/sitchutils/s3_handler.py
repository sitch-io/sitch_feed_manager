import boto3
import botocore


class S3Handler(object):
    def __init__(self, config):
        self.aws_session = boto3.Session(aws_access_key_id=config.aws_key,
                                         aws_secret_access_key=config.aws_secret)
        self.s3 = self.aws_session.client('s3')
        self.bucket_name = config.bucket_name
        if not self.bucket_exists():
            self.s3.create_bucket(ACL='public-read', Bucket=self.bucket_name)

    def bucket_exists(self):
        exists = True
        try:
            self.s3.head_bucket(Bucket=self.bucket_name)
        except botocore.exceptions.ClientError as e:
            # If a client error is thrown, then check that it was a 404 error.
            # If it was a 404 error, then the bucket does not exist.
            error_code = int(e.response['Error']['Code'])
            if error_code == 404:
                exists = False
        return exists

    def write_file_to_s3(self, basepath, filepath):
        s3_path_name = filepath.replace(basepath, "")
        self.s3.upload_file(filepath, self.bucket_name, s3_path_name,
                            {'ACL': 'public-read',
                             'ContentType': 'application/gzip'})
