import boto3


client = boto3.client('ec2',region_name = 'us-east-1')


def batch_operation ():
    response = client.describe_instances()

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
        while instance_id == "":
            print("Empty instances cannot be stopped, please provide proper instance ID")
            i = input()
            instance_id = i.strip()
        batch_instances.append(instance_id)

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


    print("Currently running instances are : ", current_running_list)

    final_list = []

    for l in batch_instances:
        for m in current_running_list:
            if l==m:
                final_list.append(m)

    if len(final_list) == 0:
        print("No valid instances are there to be stopped")
        return

    print("Final list of instances that will be stopped: ",final_list)

    print("Press y/n to continue further")

    decision = input()

    if decision in ('y','Y','yes'):
        response = client.stop_instances(
            InstanceIds= final_list
        )
        print("Instances have been stopped!")
    else:
        print("As you have selected no therefore none of the instances will be stopped")
        return

batch_operation()