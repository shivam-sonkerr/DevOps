import boto3
from collections import Counter
client = boto3.client('ec2',region_name = 'us-east-1')




def instance_summary():
    response = client.describe_instances()

    total_num_instances = 0
    state_counter = {}
    instance_type_counter = {}

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            total_num_instances = total_num_instances + 1

            instance_state = instance['State']['Name']

            instance_id = instance['InstanceId']


            state_counter[instance['State']['Name']] = state_counter.get(instance['State']['Name'],0) +1
            instance_type_counter[instance['InstanceType']] = instance_type_counter.get(instance['InstanceType'],0)+1

    print("-----------Instance Summary-----------")
    print("By State","\n",state_counter)
    print("By instance type","\n",instance_type_counter)
    print("Total number of instances are: ",total_num_instances,"\n")


instance_summary()