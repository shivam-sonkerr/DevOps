import boto3
import logging


logging.basicConfig(level=logging.INFO,format='%(asctime)s %(levelname)s: %(message)s')


s3_client = boto3.client('s3')
s3 = boto3.resource('s3')

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




