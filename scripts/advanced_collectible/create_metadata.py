from fileinput import filename
from importlib.metadata import metadata
import json
from brownie import AdvancedCollectible, network
from scripts.advanced_collectible.helpful_scripts import get_pp
from metadata.sample_metadata import metadata_template
from pathlib import Path

from scripts.advanced_collectible.upload_to_pinata import upload


def create_meta(token_id, pp):
    advanced_collectible = AdvancedCollectible[-1]
    no_of_tokens = advanced_collectible.tokenCounter()
    print(f"[Contract] Current Number Of Contract: {no_of_tokens}")
    ppname = get_pp(pp)[0]
    ppdesc = get_pp(pp)[1]
    metadata_file_name = f"./metadata/{network.show_active()}/{token_id}-{ppname}.json"
    collectible_metadata = metadata_template
    if Path(metadata_file_name).exists():
        print(f"[Metadata] {metadata_file_name} already exists.")
        return None
    else:
        print(f"[Metadata] Creating metadata filename: {metadata_file_name}")
        collectible_metadata["name"] = ppname
        collectible_metadata["description"] = ppdesc
        image_path = "./img/" + "pp" + str(pp) + ".png"
        image_uri = upload(image_path)
        collectible_metadata["image"] = image_uri
        with open(metadata_file_name, "w") as f:
            json.dump(collectible_metadata, f)
        metadata_uri = upload(metadata_file_name)
        print(metadata_uri)
        return metadata_uri

def main():
    create_meta()

# def upload_to_ipfs(filepath):
#     with Path(filepath).open("rb") as fp:
#         image_binary = fp.read()
#         # Now we will uplaod this
#         ipfs_url = "http://127.0.0.1:5001"
#         endpoint = "/api/v0/add"
#         response =  requests.post(ipfs_url + endpoint, files={"file": image_binary})
#         ipfs_hash = response.json()["Hash"]
#         filename = filepath.split("/")[-1:][0]
#         image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
#         print(image_uri)
#         return image_uri
# Note: If you are using this function you need to have IPFS Running.