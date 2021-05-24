from collections.abc import Mapping
from typing import Dict, Tuple, Any
import base64
import json
import os

from tankersdk_identity.crypto import (
    BLOCK_HASH_SIZE,
    CHECK_HASH_BLOCK_SIZE,
    USER_SECRET_SIZE,
)
import tankersdk_identity.crypto


APP_SECRET_SIZE = 64
APP_PUBLIC_KEY_SIZE = 32
AUTHOR_SIZE = 32
APP_CREATION_NATURE = 1


def _hash_user_id(app_id: bytes, user_id: str) -> bytes:
    user_id_buff = user_id.encode()
    to_hash = user_id_buff + app_id
    return tankersdk_identity.crypto.generichash(to_hash, size=BLOCK_HASH_SIZE)


def _generate_app_id(app_secret: bytes) -> bytes:
    public_key = app_secret[APP_SECRET_SIZE - APP_PUBLIC_KEY_SIZE : APP_SECRET_SIZE]
    to_hash = bytes(bytearray([APP_CREATION_NATURE] + [0] * AUTHOR_SIZE)) + public_key
    return tankersdk_identity.crypto.generichash(to_hash, size=BLOCK_HASH_SIZE)


KeyPair = Dict[str, str]
PreShareKeys = Tuple[KeyPair, KeyPair]


def _generate_preshare_keys() -> PreShareKeys:
    enc_pub_key, enc_priv_key = tankersdk_identity.crypto.box_keypair()
    encryption_keys = {
        "public_key": base64.b64encode(enc_pub_key).decode(),
        "private_key": base64.b64encode(enc_priv_key).decode(),
    }
    sig_pub_key, sig_priv_key = tankersdk_identity.crypto.sign_keypair()
    signature_keys = {
        "public_key": base64.b64encode(sig_pub_key).decode(),
        "private_key": base64.b64encode(sig_priv_key).decode(),
    }
    return encryption_keys, signature_keys


def _deserialize_identity(identity: str) -> Dict[str, str]:
    identity_json = base64.b64decode(identity).decode()
    return json.loads(identity_json)  # type: ignore


def _to_ordered_json(obj: Dict[str, Any]) -> str:
    json_order = {
        "trustchain_id": 1,
        "target": 2,
        "value": 3,
        "delegation_signature": 4,
        "ephemeral_public_signature_key": 5,
        "ephemeral_private_signature_key": 6,
        "user_secret": 7,
        "public_encryption_key": 8,
        "private_encryption_key": 9,
        "public_signature_key": 10,
        "private_signature_key": 11,
    }
    keys = sorted(obj.keys(), key=json_order.get)  # type: ignore
    items = []
    for k in keys:
        items.append(f'"{k}":"{obj[k]}"')
    return f"{{{','.join(items)}}}"


def _serialize_identity(identity: Dict[str, Any]) -> str:
    as_json = _to_ordered_json(identity)
    return base64.b64encode(as_json.encode()).decode()


def create_identity(app_id: str, app_secret: str, user_id: str) -> str:
    app_id_buf = base64.b64decode(app_id)
    secret_buf = base64.b64decode(app_secret)
    hashed_user_id = _hash_user_id(app_id_buf, user_id)

    generated_app_id = _generate_app_id(secret_buf)
    if generated_app_id != app_id_buf:
        raise ValueError("App secret and app ID mismatch")

    e_public_key, e_secret_key = tankersdk_identity.crypto.sign_keypair()
    to_sign = e_public_key + hashed_user_id
    delegation_signature = tankersdk_identity.crypto.sign_detached(to_sign, secret_buf)
    random_buf = os.urandom(USER_SECRET_SIZE - 1)
    hashed = tankersdk_identity.crypto.generichash(
        random_buf + hashed_user_id, size=CHECK_HASH_BLOCK_SIZE
    )
    user_secret = random_buf + bytearray([hashed[0]])

    identity = {
        "trustchain_id": app_id,
        "target": "user",
        "value": base64.b64encode(hashed_user_id).decode(),
        "user_secret": base64.b64encode(user_secret).decode(),
        "ephemeral_public_signature_key": base64.b64encode(e_public_key).decode(),
        "ephemeral_private_signature_key": base64.b64encode(e_secret_key).decode(),
        "delegation_signature": base64.b64encode(delegation_signature).decode(),
    }

    return _serialize_identity(identity)


def create_provisional_identity(app_id: str, email: str) -> str:
    encryption_keys, signature_keys = _generate_preshare_keys()

    identity = {
        "trustchain_id": app_id,
        "target": "email",
        "value": email,
        "public_encryption_key": encryption_keys["public_key"],
        "private_encryption_key": encryption_keys["private_key"],
        "public_signature_key": signature_keys["public_key"],
        "private_signature_key": signature_keys["private_key"],
    }  # type: Dict[str, str]

    return _serialize_identity(identity)


def get_public_identity(identity: str) -> str:
    identity_obj = _deserialize_identity(identity)

    if identity_obj["target"] == "user":
        public_identity = {
            "trustchain_id": identity_obj["trustchain_id"],
            "target": identity_obj["target"],
            "value": identity_obj["value"],
        }
    elif (
        "public_encryption_key" in identity_obj
        and "public_signature_key" in identity_obj
    ):
        # We have a provisional identity
        public_identity = {
            "trustchain_id": identity_obj["trustchain_id"],
            "target": identity_obj["target"],
            "value": identity_obj["value"],
            "public_signature_key": identity_obj["public_signature_key"],
            "public_encryption_key": identity_obj["public_encryption_key"],
        }
    else:
        raise ValueError("Not a valid Tanker identity")

    return _serialize_identity(public_identity)
