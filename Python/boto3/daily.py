import boto3
from botocore.exceptions import ClientError
from rich import print

client = boto3.client('ec2')

def instance_details():
    try:
        response = client.describe_instances()
        print(response)
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instance_state = instance['Instances']['Name']
                print("State of the instance is: ", instance_state)
                instance_id = instance['InstanceId']
                instance_type = instance['InstanceType']

    except ClientError as error :
        print(error.response['Error']['Code'])
        print(error.response['Error']['Message'])

instance_details()