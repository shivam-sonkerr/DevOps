"""
LESSON 1: EC2 Basics with Boto3
===============================

Learning Objectives:
- Understand EC2 client vs resource
- List and describe instances
- Handle AWS errors properly
- Format output for readability

Prerequisites:
- AWS CLI configured with credentials
- boto3 installed: pip install boto3
"""

import boto3
from botocore.exceptions import ClientError, NoCredentialsError
import json

class EC2Manager:
    def __init__(self, region='us-west-2'):
        """Initialize EC2 client and resource"""
        self.region = region
        try:
            self.ec2_client = boto3.client('ec2', region_name=region)
            self.ec2_resource = boto3.resource('ec2', region_name=region)
            print(f"✅ Connected to EC2 in {region}")
        except NoCredentialsError:
            print("❌ AWS credentials not found. Run 'aws configure' first.")
            raise
    
    def list_instances(self):
        """List all instances with key information"""
        try:
            response = self.ec2_client.describe_instances()
            
            print(f"\n📋 EC2 Instances in {self.region}")
            print("=" * 50)
            
            instance_count = 0
            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    instance_count += 1
                    self._print_instance_info(instance)
            
            if instance_count == 0:
                print("No instances found.")
            else:
                print(f"\nTotal instances: {instance_count}")
                
        except ClientError as e:
            print(f"❌ AWS Error: {e}")
    
    def _print_instance_info(self, instance):
        """Helper method to format instance information"""
        instance_id = instance['InstanceId']
        instance_type = instance['InstanceType']
        state = instance['State']['Name']
        
        # Get instance name from tags
        name = self._get_instance_name(instance)
        
        # Format output
        print(f"🖥️  {instance_id} ({name})")
        print(f"   Type: {instance_type}")
        print(f"   State: {self._format_state(state)}")
        print(f"   Launch: {instance.get('LaunchTime', 'N/A')}")
        
        if 'PublicIpAddress' in instance:
            print(f"   Public IP: {instance['PublicIpAddress']}")
        
        print("-" * 40)
    
    def _get_instance_name(self, instance):
        """Extract instance name from tags"""
        if 'Tags' in instance:
            for tag in instance['Tags']:
                if tag['Key'] == 'Name':
                    return tag['Value']
        return 'No Name'
    
    def _format_state(self, state):
        """Add emoji to state for better visibility"""
        state_emojis = {
            'running': '🟢 running',
            'stopped': '🔴 stopped',
            'pending': '🟡 pending',
            'stopping': '🟡 stopping',
            'terminated': '⚫ terminated'
        }
        return state_emojis.get(state, f"❓ {state}")

# PRACTICE EXERCISES
def practice_exercises():
    """Hands-on exercises for this lesson"""
    print("\n🎯 PRACTICE EXERCISES")
    print("=" * 30)
    
    ec2_mgr = EC2Manager()
    
    # Exercise 1: Basic listing
    print("\n1. List all instances:")
    ec2_mgr.list_instances()

if __name__ == "__main__":
    print("🚀 Starting Lesson 1: EC2 Basics")
    practice_exercises()
    
    print("\n📚 NEXT STEPS:")
    print("- Try launching a free-tier EC2 instance")
    print("- Practice with different regions")
    print("- Move to lesson_02_s3_basics.py")