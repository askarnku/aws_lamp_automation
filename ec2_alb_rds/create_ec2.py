import boto3
import os
from dotenv import load_dotenv

load_dotenv()

def create_ec2_instances(client, subnet_id, security_group_id):
    instances = client.run_instances(
        ImageId='ami-04fdea8e25817cd69',
        InstanceType='t2.micro',
        KeyName=os.getenv('KEY_PAIR_NAME'),
        MinCount=1,
        MaxCount=1,
        NetworkInterfaces=[
            {
                'SubnetId': subnet_id,
                'DeviceIndex': 0,
                'AssociatePublicIpAddress': True,
                'Groups': [security_group_id]
            }
        ],
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [{'Key': 'Name', 'Value': 'EC2 Instance'}]
            }
        ]
    )
    return [instance['InstanceId'] for instance in instances['Instances']]

def create_instance(subnet_id=None, security_group_id=None):

    # Check if subnet_id and security_group_id are provided
    if not subnet_id or not security_group_id:
        raise ValueError("subnet_id and security_group_id must be provided")

    # Initialize boto3 clients
    ec2_client = boto3.client('ec2')

    # Step 3: Create EC2 Instances
    ec2_instance_ids = create_ec2_instances(ec2_client, subnet_id, security_group_id)

    return ec2_instance_ids

if __name__ == "__main__":
    # Replace "null" with actual subnet_id and security_group_id values, or set them as environment variables
    try:
        response = create_instance(subnet_id=None, security_group_id=None)
        print(response)
    except ValueError as e:
        print(f"Error: {e}")
