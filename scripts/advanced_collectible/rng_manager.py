from aiohttp import request
from brownie import AdvancedCollectible, network, config, VRFCoordinatorMock, Contract, LinkToken, convert,interface
from scripts.advanced_collectible.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, NON_FORKED_LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account, getContract, pretty_output
import yaml
from pathlib import Path
from web3 import Web3

def create_subscription():
    if config["networks"][network.show_active()].get("subId", False) == False:
        account = get_account()
        vrf_coordinator = interface.IVRFCoordinator(getContract("vrf_coordinator"))
        print("[Subscription] Creating a Subscription.")
        tx = vrf_coordinator.createSubscription({"from": account})
        tx.wait(1)
        subId = tx.events[0]["subId"]
        config_path = Path("brownie-config.yaml").absolute()
        print(f"[Subscription] Your Subscription ID is: {subId}")
        if network.show_active() not in NON_FORKED_LOCAL_BLOCKCHAIN_ENVIRONMENTS:
            with open(config_path, "r") as file:
                configuration = yaml.safe_load(file)
                configuration["networks"][network.show_active()][
                    "subId"
                ] = int(subId)
            with open(config_path, "w") as file:
                yaml.dump(configuration, file)
            print("[Subscription] Your Subscription ID has been successfully saved.")
    else:
        subId = config["networks"][network.show_active()]["subId"]
        print(f"[Subscription] Subscription Selected: {subId}")
    return subId


def fund_subscription(subId=1):
    print("[Subscription] Funding The Subscription.")
    account = get_account()
    fee = config["networks"][network.show_active()]["fee"]
    if network.show_active() not in NON_FORKED_LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        link_token = getContract("link_token")
        vrf_coordinator = interface.IVRFCoordinator(getContract("vrf_coordinator"))
        tx = link_token.transferAndCall(vrf_coordinator.address,fee,convert.to_bytes(subId),{"from": account},)
        tx.wait(1)
    else:
        vrf_coordinator = interface.IVRFCoordinator(getContract("vrf_coordinator"))
        tx = vrf_coordinator.fundSubscription(subId, fee, {"from": account})
        tx.wait(1)
    print("[Subscription] Subscription has been succesffully funded!")

def is_funded(subId):
    print(f"[Subscription] Getting Subscription Id: {subId} details. ")
    vrf_coordinator = interface.IVRFCoordinator(getContract("vrf_coordinator"))
    fee = config["networks"][network.show_active()]["fee"]
    subscription_details = vrf_coordinator.getSubscription(subId)
    print(f"[Subscription] Subscription details: {subscription_details}")
    if subscription_details[0] >= fee:
        return True
    return False

def subscription():
    pretty_output("Subscription")
    subId = create_subscription()
    if not is_funded(subId):
        fund_subscription(subId=subId)
    else:
        print("[Subscription] Subscription is already funded.")


def add_vrf_consumer_to_subscription(subId, vrf_consumer):
    vrf_coordinator = interface.IVRFCoordinator(getContract("vrf_coordinator"))
    subscription_details = vrf_coordinator.getSubscription(subId)
    if vrf_consumer in subscription_details[3]:
        print(f"[VRF] {vrf_consumer} is already in the subscription")
    else:
        print(f"[VRF] Adding Consumer: {vrf_consumer} to VRFCoordinator: {vrf_coordinator.address}")
        account = get_account()
        tx = vrf_coordinator.addConsumer.transact(subId, vrf_consumer.address, {"from": account})
        tx.wait(1)
        print("[VRF] Consumer Added!")
        

def requestRandomness(contract):
    account = get_account()
    vrf_contract = contract[-1]
    try:
        tx = vrf_contract.requestRandomWords({"from": account})
        tx.wait(1)
    except:
        print("[RNG] Error Occured: Kindly Check your funds @ https://vrf.chain.link/")
    print("[RNG] Random Numbers have been requested.")


def readRandomWords(contract):
    vrf_contract = contract[-1]
    try:
        print(f"[RNG] Random Word 0:\t {vrf_contract.randomWords(0)}")
        print(f"[RNG] Random Word 0:\t {vrf_contract.randomWords(1)}")
    except:
        print("[RNG] Please wait a minute for the node to respond.")


def requestRandomWords():
    subscription()
    requestRandomness()