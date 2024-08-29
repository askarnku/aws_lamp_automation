import boto3
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create a boto3 client for EC2
client = boto3.client('ec2')

def create_vpc(client, cidr_block, vpc_name):
    response_vpc = client.create_vpc(
        CidrBlock=cidr_block,
        TagSpecifications=[ 
            {
                'ResourceType':'vpc',
                'Tags': [
                    {
                        'Key':'Name',
                        'Value':vpc_name
                    }
                ]
            },
        ]
    )
    return response_vpc['Vpc']['VpcId']

def create_subnet(client, vpc_id, cidr_block, zone, subnet_name):
    response_subnet = client.create_subnet(
        TagSpecifications=[
            {
                'ResourceType': 'subnet',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': subnet_name
                    },
                ]
            },
        ],
        AvailabilityZone=zone,
        VpcId=vpc_id,
        CidrBlock=cidr_block
    )
    return response_subnet['Subnet']['SubnetId']

def create_internet_gateway(client):
    response_igw = client.create_internet_gateway()
    return response_igw['InternetGateway']['InternetGatewayId']

def attach_internet_gateway(client, vpc_id, igw_id):
    client.attach_internet_gateway(
        InternetGatewayId=igw_id,
        VpcId=vpc_id
    )

def create_route_table(client, vpc_id, rt_name):
    response_rt = client.create_route_table(
        VpcId=vpc_id,
        TagSpecifications=[
            {
                'ResourceType': 'route-table',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': rt_name
                    },
                ]
            },
        ]
    )
    return response_rt['RouteTable']['RouteTableId']

def create_route(client, rt_id, igw_id):
    client.create_route(
        RouteTableId=rt_id,
        DestinationCidrBlock='0.0.0.0/0',
        GatewayId=igw_id
    )

def associate_route_table(client, subnet_id, rt_id):
    client.associate_route_table(
        SubnetId=subnet_id,
        RouteTableId=rt_id
    )

# Main Function
def setup_network():
    vpc_id = create_vpc(client, os.getenv("CIDR_BLOCK_VPC"), 'aws_final_project_vpc')

    # Create subnets
    public_subnet_1a = create_subnet(client, vpc_id, os.getenv('CIDR_BLOCK_SUBNET_PUBLIC_1A'), os.getenv('AZ_1A'), 'public_1a')
    private_subnet_1a = create_subnet(client, vpc_id, os.getenv('CIDR_BLOCK_SUBNET_PRIVATE_1A'), os.getenv('AZ_1A'), 'private_1a')
    public_subnet_1b = create_subnet(client, vpc_id, os.getenv('CIDR_BLOCK_SUBNET_PUBLIC_1B'), os.getenv('AZ_1B'), 'public_1b')
    private_subnet_1b = create_subnet(client, vpc_id, os.getenv('CIDR_BLOCK_SUBNET_PRIVATE_1B'), os.getenv('AZ_1B'), 'private_1b')

    # Create and attach Internet Gateway
    igw_id = create_internet_gateway(client)
    attach_internet_gateway(client, vpc_id, igw_id)

    # Create Route Table for public subnets and add route to Internet Gateway
    public_rt_id = create_route_table(client, vpc_id, 'public_rt')
    create_route(client, public_rt_id, igw_id)

    # Associate Route Table with public subnets
    associate_route_table(client, public_subnet_1a, public_rt_id)
    associate_route_table(client, public_subnet_1b, public_rt_id)

    # Print or return all IDs for further use or export
    return (
        vpc_id,
        public_subnet_1a,
        private_subnet_1a,
        public_subnet_1b,
        private_subnet_1b,
        igw_id,
        public_rt_id
    )

if __name__ == "__main__":
    resources = setup_network()
    print(resources)