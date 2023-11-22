import web3

# Connect to a BSC node
def is_valid_eth_address(address):
    if not isinstance(address, str):
        return False
    return address.startswith("0x") and len(address) == 42

