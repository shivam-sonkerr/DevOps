import boto3
from botocore.exceptions import ClientError
from rich import print
from rich.pretty import Pretty

client = boto3.client('ec2',region_name = 'us-east-1')

def learn():
    try:
        response = client.describe_instances(
            InstanceIds = ['i-fakefake']
        )
        print(response)
    except ClientError as error:
        print(Pretty(error.response))
        print(error.response['Error']['Code'])
        print(error.response['ResponseMetadata']['HTTPStatusCode'])
        print(error.response['Error']['Message'])


learn()