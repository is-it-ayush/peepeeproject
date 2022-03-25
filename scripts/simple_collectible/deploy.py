from brownie import SimpleCollectible, accounts

from scripts.simple_collectible.helpful_scripts import get_account

sample_token_uri = 'https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json'
OPEN_SEA_URI = 'https://testnets.opensea.io/assets/{}/{}'

def deploy():
    account = get_account()
    print(account)
    simple_collectible = SimpleCollectible.deploy({"from": account})
    tx = simple_collectible.createCollectible(sample_token_uri, {"from": account})
    tx.wait(1)
    print(f"[NFT] Collectible Created. View {OPEN_SEA_URI.format(simple_collectible.address, simple_collectible.tokenCounter() - 1)}")
    return simple_collectible
    
def main():
    deploy()