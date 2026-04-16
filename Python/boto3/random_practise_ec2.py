import boto3
from botocore.exceptions import ClientError
from rich import print

client = boto3.client('ec2',region_name = 'us-east-1')


def count_state_instances():
    try:
        response = client.describe_instances()
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instance_state = (instance['State']['Name'])
                print(instance_state)
                count_dict = dict()

    except ClientError as error:
        print(error.response)

count_state_instances()

