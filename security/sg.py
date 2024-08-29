import os
import boto3
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def create_security_group(ec2_client, group_name, description, vpc_id, ingress_rules): # get the VPC id
    """
    Create a security group with the specified ingress rules.

    :param ec2_client: Boto3 EC2 client
    :param group_name: Name of the security group
    :param description: Description of the security group
    :param vpc_id: The ID of the VPC
    :param ingress_rules: List of ingress rules to apply to the security group
    :return: The created security group ID
    """
    response_sg = ec2_client.create_security_group(
        GroupName=group_name,
        Description=description,
        VpcId=vpc_id
    )

    ec2_client.authorize_security_group_ingress(
        GroupId=response_sg['GroupId'],
        IpPermissions=ingress_rules
    )

    sg_id = response_sg['GroupId']
    print(f"{group_name} Security Group ID: {sg_id}")
    return sg_id

def create_sgs(vpc_id_par):
    # Initialize EC2 client
    region_name = os.getenv('AZ')
    vpc_id=vpc_id_par
    ec2_client = boto3.client('ec2')

    # Define ingress rules for EC2 security group
    ec2_ingress_rules = [
        {
            'IpProtocol': 'tcp',
            'FromPort': 22,
            'ToPort': 22,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]  # Replace with more restrictive CIDR if needed
        },
        {
            'IpProtocol': 'tcp',
            'FromPort': 80,
            'ToPort': 80,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
        },
        {
            'IpProtocol': 'tcp',
            'FromPort': 443,
            'ToPort': 443,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
        }
    ]

    # Create EC2 security group and get its ID
    ec2_sg_id = create_security_group(
        ec2_client,
        group_name='EC2SecurityGroup',
        description='Security group for EC2 instances',
        vpc_id=vpc_id,
        ingress_rules=ec2_ingress_rules
    )

    # Define ingress rules for ALB security group
    alb_ingress_rules = [
        {
            'IpProtocol': 'tcp',
            'FromPort': 80,
            'ToPort': 80,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
        },
        {
            'IpProtocol': 'tcp',
            'FromPort': 443,
            'ToPort': 443,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
        }
    ]

    # Create ALB security group and get its ID
    alb_sg_id = create_security_group(
        ec2_client,
        group_name='ALBSecurityGroup',
        description='Security group for Application Load Balancer',
        vpc_id=vpc_id,
        ingress_rules=alb_ingress_rules
    )

    # Define ingress rules for RDS security group
    rds_ingress_rules = [
        {
            'IpProtocol': 'tcp',
            'FromPort': 3306,
            'ToPort': 3306,
            'IpRanges': [{'CidrIp': os.getenv('CIDR_BLOCK_SUBNET_PUBLIC_1A')}, {'CidrIp': os.getenv('CIDR_BLOCK_SUBNET_PUBLIC_1B')}] 
        }
    ]

    # Create RDS security group and get its ID
    rds_sg_id = create_security_group(
        ec2_client,
        group_name='RDSSecurityGroup',
        description='Security group for RDS instance',
        vpc_id=vpc_id,
        ingress_rules=rds_ingress_rules
    )

    # Return the security group IDs
    return (
        ec2_sg_id,
        alb_sg_id,
        rds_sg_id
    )

if __name__ == "__main__":
    response = create_sgs(vpc_id_par="null")
    print(response)
