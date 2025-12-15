import boto3
from botocore.exceptions import ClientError


client = boto3.client('ec2',region_name = 'us-east-1')


def batch_operation ():
    try:
        response = client.describe_instances()
    except ClientError as error:
        print(error.response['ResponseMetadata']['HTTPStatusCode'])
        print(error.response['Error']['Code'])
        print(error.response['Error']['Message'])
        return


    batch_instances = []

    print("Number of instances to be stopped: ")
    num = input()

    if num == '0':
        print("Invalid Input Zero, Exiting now!")
        return
    if not num.isnumeric() :
        print("Entered a wrong count input. Exiting Now!")
        return

    print("Provide instance IDs: ")

    for i in range(0,int(num)):
        i = input()
        instance_id = i.strip()
        while instance_id == "" or not instance_id.startswith("i-") :
            print("Empty instances or invalid instance ID given, please provide proper instance ID")
            i = input()
            instance_id = i.strip()
        batch_instances.append(instance_id)

    batch_instances = list(dict.fromkeys(batch_instances))

    if len(batch_instances) == 0:
        print("No instances were provided by the user.")
        return

    print("Instances user wants to stop: ", batch_instances)

    current_running_list = []

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            current_status = instance['State']['Name']

            if current_status == 'running':
                current_running_list.append(instance['InstanceId'])

            if current_status == 'stopped':
                print("This instance is already stopped")


    print("Currently running instances are : ", current_running_list)

    final_list = []

    for batch_instance in batch_instances:
        for running_instance in current_running_list:
            if batch_instance == running_instance:
                final_list.append(running_instance)
        if batch_instance not in current_running_list:
            print("This instance cannot be stopped as it is in different state than RUNNING",batch_instance)


    if len(final_list) == 0:
        print("No valid instances are there to be stopped")
        return

    print("Final list of instances that will be stopped: ",final_list)

    print("Press y/n to continue further")

    decision = input()

    if decision in ('y','Y','yes'):
        try:
            response = client.stop_instances(
                InstanceIds= final_list
            )
            if 'StoppingInstances' in response:
                for instance_status in response['StoppingInstances']:
                    instance_id = instance_status['InstanceId']
                    current_state = instance_status['CurrentState']['Name']
                    previous_state = instance_status['PreviousState']['Name']

                    print(f"Instance ID: {instance_id}")
                    print(f"  Previous State: {previous_state}")
                    print(f"  Current State: {current_state}")
                    print("-" * 20)



        except ClientError as error:
                print(error.response['Error']['Code'])
                print(error.response['ResponseMetadata']['HTTPStatusCode'])
                print(error.response['Error']['Message'])
    else:
        print("As you have selected no therefore none of the instances will be stopped")
        return






batch_operation()