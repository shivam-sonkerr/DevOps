#!/usr/bin/env python3
"""
AWS Account Resource Cleaner
Comprehensive script to list and delete ALL AWS resources in an account.
WARNING: This script can delete ALL resources in your AWS account!
"""

import boto3
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from botocore.exceptions import ClientError, NoCredentialsError
import sys

class AWSResourceCleaner:
    def __init__(self):
        self.session = boto3.Session()
        self.regions = self.get_all_regions()
        self.resources_found = {}
        
    def get_all_regions(self):
        """Get all AWS regions"""
        try:
            ec2 = self.session.client('ec2', region_name='us-east-1')
            regions = [region['RegionName'] for region in ec2.describe_regions()['Regions']]
            return regions
        except Exception as e:
            print(f"Error getting regions: {e}")
            return ['us-east-1', 'us-west-2', 'eu-west-1']  # fallback
    
    def safe_client_call(self, service, region, operation, **kwargs):
        """Safely make AWS API calls with error handling"""
        try:
            client = self.session.client(service, region_name=region)
            return getattr(client, operation)(**kwargs)
        except Exception as e:
            return None
    
    def list_ec2_resources(self, region):
        """List EC2 resources"""
        resources = {}
        
        # Instances
        result = self.safe_client_call('ec2', region, 'describe_instances')
        if result:
            instances = []
            for reservation in result.get('Reservations', []):
                for instance in reservation.get('Instances', []):
                    if instance['State']['Name'] != 'terminated':
                        instances.append({
                            'id': instance['InstanceId'],
                            'state': instance['State']['Name'],
                            'type': instance['InstanceType']
                        })
            if instances:
                resources['instances'] = instances
        
        # Volumes
        result = self.safe_client_call('ec2', region, 'describe_volumes')
        if result:
            volumes = [{'id': vol['VolumeId'], 'state': vol['State']} 
                      for vol in result.get('Volumes', []) if vol['State'] != 'deleted']
            if volumes:
                resources['volumes'] = volumes
        
        # Security Groups (excluding default)
        result = self.safe_client_call('ec2', region, 'describe_security_groups')
        if result:
            sgs = [{'id': sg['GroupId'], 'name': sg['GroupName']} 
                   for sg in result.get('SecurityGroups', []) if sg['GroupName'] != 'default']
            if sgs:
                resources['security_groups'] = sgs
        
        # Key Pairs
        result = self.safe_client_call('ec2', region, 'describe_key_pairs')
        if result:
            keys = [{'name': kp['KeyName']} for kp in result.get('KeyPairs', [])]
            if keys:
                resources['key_pairs'] = keys
        
        # AMIs (owned by account)
        result = self.safe_client_call('ec2', region, 'describe_images', Owners=['self'])
        if result:
            amis = [{'id': img['ImageId'], 'name': img.get('Name', 'N/A')} 
                   for img in result.get('Images', [])]
            if amis:
                resources['amis'] = amis
        
        # Snapshots (owned by account)
        result = self.safe_client_call('ec2', region, 'describe_snapshots', OwnerIds=['self'])
        if result:
            snapshots = [{'id': snap['SnapshotId'], 'description': snap.get('Description', 'N/A')} 
                        for snap in result.get('Snapshots', [])]
            if snapshots:
                resources['snapshots'] = snapshots
        
        # Elastic IPs
        result = self.safe_client_call('ec2', region, 'describe_addresses')
        if result:
            eips = [{'ip': addr.get('PublicIp', 'N/A'), 'allocation_id': addr.get('AllocationId')} 
                   for addr in result.get('Addresses', [])]
            if eips:
                resources['elastic_ips'] = eips
        
        # Load Balancers (Classic)
        result = self.safe_client_call('elb', region, 'describe_load_balancers')
        if result:
            elbs = [{'name': lb['LoadBalancerName']} for lb in result.get('LoadBalancerDescriptions', [])]
            if elbs:
                resources['classic_load_balancers'] = elbs
        
        # Application Load Balancers
        result = self.safe_client_call('elbv2', region, 'describe_load_balancers')
        if result:
            albs = [{'arn': lb['LoadBalancerArn'], 'name': lb['LoadBalancerName']} 
                   for lb in result.get('LoadBalancers', [])]
            if albs:
                resources['application_load_balancers'] = albs
        
        return resources
    
    def list_s3_resources(self):
        """List S3 resources (global service)"""
        resources = {}
        
        result = self.safe_client_call('s3', 'us-east-1', 'list_buckets')
        if result:
            buckets = [{'name': bucket['Name']} for bucket in result.get('Buckets', [])]
            if buckets:
                resources['buckets'] = buckets
        
        return resources
    
    def list_iam_resources(self):
        """List IAM resources (global service)"""
        resources = {}
        
        # Users
        result = self.safe_client_call('iam', 'us-east-1', 'list_users')
        if result:
            users = [{'name': user['UserName']} for user in result.get('Users', [])]
            if users:
                resources['users'] = users
        
        # Roles
        result = self.safe_client_call('iam', 'us-east-1', 'list_roles')
        if result:
            roles = [{'name': role['RoleName']} for role in result.get('Roles', []) 
                    if not role['RoleName'].startswith('AWSServiceRole')]
            if roles:
                resources['roles'] = roles
        
        # Policies (customer managed)
        result = self.safe_client_call('iam', 'us-east-1', 'list_policies', Scope='Local')
        if result:
            policies = [{'arn': policy['Arn'], 'name': policy['PolicyName']} 
                       for policy in result.get('Policies', [])]
            if policies:
                resources['policies'] = policies
        
        # Groups
        result = self.safe_client_call('iam', 'us-east-1', 'list_groups')
        if result:
            groups = [{'name': group['GroupName']} for group in result.get('Groups', [])]
            if groups:
                resources['groups'] = groups
        
        return resources
    
    def list_rds_resources(self, region):
        """List RDS resources"""
        resources = {}
        
        # DB Instances
        result = self.safe_client_call('rds', region, 'describe_db_instances')
        if result:
            instances = [{'id': db['DBInstanceIdentifier'], 'engine': db['Engine']} 
                        for db in result.get('DBInstances', [])]
            if instances:
                resources['db_instances'] = instances
        
        # DB Clusters
        result = self.safe_client_call('rds', region, 'describe_db_clusters')
        if result:
            clusters = [{'id': cluster['DBClusterIdentifier'], 'engine': cluster['Engine']} 
                       for cluster in result.get('DBClusters', [])]
            if clusters:
                resources['db_clusters'] = clusters
        
        # DB Snapshots
        result = self.safe_client_call('rds', region, 'describe_db_snapshots')
        if result:
            snapshots = [{'id': snap['DBSnapshotIdentifier']} 
                        for snap in result.get('DBSnapshots', []) if snap['SnapshotType'] == 'manual']
            if snapshots:
                resources['db_snapshots'] = snapshots
        
        return resources
    
    def list_lambda_resources(self, region):
        """List Lambda resources"""
        resources = {}
        
        result = self.safe_client_call('lambda', region, 'list_functions')
        if result:
            functions = [{'name': func['FunctionName'], 'runtime': func.get('Runtime', 'N/A')} 
                        for func in result.get('Functions', [])]
            if functions:
                resources['functions'] = functions
        
        return resources
    
    def list_cloudformation_resources(self, region):
        """List CloudFormation resources"""
        resources = {}
        
        result = self.safe_client_call('cloudformation', region, 'describe_stacks')
        if result:
            stacks = [{'name': stack['StackName'], 'status': stack['StackStatus']} 
                     for stack in result.get('Stacks', []) if stack['StackStatus'] != 'DELETE_COMPLETE']
            if stacks:
                resources['stacks'] = stacks
        
        return resources
    
    def list_route53_resources(self):
        """List Route53 resources (global service)"""
        resources = {}
        
        result = self.safe_client_call('route53', 'us-east-1', 'list_hosted_zones')
        if result:
            zones = [{'id': zone['Id'], 'name': zone['Name']} 
                    for zone in result.get('HostedZones', [])]
            if zones:
                resources['hosted_zones'] = zones
        
        return resources
    
    def list_cloudwatch_resources(self, region):
        """List CloudWatch resources"""
        resources = {}
        
        # Alarms
        result = self.safe_client_call('cloudwatch', region, 'describe_alarms')
        if result:
            alarms = [{'name': alarm['AlarmName']} for alarm in result.get('MetricAlarms', [])]
            if alarms:
                resources['alarms'] = alarms
        
        # Log Groups
        result = self.safe_client_call('logs', region, 'describe_log_groups')
        if result:
            log_groups = [{'name': lg['logGroupName']} for lg in result.get('logGroups', [])]
            if log_groups:
                resources['log_groups'] = log_groups
        
        return resources
    
    def list_dynamodb_resources(self, region):
        """List DynamoDB resources"""
        resources = {}
        
        result = self.safe_client_call('dynamodb', region, 'list_tables')
        if result:
            tables = [{'name': table} for table in result.get('TableNames', [])]
            if tables:
                resources['tables'] = tables
        
        return resources
    
    def list_sns_sqs_resources(self, region):
        """List SNS and SQS resources"""
        resources = {}
        
        # SNS Topics
        result = self.safe_client_call('sns', region, 'list_topics')
        if result:
            topics = [{'arn': topic['TopicArn']} for topic in result.get('Topics', [])]
            if topics:
                resources['sns_topics'] = topics
        
        # SQS Queues
        result = self.safe_client_call('sqs', region, 'list_queues')
        if result:
            queues = [{'url': queue} for queue in result.get('QueueUrls', [])]
            if queues:
                resources['sqs_queues'] = queues
        
        return resources
    
    def discover_all_resources(self):
        """Discover all resources across all regions and services"""
        print("🔍 Discovering AWS resources across all regions...")
        
        # Global services (run once)
        print("  Scanning global services...")
        global_resources = {}
        
        s3_resources = self.list_s3_resources()
        if s3_resources:
            global_resources['s3'] = s3_resources
        
        iam_resources = self.list_iam_resources()
        if iam_resources:
            global_resources['iam'] = iam_resources
        
        route53_resources = self.list_route53_resources()
        if route53_resources:
            global_resources['route53'] = route53_resources
        
        if global_resources:
            self.resources_found['global'] = global_resources
        
        # Regional services
        def scan_region(region):
            print(f"  Scanning region: {region}")
            region_resources = {}
            
            # Scan all services for this region
            services = [
                ('ec2', self.list_ec2_resources),
                ('rds', self.list_rds_resources),
                ('lambda', self.list_lambda_resources),
                ('cloudformation', self.list_cloudformation_resources),
                ('cloudwatch', self.list_cloudwatch_resources),
                ('dynamodb', self.list_dynamodb_resources),
                ('sns_sqs', self.list_sns_sqs_resources)
            ]
            
            for service_name, list_func in services:
                try:
                    resources = list_func(region)
                    if resources:
                        region_resources[service_name] = resources
                except Exception as e:
                    print(f"    Error scanning {service_name} in {region}: {e}")
            
            return region, region_resources
        
        # Use threading for faster region scanning
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_region = {executor.submit(scan_region, region): region for region in self.regions}
            
            for future in as_completed(future_to_region):
                region, resources = future.result()
                if resources:
                    self.resources_found[region] = resources
        
        print(f"✅ Resource discovery complete. Found resources in {len(self.resources_found)} locations.")
    
    def display_resources(self):
        """Display all discovered resources"""
        if not self.resources_found:
            print("✅ No resources found in your AWS account!")
            return False
        
        print("\n" + "="*80)
        print("📋 DISCOVERED AWS RESOURCES")
        print("="*80)
        
        total_resources = 0
        
        for location, services in self.resources_found.items():
            print(f"\n🌍 {location.upper()}")
            print("-" * 40)
            
            for service, resource_types in services.items():
                print(f"\n  📦 {service.upper()}")
                for resource_type, resources in resource_types.items():
                    count = len(resources)
                    total_resources += count
                    print(f"    • {resource_type}: {count} items")
                    
                    # Show first few items as examples
                    for i, resource in enumerate(resources[:3]):
                        if isinstance(resource, dict):
                            key = list(resource.keys())[0]
                            value = resource[key]
                            print(f"      - {value}")
                        else:
                            print(f"      - {resource}")
                    
                    if len(resources) > 3:
                        print(f"      ... and {len(resources) - 3} more")
        
        print(f"\n🔢 TOTAL RESOURCES: {total_resources}")
        print("="*80)
        return True
    
    def get_deletion_choices(self):
        """Interactive menu for selective resource deletion"""
        if not self.resources_found:
            return {}
        
        print("\n" + "="*60)
        print("🎯 SELECT RESOURCES TO DELETE")
        print("="*60)
        
        # Build service menu
        service_map = {}
        menu_items = []
        counter = 1
        
        for location, services in self.resources_found.items():
            for service in services.keys():
                service_key = f"{location}:{service}"
                if service_key not in service_map:
                    service_map[counter] = service_key
                    menu_items.append(f"{counter}. {service.upper()} in {location}")
                    counter += 1
        
        # Add special options
        menu_items.append(f"{counter}. DELETE ALL RESOURCES")
        service_map[counter] = "ALL"
        counter += 1
        
        menu_items.append(f"{counter}. Cancel and exit")
        service_map[counter] = "CANCEL"
        
        # Display menu
        print("\nChoose what to delete:")
        for item in menu_items:
            print(f"  {item}")
        
        print(f"\nYou can select multiple options (e.g., 1,3,5) or ranges (e.g., 1-5)")
        
        while True:
            choice = input("\nEnter your choice(s): ").strip()
            
            if not choice:
                continue
            
            try:
                selected_numbers = self.parse_selection(choice, len(service_map))
                break
            except ValueError as e:
                print(f"❌ {e}")
                continue
        
        # Process selections
        selected_services = {}
        delete_all = False
        
        for num in selected_numbers:
            if service_map[num] == "CANCEL":
                print("❌ Operation cancelled.")
                return None
            elif service_map[num] == "ALL":
                delete_all = True
                break
            else:
                location, service = service_map[num].split(":")
                if location not in selected_services:
                    selected_services[location] = []
                selected_services[location].append(service)
        
        if delete_all:
            return self.resources_found
        
        # Build filtered resources
        filtered_resources = {}
        for location, services in selected_services.items():
            filtered_resources[location] = {}
            for service in services:
                if service in self.resources_found[location]:
                    filtered_resources[location][service] = self.resources_found[location][service]
        
        return filtered_resources
    
    def parse_selection(self, selection, max_num):
        """Parse user selection string"""
        numbers = set()
        
        for part in selection.split(','):
            part = part.strip()
            
            if '-' in part:
                # Range selection
                try:
                    start, end = map(int, part.split('-'))
                    if start < 1 or end > max_num or start > end:
                        raise ValueError(f"Invalid range: {part}")
                    numbers.update(range(start, end + 1))
                except ValueError:
                    raise ValueError(f"Invalid range format: {part}")
            else:
                # Single number
                try:
                    num = int(part)
                    if num < 1 or num > max_num:
                        raise ValueError(f"Number {num} is out of range (1-{max_num})")
                    numbers.add(num)
                except ValueError:
                    raise ValueError(f"Invalid number: {part}")
        
        return sorted(numbers)
    
    def confirm_deletion(self, resources_to_delete):
        """Get user confirmation for deletion"""
        if not resources_to_delete:
            return False
        
        print("\n⚠️  WARNING: You are about to DELETE the following resources:")
        
        total_count = 0
        for location, services in resources_to_delete.items():
            print(f"\n🌍 {location.upper()}:")
            for service, resource_types in services.items():
                print(f"  📦 {service.upper()}:")
                for resource_type, resources in resource_types.items():
                    count = len(resources)
                    total_count += count
                    print(f"    • {resource_type}: {count} items")
        
        print(f"\n🔢 TOTAL RESOURCES TO DELETE: {total_count}")
        print("\n⚠️  This action is IRREVERSIBLE!")
        
        confirmation = input("\nType 'DELETE' to confirm: ").strip()
        
        if confirmation != "DELETE":
            print("❌ Deletion cancelled.")
            return False
        
        return True
    
    def delete_resources(self, resources_to_delete):
        """Delete selected resources"""
        print("\n🗑️  Starting resource deletion...")
        
        deletion_order = [
            # Delete in specific order to handle dependencies
            ('ec2', self.delete_ec2_resources),
            ('rds', self.delete_rds_resources),
            ('lambda', self.delete_lambda_resources),
            ('cloudformation', self.delete_cloudformation_resources),
            ('dynamodb', self.delete_dynamodb_resources),
            ('sns_sqs', self.delete_sns_sqs_resources),
            ('cloudwatch', self.delete_cloudwatch_resources),
            ('s3', self.delete_s3_resources),
            ('iam', self.delete_iam_resources),
            ('route53', self.delete_route53_resources)
        ]
        
        for location, services in resources_to_delete.items():
            print(f"\n🌍 Deleting resources in {location}")
            
            for service_name, delete_func in deletion_order:
                if service_name in services:
                    try:
                        delete_func(location, services[service_name])
                    except Exception as e:
                        print(f"❌ Error deleting {service_name} in {location}: {e}")
        
        print("\n✅ Resource deletion completed!")
    
    def delete_ec2_resources(self, region, resources):
        """Delete EC2 resources"""
        print(f"  🖥️  Deleting EC2 resources in {region}")
        
        # Terminate instances
        if 'instances' in resources:
            instance_ids = [inst['id'] for inst in resources['instances']]
            if instance_ids:
                self.safe_client_call('ec2', region, 'terminate_instances', InstanceIds=instance_ids)
                print(f"    Terminated {len(instance_ids)} instances")
        
        # Wait for instances to terminate before deleting other resources
        time.sleep(30)
        
        # Delete volumes
        if 'volumes' in resources:
            for vol in resources['volumes']:
                self.safe_client_call('ec2', region, 'delete_volume', VolumeId=vol['id'])
            print(f"    Deleted {len(resources['volumes'])} volumes")
        
        # Delete snapshots
        if 'snapshots' in resources:
            for snap in resources['snapshots']:
                self.safe_client_call('ec2', region, 'delete_snapshot', SnapshotId=snap['id'])
            print(f"    Deleted {len(resources['snapshots'])} snapshots")
        
        # Delete AMIs
        if 'amis' in resources:
            for ami in resources['amis']:
                self.safe_client_call('ec2', region, 'deregister_image', ImageId=ami['id'])
            print(f"    Deregistered {len(resources['amis'])} AMIs")
        
        # Release Elastic IPs
        if 'elastic_ips' in resources:
            for eip in resources['elastic_ips']:
                if eip.get('allocation_id'):
                    self.safe_client_call('ec2', region, 'release_address', AllocationId=eip['allocation_id'])
            print(f"    Released {len(resources['elastic_ips'])} Elastic IPs")
        
        # Delete Load Balancers
        if 'classic_load_balancers' in resources:
            for elb in resources['classic_load_balancers']:
                self.safe_client_call('elb', region, 'delete_load_balancer', LoadBalancerName=elb['name'])
            print(f"    Deleted {len(resources['classic_load_balancers'])} Classic Load Balancers")
        
        if 'application_load_balancers' in resources:
            for alb in resources['application_load_balancers']:
                self.safe_client_call('elbv2', region, 'delete_load_balancer', LoadBalancerArn=alb['arn'])
            print(f"    Deleted {len(resources['application_load_balancers'])} Application Load Balancers")
        
        # Delete Security Groups (after instances are terminated)
        time.sleep(60)
        if 'security_groups' in resources:
            for sg in resources['security_groups']:
                self.safe_client_call('ec2', region, 'delete_security_group', GroupId=sg['id'])
            print(f"    Deleted {len(resources['security_groups'])} Security Groups")
        
        # Delete Key Pairs
        if 'key_pairs' in resources:
            for kp in resources['key_pairs']:
                self.safe_client_call('ec2', region, 'delete_key_pair', KeyName=kp['name'])
            print(f"    Deleted {len(resources['key_pairs'])} Key Pairs")
    
    def delete_s3_resources(self, region, resources):
        """Delete S3 resources"""
        print("  🪣 Deleting S3 resources")
        
        if 'buckets' in resources:
            for bucket in resources['buckets']:
                bucket_name = bucket['name']
                
                # Delete all objects in bucket first
                try:
                    s3 = self.session.client('s3')
                    
                    # Delete all object versions
                    paginator = s3.get_paginator('list_object_versions')
                    for page in paginator.paginate(Bucket=bucket_name):
                        delete_keys = []
                        
                        if 'Versions' in page:
                            delete_keys.extend([{'Key': obj['Key'], 'VersionId': obj['VersionId']} 
                                              for obj in page['Versions']])
                        
                        if 'DeleteMarkers' in page:
                            delete_keys.extend([{'Key': obj['Key'], 'VersionId': obj['VersionId']} 
                                              for obj in page['DeleteMarkers']])
                        
                        if delete_keys:
                            s3.delete_objects(Bucket=bucket_name, Delete={'Objects': delete_keys})
                    
                    # Delete the bucket
                    s3.delete_bucket(Bucket=bucket_name)
                    print(f"    Deleted bucket: {bucket_name}")
                    
                except Exception as e:
                    print(f"    Failed to delete bucket {bucket_name}: {e}")
    
    def delete_rds_resources(self, region, resources):
        """Delete RDS resources"""
        print(f"  🗄️  Deleting RDS resources in {region}")
        
        # Delete DB instances
        if 'db_instances' in resources:
            for db in resources['db_instances']:
                self.safe_client_call('rds', region, 'delete_db_instance', 
                                    DBInstanceIdentifier=db['id'], 
                                    SkipFinalSnapshot=True,
                                    DeleteAutomatedBackups=True)
            print(f"    Deleted {len(resources['db_instances'])} DB instances")
        
        # Delete DB clusters
        if 'db_clusters' in resources:
            for cluster in resources['db_clusters']:
                self.safe_client_call('rds', region, 'delete_db_cluster',
                                    DBClusterIdentifier=cluster['id'],
                                    SkipFinalSnapshot=True)
            print(f"    Deleted {len(resources['db_clusters'])} DB clusters")
        
        # Delete manual snapshots
        if 'db_snapshots' in resources:
            for snap in resources['db_snapshots']:
                self.safe_client_call('rds', region, 'delete_db_snapshot', 
                                    DBSnapshotIdentifier=snap['id'])
            print(f"    Deleted {len(resources['db_snapshots'])} DB snapshots")
    
    def delete_lambda_resources(self, region, resources):
        """Delete Lambda resources"""
        print(f"  ⚡ Deleting Lambda resources in {region}")
        
        if 'functions' in resources:
            for func in resources['functions']:
                self.safe_client_call('lambda', region, 'delete_function', FunctionName=func['name'])
            print(f"    Deleted {len(resources['functions'])} Lambda functions")
    
    def delete_cloudformation_resources(self, region, resources):
        """Delete CloudFormation resources"""
        print(f"  📚 Deleting CloudFormation resources in {region}")
        
        if 'stacks' in resources:
            for stack in resources['stacks']:
                self.safe_client_call('cloudformation', region, 'delete_stack', StackName=stack['name'])
            print(f"    Deleted {len(resources['stacks'])} CloudFormation stacks")
    
    def delete_dynamodb_resources(self, region, resources):
        """Delete DynamoDB resources"""
        print(f"  🗃️  Deleting DynamoDB resources in {region}")
        
        if 'tables' in resources:
            for table in resources['tables']:
                self.safe_client_call('dynamodb', region, 'delete_table', TableName=table['name'])
            print(f"    Deleted {len(resources['tables'])} DynamoDB tables")
    
    def delete_sns_sqs_resources(self, region, resources):
        """Delete SNS and SQS resources"""
        print(f"  📨 Deleting SNS/SQS resources in {region}")
        
        if 'sns_topics' in resources:
            for topic in resources['sns_topics']:
                self.safe_client_call('sns', region, 'delete_topic', TopicArn=topic['arn'])
            print(f"    Deleted {len(resources['sns_topics'])} SNS topics")
        
        if 'sqs_queues' in resources:
            for queue in resources['sqs_queues']:
                self.safe_client_call('sqs', region, 'delete_queue', QueueUrl=queue['url'])
            print(f"    Deleted {len(resources['sqs_queues'])} SQS queues")
    
    def delete_cloudwatch_resources(self, region, resources):
        """Delete CloudWatch resources"""
        print(f"  📊 Deleting CloudWatch resources in {region}")
        
        if 'alarms' in resources:
            alarm_names = [alarm['name'] for alarm in resources['alarms']]
            if alarm_names:
                self.safe_client_call('cloudwatch', region, 'delete_alarms', AlarmNames=alarm_names)
                print(f"    Deleted {len(alarm_names)} CloudWatch alarms")
        
        if 'log_groups' in resources:
            for lg in resources['log_groups']:
                self.safe_client_call('logs', region, 'delete_log_group', logGroupName=lg['name'])
            print(f"    Deleted {len(resources['log_groups'])} CloudWatch log groups")
    
    def delete_iam_resources(self, region, resources):
        """Delete IAM resources"""
        print("  👤 Deleting IAM resources")
        
        # Delete users (detach policies first)
        if 'users' in resources:
            for user in resources['users']:
                user_name = user['name']
                
                # Detach managed policies
                result = self.safe_client_call('iam', 'us-east-1', 'list_attached_user_policies', UserName=user_name)
                if result:
                    for policy in result.get('AttachedPolicies', []):
                        self.safe_client_call('iam', 'us-east-1', 'detach_user_policy', 
                                            UserName=user_name, PolicyArn=policy['PolicyArn'])
                
                # Delete inline policies
                result = self.safe_client_call('iam', 'us-east-1', 'list_user_policies', UserName=user_name)
                if result:
                    for policy_name in result.get('PolicyNames', []):
                        self.safe_client_call('iam', 'us-east-1', 'delete_user_policy', 
                                            UserName=user_name, PolicyName=policy_name)
                
                # Delete access keys
                result = self.safe_client_call('iam', 'us-east-1', 'list_access_keys', UserName=user_name)
                if result:
                    for key in result.get('AccessKeyMetadata', []):
                        self.safe_client_call('iam', 'us-east-1', 'delete_access_key', 
                                            UserName=user_name, AccessKeyId=key['AccessKeyId'])
                
                # Delete user
                self.safe_client_call('iam', 'us-east-1', 'delete_user', UserName=user_name)
            
            print(f"    Deleted {len(resources['users'])} IAM users")
        
        # Delete roles
        if 'roles' in resources:
            for role in resources['roles']:
                role_name = role['name']
                
                # Detach managed policies
                result = self.safe_client_call('iam', 'us-east-1', 'list_attached_role_policies', RoleName=role_name)
                if result:
                    for policy in result.get('AttachedPolicies', []):
                        self.safe_client_call('iam', 'us-east-1', 'detach_role_policy', 
                                            RoleName=role_name, PolicyArn=policy['PolicyArn'])
                
                # Delete inline policies
                result = self.safe_client_call('iam', 'us-east-1', 'list_role_policies', RoleName=role_name)
                if result:
                    for policy_name in result.get('PolicyNames', []):
                        self.safe_client_call('iam', 'us-east-1', 'delete_role_policy', 
                                            RoleName=role_name, PolicyName=policy_name)
                
                # Delete role
                self.safe_client_call('iam', 'us-east-1', 'delete_role', RoleName=role_name)
            
            print(f"    Deleted {len(resources['roles'])} IAM roles")
        
        # Delete policies
        if 'policies' in resources:
            for policy in resources['policies']:
                self.safe_client_call('iam', 'us-east-1', 'delete_policy', PolicyArn=policy['arn'])
            print(f"    Deleted {len(resources['policies'])} IAM policies")
        
        # Delete groups
        if 'groups' in resources:
            for group in resources['groups']:
                group_name = group['name']
                
                # Detach policies
                result = self.safe_client_call('iam', 'us-east-1', 'list_attached_group_policies', GroupName=group_name)
                if result:
                    for policy in result.get('AttachedPolicies', []):
                        self.safe_client_call('iam', 'us-east-1', 'detach_group_policy', 
                                            GroupName=group_name, PolicyArn=policy['PolicyArn'])
                
                # Delete group
                self.safe_client_call('iam', 'us-east-1', 'delete_group', GroupName=group_name)
            
            print(f"    Deleted {len(resources['groups'])} IAM groups")
    
    def delete_route53_resources(self, region, resources):
        """Delete Route53 resources"""
        print("  🌐 Deleting Route53 resources")
        
        if 'hosted_zones' in resources:
            for zone in resources['hosted_zones']:
                zone_id = zone['id']
                
                # Delete all records except NS and SOA
                result = self.safe_client_call('route53', 'us-east-1', 'list_resource_record_sets', HostedZoneId=zone_id)
                if result:
                    for record in result.get('ResourceRecordSets', []):
                        if record['Type'] not in ['NS', 'SOA']:
                            self.safe_client_call('route53', 'us-east-1', 'change_resource_record_sets',
                                                HostedZoneId=zone_id,
                                                ChangeBatch={
                                                    'Changes': [{
                                                        'Action': 'DELETE',
                                                        'ResourceRecordSet': record
                                                    }]
                                                })
                
                # Delete hosted zone
                self.safe_client_call('route53', 'us-east-1', 'delete_hosted_zone', Id=zone_id)
            
            print(f"    Deleted {len(resources['hosted_zones'])} Route53 hosted zones")


def main():
    """Main execution function"""
    print("🚨 AWS ACCOUNT RESOURCE CLEANER 🚨")
    print("="*50)
    print("This script will find and selectively delete AWS resources!")
    print("="*50)
    
    try:
        # Initialize cleaner
        cleaner = AWSResourceCleaner()
        
        # Discover all resources
        cleaner.discover_all_resources()
        
        # Display resources
        has_resources = cleaner.display_resources()
        
        if not has_resources:
            return
        
        # Get user selection
        resources_to_delete = cleaner.get_deletion_choices()
        
        if resources_to_delete is None:
            return
        
        # Get confirmation
        if not cleaner.confirm_deletion(resources_to_delete):
            return
        
        # Delete selected resources
        cleaner.delete_resources(resources_to_delete)
        
        print("\n🎉 AWS resource cleanup completed!")
        print("Selected resources have been deleted from your account.")
        
    except NoCredentialsError:
        print("❌ AWS credentials not found. Please configure your credentials.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
