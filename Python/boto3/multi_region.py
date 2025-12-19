import boto3

client = boto3.client('ec2')

response = client.describe_regions()

regions = []
for Regions in response['Regions']:
    regions.append(Regions['RegionName'])
print(regions)



print("Enter number of regions to be checked: ")
num = input()

print("Enter regions to be checked:")

final_regions_check = []

for i in range(0,int(num)):
    i = input()
    region_to_check = i.strip()
    while region_to_check == "":
        print("Empty region given, please input again")
        i = input()
        region_to_check = i.strip()

    if region_to_check in regions:
        final_regions_check.append(region_to_check)
    else:
        print("Invalid region entered.Skipping the check",region_to_check)

def multi_region():
    for region in final_regions_check:
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