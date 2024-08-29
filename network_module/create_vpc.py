import boto3
import os
from dotenv import load_dotenv

load_dotenv()

# Create a boto3 client for EC2
client = boto3.client('ec2')

response_vpc = client.create_vpc(
    CidrBlock=os.getenv("CIDR_BLOCK_VPC"),
    TagSpecifications = [ 
        {
            'ResourceType':'vpc',
            'Tags': [
                {
                    'Key':'Name',
                    'Value':'aws_final_project_vpc'
                }
            ]
        },
    ]
)

# Create 1 private and 1 public subnets per zone 1
response_pubsub_1a = client.create_subnet(
        TagSpecifications=[
        {
            'ResourceType': 'subnet',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'public_1a'
                },
            ]
        },
    ],
    AvailabilityZone='us-west-1a',
    VpcId=response_vpc['Vpc']['VpcId'],
    CidrBlock=os.getenv('CIDR_BLOCK_SUBNET_PUBLIC_1A')
)


response_prisub_1a = client.create_subnet(
        TagSpecifications=[
        {
            'ResourceType': 'subnet',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'private_1a'
                },
            ]
        },
    ],
    AvailabilityZone='us-west-1a',
    VpcId=response_vpc['Vpc']['VpcId'],
    CidrBlock=os.getenv('CIDR_BLOCK_SUBNET_PRIVATE_1A')
)

# Create 1 private and 1 public subnets per zone 2
response_pubsub_1b = client.create_subnet(
        TagSpecifications=[
        {
            'ResourceType': 'subnet',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'public_1b'
                },
            ]
        },
    ],
    AvailabilityZone='us-west-1b',
    VpcId=response_vpc['Vpc']['VpcId'],
    CidrBlock=os.getenv('CIDR_BLOCK_SUBNET_PUBLIC_1B')
)


response_prisub_1b = client.create_subnet(
        TagSpecifications=[
        {
            'ResourceType': 'subnet',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'private_1b'
                },
            ]
        },
    ],
    AvailabilityZone='us-west-1b',
    VpcId=response_vpc['Vpc']['VpcId'],
    CidrBlock=os.getenv('CIDR_BLOCK_SUBNET_PRIVATE_1B')
)

# Return subnet_id = response_subnet['Subnet']['SubnetId']

# Create Internet Gateway and Attach it to VPC
response_igw = client.create_internet_gateway()

client.attach_internet_gateway(
    InternetGatewayId=response_igw['InternetGateway']['InternetGatewayId'],
    VpcId=response_vpc['Vpc']['VpcId']
)

# Create Route Table for public subnets
response_public_rt=client.create_route_table(
    VpcId=response_vpc['Vpc']['VpcId'],
    TagSpecifications=[
        {
            'ResourceType': 'route-table',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'public_rt'
                },
            ]
        },
    ]
)

# Create a route to the Internet Gateway
client.create_route(
    RouteTableId=response_public_rt['RouteTable']['RouteTableId'],
    DestinationCidrBlock='0.0.0.0/0',
    GatewayId=response_igw['InternetGateway']['InternetGatewayId']
)

# Associate the route table with the first public subnet
client.associate_route_table(
    SubnetId=response_pubsub_1a['Subnet']['SubnetId'],
    RouteTableId=response_public_rt['RouteTable']['RouteTableId']
)

# Associate the route table with the second public subnet
client.associate_route_table(
    SubnetId=response_pubsub_1b['Subnet']['SubnetId'],
    RouteTableId=response_public_rt['RouteTable']['RouteTableId']
)
