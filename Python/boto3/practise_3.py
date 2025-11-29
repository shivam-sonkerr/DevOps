import boto3


client = boto3.client('ec2',region_name = 'us-east-1')


def batch_operation ():
    response = client.describe_instances()

    batch_instances = []

    print("Number of instances to be stopped: ")
    num = input()
    print("Provide instance IDs: ")



    for i in range(0,int(num)):
        i = input()
        batch_instances.append(i)

    print(batch_instances)


    # for reservation in response['Reservations']:
    #     for instance in reservation['Instances']:
    #
    #         print(instance['State']['Name'])




batch_operation()