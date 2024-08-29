from network_module.network_setup import setup_network

if __name__ == "__main__":
    vpc_id, public_subnet_1a, private_subnet_1a, public_subnet_1b, private_subnet_1b, igw_id, public_rt_id = setup_network()


print(vpc_id)


'''.env
        # Print or return all IDs for further use or export
    return {
        vpc_id, public_subnet_1a, private_subnet_1a, public_subnet_1b, private_subnet_1b, igw_id, public_rt_id
    }
'''