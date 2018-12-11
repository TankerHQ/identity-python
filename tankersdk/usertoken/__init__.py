import base64
import json
import os

from tankersdk.crypto import BLOCK_HASH_SIZE, CHECK_HASH_BLOCK_SIZE, USER_SECRET_SIZE
import tankersdk.crypto


def generate_user_token(trustchain_id, trustchain_private_key, user_id):
    trustchain_id_buf = base64.b64decode(trustchain_id)
    private_key_buf = base64.b64decode(trustchain_private_key)

    user_id_buff = user_id.encode()
    to_hash = user_id_buff + trustchain_id_buf
    hashed_user_id = tankersdk.crypto.generichash(to_hash, size=BLOCK_HASH_SIZE)

    e_public_key, e_secret_key = tankersdk.crypto.sign_keypair()
    to_sign = e_public_key + hashed_user_id
    delegation_signature = tankersdk.crypto.sign_detached(to_sign, private_key_buf)
    random_buf = os.urandom(USER_SECRET_SIZE - 1)
    hashed = tankersdk.crypto.generichash(random_buf + hashed_user_id, size=CHECK_HASH_BLOCK_SIZE)
    user_secret = random_buf + bytearray([hashed[0]])

    user_token = {
        "ephemeral_private_signature_key": base64.b64encode(e_secret_key).decode(),
        "ephemeral_public_signature_key": base64.b64encode(e_public_key).decode(),
        "user_id": base64.b64encode(hashed_user_id).decode(),
        "delegation_signature": base64.b64encode(delegation_signature).decode(),
        "user_secret": base64.b64encode(user_secret).decode(),
    }

    as_json = json.dumps(user_token)
    return base64.b64encode(as_json.encode()).decode()
