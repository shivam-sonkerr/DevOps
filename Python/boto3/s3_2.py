import boto3
from botocore.exceptions import ClientError
from rich import print

client = boto3.client('s3')

print(f"Region: {client.meta.region_name}")

print(f"Endpoint: {client.meta.endpoint_url}")

def upload_file():
    try:
        print("Bucket available is :")
        response = client.list_buckets()

        for bucket in response['Buckets'] :
            bucket_name = bucket['Name']
            print(bucket_name)

        print("Enter the name of the bucket to upload to:")
        destination_bucket = input()

        print("Path of the file to upload in S3 bucket: ")
        file_to_upload = input()

        print("File to be saved with name: ")
        uploaded_file_name = input()

        client.upload_file(file_to_upload,destination_bucket,uploaded_file_name)
        print("File has been successfully uploaded to the destination bucket")
    except ClientError as error:
        print(error.response['Error']['Code'])
        print(error.response['Error']['Message'])

upload_file()