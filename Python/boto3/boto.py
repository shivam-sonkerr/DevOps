import boto3
import logging
import uuid
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO,format='%(asctime)s %(levelname)s: %(message)s')

s3_client = boto3.client('s3')
s3 = boto3.resource('s3')

##Function to create bucket
def create_bucket(bucket_name,region="us-west-2"):

    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3',region_name = region)
            location = {'LocationConstraint':region}
            s3_client.create_bucket(Bucket=bucket_name,CreateBucketConfiguration=location)

    except ClientError as e:
        logging.error(e)
        return False
    return True

#Bucket name to be based on random uuid
random_uuid = uuid.uuid4()
create_bucket(str(random_uuid))


##File Upload
bucket_names = []
for bucket in s3.buckets.all():
    bucket_names.append(bucket)
    s3_client.upload_file('/Users/shivam/ubuntu-worker.yaml',bucket.name, 'worker.yaml')
    print("File upload successful")
    s3_client.download_file(bucket.name,'worker.yaml','/Users/shivam/worker.yaml')
    print('File Downloaded')
print("Buckets available are: ")
print(bucket_names)

