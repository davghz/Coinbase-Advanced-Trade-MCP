# jwt_generator.py – Patched for raw key ID use (no ORG prefix)
# Validated against Coinbase Ed25519 JavaScript reference logic

from dotenv import load_dotenv
load_dotenv()


import time
import json
import base64
import secrets
import os
from typing import Union
from nacl.signing import SigningKey

# Load from environment
KEY_ID = os.getenv("COINBASE_KEY_ID")
PRIVATE_KEY_BASE64 = os.getenv("COINBASE_ED25519_KEY")


def base64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("utf-8")


def build_jwt(
    method: str = "GET",
    path: str = "/api/v3/brokerage/accounts",
    host: str = "api.coinbase.com"
) -> str:
    """
    Creates a Coinbase-compliant Ed25519 JWT token (no org ID)
    - Matches JavaScript example from official docs
    - Claims: iss, sub, nbf, exp, uri
    - Header: alg, kid, nonce, typ
    """
    now = int(time.time())
    nonce = secrets.token_hex(16)
    uri = f"{method.upper()} {host}{path}"

    header = {
        "alg": "EdDSA",
        "kid": KEY_ID,
        "nonce": nonce,
        "typ": "JWT"
    }

    payload = {
        "iss": "cdp",
        "sub": KEY_ID,
        "nbf": now,
        "exp": now + 120,
        "uri": uri
    }

    header_b64 = base64url_encode(json.dumps(header).encode())
    payload_b64 = base64url_encode(json.dumps(payload).encode())
    signing_input = f"{header_b64}.{payload_b64}".encode()

    key_bytes = base64.b64decode(PRIVATE_KEY_BASE64)[:32]  # Only first 32 bytes
    signing_key = SigningKey(key_bytes)
    signature = signing_key.sign(signing_input).signature
    signature_b64 = base64url_encode(signature)

    jwt_token = f"{header_b64}.{payload_b64}.{signature_b64}"

    print("[🔐 JWT Created: Coinbase Compatible — Raw Key ID Mode]")
    print("Header:", json.dumps(header, indent=2))
    print("Payload:", json.dumps(payload, indent=2))
    return jwt_token
