import os
import boto3
from botocore.exceptions import ClientError
from rich import print

client = boto3.client('s3')

def list_buckets() :
    try:
        response = client.list_buckets()
        for bucket in response['Buckets']:
            name = bucket['Name']
            print("Names of the buckets are: ",name)
    except ClientError as error:
        print(error.response)


def bulk_operation_s3():
    try:
        print("Current Working Directory is : ",os.getcwd())

        print("Buckets available to upload are: ")
        list_buckets()

        print("Enter the name of the bucket to upload to:")
        destination_bucket = input()

        root, dirs, files = next(os.walk(os.getcwd()))
        total_number_of_files = len(files)

        current_file = 0
        for f in files:
            current_file += 1
            print(f)
            local_path = os.path.join(root,f)
            uploaded_file_name = os.path.basename(local_path)

            try:
                client.upload_file(local_path, destination_bucket, uploaded_file_name)
                print(f"Currently uploading  {current_file} of {total_number_of_files}")

            except ClientError as e:
                print(e.response['Error']['Message'])

        print("Files have been successfully uploaded to the destination bucket")

    except ClientError as error:
        print(error.response)

list_buckets()
bulk_operation_s3()

