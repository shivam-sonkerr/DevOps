import boto3


s3 = boto3.resource('s3')


for bucket in s3.buckets.all():
    print(bucket.name)


ec2 = boto3.client('ec2')

print ("EC2 Details: ")
print ("\n")

response = ec2.describe_instances()
print(response)


res = ec2.describe_vpcs()
print ("\n")
print ("VPC Details: ")

print(res)
