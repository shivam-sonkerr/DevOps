import boto3
from botocore.exceptions import ClientError
from rich import print

client = boto3.client('s3')

def list_buckets():
    try:
            response = client.list_buckets()
            for bucket in response['Buckets']:
                name = bucket['Name']
                print(name)
    except ClientError as error:
        print(error.response)

list_buckets()