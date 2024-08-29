from network_module.network_setup import setup_network
from security.sg import create_sgs
from ec2_alb_rds.create_services import create_resources

if __name__ == "__main__":
    (
        vpc_id,
        public_subnet_1a,
        private_subnet_1a, 
        public_subnet_1b,
        private_subnet_1b,
        igw_id,
        public_rt_id
    ) = setup_network()

    print(public_subnet_1a)
    print(public_subnet_1b)

    (
        ec2_sg_id,
        alb_sg_id,
        rds_sg_id 
    ) = create_sgs(vpc_id)

    #Create 2 instances in 2 regions
    create_resources(public_subnet_1a, ec2_sg_id)
    create_resources(public_subnet_1b, ec2_sg_id)

