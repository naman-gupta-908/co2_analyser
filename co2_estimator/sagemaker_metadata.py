import requests
import boto3

def get_instance_metadata():
    try:
        instance_id = requests.get('http://169.254.169.254/latest/meta-data/instance-id', timeout=1).text
        ec2 = boto3.client('ec2')
        instance = ec2.describe_instances(InstanceIds=[instance_id])
        instance_type = instance['Reservations'][0]['Instances'][0]['InstanceType']
        region = instance['Reservations'][0]['Instances'][0]['Placement']['AvailabilityZone'][:-1]
        return instance_type, region
    except Exception as e:
        print("Error fetching instance metadata:", e)
        return "unknown", "unknown"
