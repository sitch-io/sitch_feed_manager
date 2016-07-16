# Sitch feed manager

## Retrieves OpenCellID DB and parses out into MCC-specific files.  Publishes feed files on AWS S3.

### Required environment variables:
```shell
AWS_KEY        # Amazon AWS key.  Needs privs for S3
AWS_SECRET     # Amazon AWS key secret
OCID_KEY       # API key for OpenCellID DB
BUCKET_NAME    # S3 Bucket name for feed files
BASE_PATH      # Local path for storing parsed files, before uploading to S3.  Don't pick a ramdisk.
TWILIO_SID     # API Key
TWILIO_TOKEN   # API Token
ISO_COUNTRY    # Used for getting carrier info from Twilio
```

### Recommended operation:

* Create creds for AWS.
* Obtain API key from OpenCellID.org (http://opencellid.org)
* Build the Docker container: `docker build -t feedmanager .`
* Run the container like this:
```shell
docker run -it --rm -e AWS_KEY=$AWS_KEY \
-e AWS_SECRET="$AWS_SECRET_KEY" \
-e BUCKET_NAME=MyBucketName \
-e OCID_KEY=$OPEN_CELL_ID_KEY \
-e BASE_PATH=/opt/basepath \
-e TWILIO_SID=$TWILIO_SID \
-e TWILIO_TOKEN=$TWILIO_TOKEN \
-e ISO_COUNTRY=$ISO_COUNTRY
feedmanager
```
