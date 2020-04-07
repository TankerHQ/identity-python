import base64
import json
import tankersdk_identity.crypto

from tankersdk_identity.crypto import (
    BLOCK_HASH_SIZE,
    CHECK_HASH_BLOCK_SIZE,
    USER_SECRET_SIZE,
)


def parse_b64_json(b64_json):
    json_obj = base64.b64decode(b64_json)
    return json.loads(json_obj.decode())


def corrupt_buffer(buffer):
    """ Make sure one part of the buffer gets changed """
    array = bytearray(buffer)
    array[0] = (array[0] + 1) % 255
    return bytes(array)


def check_user_secret(token_or_identity, id_key):
    hashed_user_id = base64.b64decode(token_or_identity[id_key])
    user_secret = base64.b64decode(token_or_identity["user_secret"])

    assert len(hashed_user_id) == BLOCK_HASH_SIZE
    assert len(user_secret) == USER_SECRET_SIZE
    to_hash = user_secret[:-1] + hashed_user_id
    control = tankersdk_identity.crypto.generichash(to_hash, size=CHECK_HASH_BLOCK_SIZE)
    assert user_secret[-1] == control[0]


def check_signature(public_key, token, signature, id_key):
    e_pub_key = base64.b64decode(token["ephemeral_public_signature_key"])
    user_id = base64.b64decode(token[id_key])
    signed_data = e_pub_key + user_id
    verify_key = base64.b64decode(public_key)
    tankersdk_identity.crypto.verify_sign_detached(signed_data, signature, verify_key)
