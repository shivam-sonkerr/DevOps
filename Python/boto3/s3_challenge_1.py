import boto3
import logging
import uuid
import json


logging.basicConfig(level=logging.INFO,format='%(asctime)s %(levelname)s: %(message)s')

s3 = boto3.resource('s3')

random_uuid = uuid.uuid4()

print("How many unique buckets you want?")

number_bucket = int(input())

x = range(number_bucket)

regions = {"location1": 'us-west-1', "location2": 'us-west-2',"location3": 'us-east-1'}

s3_client = boto3.client('s3')





created_buckets = []

def create_bucket():
    for key in regions:
        region = regions[key]
        s3_client = boto3.client('s3', region_name=region)

        for num in x:
            bucket_name = f"{random_uuid}-{region}-{num}"
            print(bucket_name)
            created_buckets.append(bucket_name)

            policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": "*",
                        "Action": "s3:*",
                        "Resource": [
                            f"arn:aws:s3:::{bucket_name}",
                            f"arn:aws:s3:::{bucket_name}/*"
                        ],
                        "Condition": {
                            "StringNotEquals": {
                                "s3:x-amz-server-side-encryption": "AES256"
                            }
                        }
                    }
                ]
            }

            policy_string = json.dumps(policy)

            if region == 'us-east-1':
             s3_client.create_bucket(Bucket=bucket_name)

             response = s3_client.put_object(Bucket=bucket_name, Key='abcde123',ServerSideEncryption='AES256')
             s3_client.put_public_access_block(
                 Bucket=bucket_name,
                 PublicAccessBlockConfiguration={
                     'BlockPublicAcls': True,
                     'IgnorePublicAcls': True,
                     'BlockPublicPolicy': False,
                     'RestrictPublicBuckets': False
                 }
             )
             policy_bucket = s3_client.put_bucket_policy(Bucket=bucket_name,Policy=policy_string)
             # s3_client.put_bucket_versioning(Bucket=bucket_name,VersioningConfiguration ={'MFADelete':'Disabled','Status':'Enabled'})
            else:
                location = {'LocationConstraint':region}

                s3_client.create_bucket(Bucket=bucket_name,CreateBucketConfiguration=location)
                response = s3_client.put_object(Bucket=bucket_name, Key='abcde123',ServerSideEncryption='AES256')
                s3_client.put_public_access_block(
                    Bucket=bucket_name,
                    PublicAccessBlockConfiguration={
                        'BlockPublicAcls': True,
                        'IgnorePublicAcls': True,
                        'BlockPublicPolicy': False,
                        'RestrictPublicBuckets': False
                    }
                )
                policy_bucket = s3_client.put_bucket_policy(Bucket=bucket_name, Policy=policy_string)
                # s3_client.put_bucket_versioning(Bucket=bucket_name,VersioningConfiguration={'MFADelete': 'Disabled', 'Status': 'Enabled'})


create_bucket()


def copy_files():
    global source_key, destination_key
    s3_client = boto3.client('s3')

    bucket_names = []

    for buckets in s3.buckets.all():
        bucket_names.append(buckets.name)


    for i in range(len(created_buckets) - 1):

        source_bucket = created_buckets[i]
        destination_bucket = created_buckets[i + 1]
        print(f"Source Bucket is: {source_bucket}")
        print(f"Destination Bucket is: {destination_bucket}")
        print("---")

        response = s3_client.list_objects_v2(Bucket=source_bucket)
        if 'Contents' in response:
            for obj in response['Contents']:
                source_key = obj['Key']
                destination_key = f"copy-of-{source_key}"

                print(f"Object Key: {obj['Key']}")
                print(f"Size: {obj['Size'] / (1024 * 1024)} MB")



            s3_client.copy_object(Bucket=destination_bucket,
                              CopySource={'Bucket': source_bucket, 'Key': source_key}, Key=destination_key)
            encryption_response = s3_client.get_bucket_encryption(Bucket=source_bucket)
            print("Bucket Encryption status is: ",encryption_response)
            if "HTTPStatusCode" in encryption_response and "HTTPStatusCode"=='200':
                print("Bucket is encrypted")
            else:
                print("Bucket is not encrypted")
            print(f"  -> Copied to {destination_key}")





copy_files()





def delete_files():
##Printing objects and keeping it in response
    for buckets in s3.buckets.all():
        print("Name of the bucket is : ",buckets.name)

        response = s3_client.list_objects_v2(Bucket=buckets.name)

        print(response)

##Using response's Contents and then fetching the object key out of it
        if 'Contents' in response:
            for obj in response['Contents']:
                s3_client.delete_objects(Bucket=buckets.name, Delete ={'Objects':[{'Key':obj['Key']}]})
                print("File Deleted")
                print(f"Object Key: {obj['Key']}")
                print(f"Size: {obj['Size']/(1024*1024)} MB")
                print("Bucket Deleted")
            s3_client.delete_bucket(Bucket=buckets.name)
        else:
            s3_client.delete_bucket(Bucket=buckets.name)
            print("Bucket Deleted")
        print("All buckets and object deleted")




#delete_files()
