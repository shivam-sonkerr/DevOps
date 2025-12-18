import boto3

client = boto3.client('ec2')

response = client.describe_regions()

regions = []
for Regions in response['Regions']:
    regions.append(Regions['RegionName'])
print(regions)

def multi_region():
    for region in regions:
        regional_client = boto3.client('ec2',region_name = region)
        response_for_instance = regional_client.describe_instances()
        for reservation in response_for_instance['Reservations']:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']
                instance_state = instance['State']['Name']
                print("Region: ",region)
                print(instance_id, "\n")
                print(instance_state)

multi_region()