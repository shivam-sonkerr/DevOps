"""
LESSON 2: S3 Basics with Boto3
==============================

Learning Objectives:
- Create and manage S3 buckets
- Upload/download objects
- Set bucket policies and permissions
- Handle S3 errors and edge cases
"""

import boto3
from botocore.exceptions import ClientError
import os
from datetime import datetime

class S3Manager:
    def __init__(self, region='us-west-2'):
        self.region = region
        self.s3_client = boto3.client('s3', region_name=region)
        self.s3_resource = boto3.resource('s3', region_name=region)
    
    def list_buckets(self):
        """List all S3 buckets"""
        try:
            response = self.s3_client.list_buckets()
            print("\n🪣 S3 Buckets:")
            print("=" * 40)
            
            for bucket in response['Buckets']:
                print(f"📦 {bucket['Name']}")
                print(f"   Created: {bucket['CreationDate']}")
                print("-" * 30)
                
        except ClientError as e:
            print(f"❌ Error: {e}")
    
    def create_bucket(self, bucket_name):
        """Create a new S3 bucket"""
        try:
            if self.region == 'us-east-1':
                self.s3_client.create_bucket(Bucket=bucket_name)
            else:
                self.s3_client.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={'LocationConstraint': self.region}
                )
            print(f"✅ Bucket '{bucket_name}' created successfully")
            
        except ClientError as e:
            if e.response['Error']['Code'] == 'BucketAlreadyExists':
                print(f"❌ Bucket '{bucket_name}' already exists")
            else:
                print(f"❌ Error creating bucket: {e}")
    
    def upload_file(self, bucket_name, file_path, object_key=None):
        """Upload a file to S3 bucket"""
        if object_key is None:
            object_key = os.path.basename(file_path)
        
        try:
            self.s3_client.upload_file(file_path, bucket_name, object_key)
            print(f"✅ Uploaded {file_path} to {bucket_name}/{object_key}")
            
        except FileNotFoundError:
            print(f"❌ File {file_path} not found")
        except ClientError as e:
            print(f"❌ Error uploading: {e}")

# PRACTICE EXERCISES
def practice_exercises():
    print("\n🎯 S3 PRACTICE EXERCISES")
    print("=" * 30)
    
    s3_mgr = S3Manager()
    
    # Exercise 1: List existing buckets
    s3_mgr.list_buckets()
    
    # Exercise 2: Create a practice bucket
    bucket_name = f"my-practice-bucket-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    print(f"\n2. Creating practice bucket: {bucket_name}")
    s3_mgr.create_bucket(bucket_name)

if __name__ == "__main__":
    print("🚀 Starting Lesson 2: S3 Basics")
    practice_exercises()