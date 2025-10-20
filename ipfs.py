import os
import json
import requests

PINATA_PIN_URL = "https://api.pinata.cloud/pinning/pinJSONToIPFS"
IPFS_GATEWAY = "https://ipfs.io/ipfs"

def pin_to_ipfs(data):
    assert isinstance(data, dict), "Error pin_to_ipfs expects a dictionary"

    jwt = os.getenv("PINATA_JWT")
    if jwt:
        headers = {
            "Authorization": f"Bearer {jwt}",
            "Content-Type": "application/json",
        }
    else:
        api_key = os.getenv("PINATA_KEY")
        api_secret = os.getenv("PINATA_SECRET")
        assert api_key and api_secret, "Missing PINATA_KEY/PINATA_SECRET"
        headers = {
            "pinata_api_key": api_key,
            "pinata_secret_api_key": api_secret,
            "Content-Type": "application/json",
        }

    payload = {"pinataContent": data}
    r = requests.post(PINATA_PIN_URL, headers=headers, json=payload, timeout=30)
    r.raise_for_status()
    cid = r.json().get("IpfsHash")
    assert cid, f"Pinata response missing CID: {r.text}"
    return cid

def get_from_ipfs(cid):
    url = f"{IPFS_GATEWAY}/{cid}"
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    obj = r.json()
    assert isinstance(obj, dict)
    return obj
