import boto3
from botocore.exceptions import ClientError
from rich import print



client = boto3.client('s3')

print(f"Region: {client.meta.region_name}")

print(f"Endpoint: {client.meta.endpoint_url}")

def create_bucket():
    try:
        response = client.create_bucket(
        Bucket = 'boto11321',
            CreateBucketConfiguration = {
                'LocationConstraint':'us-west-2'
                # 'Location': {
                #     'Name':'us-west-2'
                # }
            }
    )
    except ClientError as error:
        print (error.response['Error']['Code'])
        print(error.response['Error']['Message'])
        print(error.response['ResponseMetadata']['HTTPStatusCode'])

def list_buckets():
    try:
        response = client.list_buckets()
        for bucket in response['Buckets']:
            name = bucket['Name']
            print("Name of the bucket are :",name)
    except ClientError as error:
        print(error.response['Error']['Code'])
        print(error.response['Error']['Message'])
        print(error.response['ResponseMetadata']['HTTPStatusCode'])


def list_objects():

    print("Enter bucket name: ")
    bucket_name = input()

    try:
        response = client.list_objects(
            Bucket = bucket_name
        )

        for content in response['Contents']:
            file_name = content['Key']
            file_size = content ['Size']
            print("File name: ", file_name)
            print("File Size", file_size)

    except ClientError as error:
        print(error.response['Error']['Code'])
        print(error.response['Error']['Message'])

def download_file():
    print("Enter bucket name: ")
    bucket_name = input()

    try:
        response = client.list_objects(
            Bucket = bucket_name
        )

        for content in response['Contents']:
            file_name = content['Key']
            print(file_name)

        print("Select which file to download")
        file_to_download = input()

        # client.download_file(bucket_name,file_to_download,'/Users/shivam/'+file_to_download)
        #
        # print("File has been downloaded, please check at the path.")
    except ClientError as error:
        print(error.response)



def get_object():

    print("Enter bucket name: ")
    bucket_name = input()

    try:
        response = client.list_objects(
            Bucket = bucket_name
        )



        for content in response['Contents']:
            file_name = content['Key']
            print(file_name)

        print("Select which file to download")
        file_to_download = input()


        response = client.get_object(
            Bucket = bucket_name,
            Key = file_to_download
        )

        print(response['Body'].read())
    except ClientError as error:
        print(error.response)


create_bucket()
list_buckets()
list_objects()
download_file()
get_object()