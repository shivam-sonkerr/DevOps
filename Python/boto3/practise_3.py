import boto3


client = boto3.client('ec2',region_name = 'us-east-1')


def batch_operation ():
    response = client.describe_instances()

    batch_instances = []

    # print("Number of instances to be stopped: ")
    # num = input()
    # print("Provide instance IDs: ")

    # for i in range(0,int(num)):
    #     i = input()
    #     batch_instances.append(i)

    current_running_list = []

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            current_status = instance['State']['Name']

            if current_status == 'running':
                current_running_list.append(instance['InstanceId'])


    print(current_running_list)
    response = client.stop_instances(
            InstanceIds = current_running_list
            )
    print("Instance has been stopped!")

batch_operation()