from lib2to3.pgen2.tokenize import tokenize
from brownie import accounts, network, AdvancedCollectible,config
from scripts.advanced_collectible.create_metadata import create_meta
from scripts.advanced_collectible.helpful_scripts import BLOCK_CONFIRMATIONS_FOR_VERIFICATION, OPENSEA_URL, get_account, get_pp, getContract, listen_for_event
from scripts.advanced_collectible.rng_manager import add_vrf_consumer_to_subscription, subscription



def depoly_consumer(consumer):
    account = get_account()
    print(f"[Network] Current Network: {network.show_active()}")
    
    subscription()

    vrf_coordinator = getContract("vrf_coordinator")
    link_token = getContract("link_token")
    subscription_id = config["networks"][network.show_active()]["subId"]
    keyHash = config["networks"][network.show_active()]["keyHash"]
    
    if len(consumer) <= 0:
        vrf_consumer = consumer.deploy(vrf_coordinator, link_token, subscription_id, keyHash, {"from": account})
        print(f"[Contract] Contract has been deployed at {vrf_consumer.address}")
        if config["networks"][network.show_active()].get("verify", False):
            consumer.publish_source(vrf_consumer)
    else:
        vrf_consumer = consumer[-1]
        print(f"[Contract] Selected Contract {vrf_consumer.address}")
    
    
    
    add_vrf_consumer_to_subscription(subscription_id,vrf_consumer)
    
    return vrf_consumer

def deploy():
    account = get_account()
    depoly_consumer(AdvancedCollectible)
    for i in range(11):
        create_collectible()
    

def create_collectible():
    account = get_account()
    advanced_collectible = AdvancedCollectible[-1]
    advanced_collectible.createCollectible({"from": account})
    print("[Contract] Collectible Created!")
    listen_for_event(advanced_collectible,"ReturnedRandomness")

    token_id = advanced_collectible.tokenCounter() - 1
    print(f"[Contract] Current Number Of Token Id: {token_id}")

    ppnumberfromtoken = advanced_collectible.tokenIdToPP(token_id)
    print(f"[Token] The Token: {token_id} is assigned to PP: {ppnumberfromtoken}")
    pptype = get_pp(ppnumberfromtoken)[0]
    print(f"[Contract] Setting tokenURI of: {token_id} with PP: {ppnumberfromtoken}")
    uri = create_meta(token_id, ppnumberfromtoken)
    if uri != None:
        set_TokenURI(token_id, advanced_collectible, uri)

def set_TokenURI(tokenid, contract, tokenURI):
    account = get_account()
    tx = contract.setTokenURI(tokenid,tokenURI,{"from":account})
    tx.wait(1)
    print(f"[NFT] You can now successfully view your NFT at {OPENSEA_URL.format(contract.address,tokenid)}")

def main():
    deploy()