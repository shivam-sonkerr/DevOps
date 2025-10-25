import boto3
from pprint import pprint



def list_ec2_instances():
    ec2 = boto3.client('ec2')
    response = ec2.describe_instances()
    #print(response)
    #pprint(response)
    instances = []

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instances.append({
                'InstanceId' : instance['InstanceId'],
                'State': instance['State']['Name'],
                'InstanceType': instance['InstanceType']

            })

    return instances


pprint(list_ec2_instances())

