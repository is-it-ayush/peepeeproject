from brownie import (network,accounts,config,LinkToken,MockV3Aggregator,MockOracle,VRFCoordinatorMock,Contract,web3,interface)
import time

OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"

from web3 import Web3

NON_FORKED_LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["hardhat", "development", "ganache"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = NON_FORKED_LOCAL_BLOCKCHAIN_ENVIRONMENTS + ["mainnet-fork", "binance-fork", "matic-fork",]
# Etherscan usually takes a few blocks to register the contract has been deployed
BLOCK_CONFIRMATIONS_FOR_VERIFICATION = 6

CONTRACT_TO_MOCK = {"link_token": LinkToken, "eth_usd_price_feed": MockV3Aggregator, "vrf_coordinator": VRFCoordinatorMock, "oracle": MockOracle,}

DECIMALS = 18
INITIAL_VALUE = web3.toWei(2000, "ether")
BASE_FEE = 100000000000000000  # The premium
GAS_PRICE_LINK = 1e9  # Some value calculated depending on the Layer 1 cost and Link


PP_NAME = { 0 :"Average Hairy Circum", 1 :"Average Clean Circum", 2 :"Average Hairy Uncircum", 3 :"Average Clean Uncircum", 4 :"Short Hairy Uncircum", 5 :"Short Clean Uncircum", 6 :"Short Hairy Circum", 7 :"Short Clean Circum", 8 :"Huge Hairy Circum", 9 :"Huge Clean Circum", 10 :"Huge Hairy Uncircum", 11 :"Huge Clean Uncircum"}
PP_DESC = { 0 : "Buddy Eric's PeePee.",
    1: "Yo! Eric has a date.",
    2: "The noble knight.",
    3: "The King.",
    4: "Lannister's personal PeePee.",
    5: "It's not the size of sword it's how you use it.",
    6: "You can do it.",
    7: "I am sorry for you little one.",
    8: "The rare PeePee.",
    9: "The emperor.",
    10: "The NFT Creator's PeePee",
    11: "It resides in the darkest corner's of the [REDACTED].",

}

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
    return accounts.add(config["wallets"]["from_key"])

def pretty_output(action=""):
    # Used to seprate the output
    s=""
    r = range(0,100)
    for i in r:
        if i == (len(r)/2):
            s+=action
        s+='='
    print(s)


# Getting the contract
def getContract(contractName):
    """ This function will grab the contract addresses from the bronwie config if defined, otherwise, it will dpeloy a mock version of the contract, and reuturn the address of mock contract.

        Args:
            contract_name(string)
        
        Returns:
            brownie.network.contract.ProjectContract: The most recently deployed version of the contract.
    """
    # Getting which contract is the variable referring to.
    contract_type = CONTRACT_TO_MOCK[contractName] 
    # If network is not a real network i.e. a Local Blockchain Environment, deploy a mock so we can fetch the variable.
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        # If the mock is already deployed, get the latest deployed mock else deploy one.
        if len(contract_type) <=0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        # If this is a real netwrok, fetch the variable from brownie-config.yaml where its defined under networks section.
        contract_address = config["networks"][network.show_active()][contractName]
        # Then Get the details of contract from name, its address and its abi to interact with it.
        contract = Contract.from_abi(contract_type._name, contract_address , contract_type.abi)
    # Finally return the contract.
    return contract

# deploy_mocks(): To deploy the mocks. Take's Decimals and intital value.
def deploy_mocks(decimals=DECIMALS, initial_value=INITIAL_VALUE):
    # Print in a neat way.
    pretty_output("Mocks")
    # Grab Account depending upon network.
    account = get_account()
    # Deploy LinkToken Mock to send $LINK to Randomess Generator.   
    link_token = LinkToken.deploy({"from":account})
    # Deploy VRFCoordinator Mock to conenct with VRF Node.
    VRFCoordinatorMock.deploy(link_token.address,{"from":account})
    print(f"[Contract] The contract has been deployed.")


def vrf_data(subId=None,i=False):
    vrfc = interface.IVRFCoordinatorV2(getContract("vrf_coordinator"))
    if i:
        print(f"[VRF] Using Subscription Id: {subId}")
    cordinator_data = vrfc.getSubscription(subId, {"from": get_account()})
    return cordinator_data

def get_node_balance(subId=None,i=False):
    data = vrf_data(subId)
    balance_in_link = Web3.fromWei(data[0],"ether")
    if i:
        print(f"[VRF] Node Balnce: {balance_in_link} LINK.")
    return balance_in_link



def listen_for_event(brownie_contract, event, timeout=200, poll_interval=2):
    """Listen for an event to be fired from a contract.
    We are waiting for the event to return, so this function is blocking.
    Args:
        brownie_contract ([brownie.network.contract.ProjectContract]):
        A brownie contract of some kind.
        event ([string]): The event you'd like to listen for.
        timeout (int, optional): The max amount in seconds you'd like to
        wait for that event to fire. Defaults to 200 seconds.
        poll_interval ([int]): How often to call your node to check for events.
        Defaults to 2 seconds.
    """
    web3_contract = web3.eth.contract(
        address=brownie_contract.address, abi=brownie_contract.abi
    )
    start_time = time.time()
    current_time = time.time()
    event_filter = web3_contract.events[event].createFilter(fromBlock="latest")
    while current_time - start_time < timeout:
        for event_response in event_filter.get_new_entries():
            if event in event_response.event:
                print("[EVENT] An Event Has Occured.")
                return event_response
        time.sleep(poll_interval)
        current_time = time.time()
    print("[EVENT] Timeout has reached! Event Not Found!")
    return {"event": None}

def get_pp(pp_number):
    return (PP_NAME[pp_number],PP_DESC[pp_number])