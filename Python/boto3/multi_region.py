import boto3

regions = ['us-east-1','us-east-2','us-west-1','us-west-2']

def multi_region():


    for region in regions:
        client = boto3.client('ec2', region_name=region)
        response = client.describe_instances()
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']
                instance_state = instance['State']['Name']
                print("Region: ",region)
                print(instance_id, "\n")
                print(instance_state)



multi_region()