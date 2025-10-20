import os
import json
import requests

def pin_to_ipfs(data):
    assert isinstance(data, dict), "Error pin_to_ipfs expects a dictionary"
    jwt = os.getenv("PINATA_JWT")
    assert jwt, "Missing PINATA_JWT environment variable"
    url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"
    headers = {"Authorization": f"Bearer {jwt}", "Content-Type": "application/json"}
    payload = {"pinataContent": data}
    r = requests.post(url, headers=headers, json=payload, timeout=30)
    r.raise_for_status()
    resp = r.json()
    cid = resp.get("IpfsHash") or resp.get("cid") or resp.get("Hash")
    assert cid, f"Pinata response missing CID: {resp}"
    return cid

def get_from_ipfs(cid, content_type="json"):
    assert isinstance(cid, str), "get_from_ipfs accepts a cid in the form of a string"
    url = f"https://gateway.pinata.cloud/ipfs/{cid}"
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    data = r.json() if content_type == "json" else json.loads(r.text)
    assert isinstance(data, dict), "get_from_ipfs should return a dict"
    return data
