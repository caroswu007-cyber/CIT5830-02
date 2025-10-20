import os
import requests
import jason

PINATA_PIN_URL = "https://api.pinata.cloud/pinning/pinJSONToIPFS"
IPFS_GATEWAY = "https://ipfs.io/ipfs"

def pin_to_ipfs(data):
    assert isinstance(data, dict), "Error pin_to_ipfs expects a dictionary"

    jwt = os.getenv("PINATA_JWT")
    use_jwt = bool(jwt and jwt.strip().startswith("eyJ"))

    if use_jwt:
        headers = {
            "Authorization": f"Bearer {jwt.strip()}",
            "Content-Type": "application/json",
        }
    else:
        api_key = os.getenv("PINATA_KEY")
        api_secret = os.getenv("PINATA_SECRET")
        assert api_key and api_secret, "Missing PINATA_KEY/PINATA_SECRET"
        headers = {
            "pinata_api_key": api_key.strip(),
            "pinata_secret_api_key": api_secret.strip(),
            "Content-Type": "application/json",
        }

    
    print("AUTH_MODE=", "JWT" if use_jwt else "KEY_SECRET")
    if not use_jwt:
        print(
            "KEY_PREFIX=",
            headers.get("pinata_api_key", "")[:6],
            headers.get("pinata_secret_api_key", "")[:6],
        )

    r = requests.post(PINATA_PIN_URL, headers=headers, json={"pinataContent": data}, timeout=30)
    r.raise_for_status()
    return r.json()["IpfsHash"]

def get_from_ipfs(cid):
    url = f"{IPFS_GATEWAY}/{cid}"
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    obj = r.json()
    assert isinstance(obj, dict)
    return obj
