import json
import os
from pathlib import Path
import requests


def upload(filepath):
    PINATA_BASE_URL = "https://api.pinata.cloud"
    endpoint = "/pinning/pinFileToIPFS"
    filename = filepath.split("/")[-1:][0]
    print(filename)
    headers = {
        "pinata_api_key": str(os.getenv("PINATA_API_KEY")),
        "pinata_secret_api_key": str(os.getenv("PINATA_API_SECRET")),
    }
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        response = requests.post(
        PINATA_BASE_URL + endpoint,files={"file": (filename, image_binary)},headers=headers,)
        pinata_hash = response.json()["IpfsHash"]
        image_uri = f"https://gateway.pinata.cloud/ipfs/{pinata_hash}"
        return image_uri
