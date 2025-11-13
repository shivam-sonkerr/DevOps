import boto3

client = boto3.client('ec2',region_name = 'us-east-1')

def instance_details():
    response = client.describe_instances()
    count = 0
    print("Enter state of the instance to be checked : ")
    state_to_check = input()

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            count = count +1
            if instance['State']['Name']== state_to_check.lower() :
                print("Instance number : ",count)
                print("Instance ID is: ",instance['InstanceId'])
                print("Instance Type is: ",instance['InstanceType'])
                print("State of the instance is: ",instance['State'].get('Name'))
                print("\n")


def stop_instance():
    response = client.describe_instances()

    print(" Provide Instance ID : ")
    instance_stop = input()
    if instance_stop == "":
        print("Empty value is given.")
        return


    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            if instance['InstanceId'] == instance_stop:
                current_status = instance['State']['Name'].lower()


                if current_status == "running":
                    response = client.stop_instances(
                    InstanceIds = [
                        instance_stop,
                    ])
                    print("Instance is stopped now!")
                return
    print("Instance not found")
    return







instance_details()

stop_instance()