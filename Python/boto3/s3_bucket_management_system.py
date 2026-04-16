import boto3
from botocore.exceptions import ClientError
from rich import print

client = boto3.resource('ec2')

def list_buckets():
    try:
        response =  client.list_buckets
        for bucket in response['Buckets']:
            name = bucket['Name']
            print("Buckets available are: ",name)

    except ClientError as error:
        print(error.response['Error']['Message'])
        print(error.response['Error']['Code'])


list_buckets()