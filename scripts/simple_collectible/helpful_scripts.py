from brownie import accounts,network, interface, config, exceptions
from web3 import Web3

# List of all the testing environments.
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development","mainnet-fork"]

# To interact with any contract over the world you need an
# - ABI
# - Contract Address
# You can actually generate ABI from Interface. (Just make sure that Interface has the functions you need to interact with.) 

    
def get_account(index=None, id=None):
    """Returns the account depending upon network."""
    if index:
        return accounts[index]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    if id: 
        return accounts.load(id)
    if network.show_active() in config["networks"]:
        return accounts.add(config["wallets"]["from_key"])
    return None


def pretty_output(action=""):
    # Used to seprate the output
    s=""
    r = range(0,100)
    for i in r:
        if i == (len(r)/2):
            s+=action
        s+='='
    print(s)

