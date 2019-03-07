import base64
import json
import os

from tankersdk_identity.crypto import BLOCK_HASH_SIZE, CHECK_HASH_BLOCK_SIZE, USER_SECRET_SIZE
import tankersdk_identity.crypto


def _hash_user_id(trustchain_id, user_id):
    user_id_buff = user_id.encode()
    to_hash = user_id_buff + trustchain_id
    return tankersdk_identity.crypto.generichash(to_hash, size=BLOCK_HASH_SIZE)


def _generate_preshare_keys():
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


def generate_user_token(trustchain_id, trustchain_private_key, user_id):
    trustchain_id_buf = base64.b64decode(trustchain_id)
    private_key_buf = base64.b64decode(trustchain_private_key)
    hashed_user_id = _hash_user_id(trustchain_id_buf, user_id)

    e_public_key, e_secret_key = tankersdk_identity.crypto.sign_keypair()
    to_sign = e_public_key + hashed_user_id
    delegation_signature = tankersdk_identity.crypto.sign_detached(to_sign, private_key_buf)
    random_buf = os.urandom(USER_SECRET_SIZE - 1)
    hashed = tankersdk_identity.crypto.generichash(random_buf + hashed_user_id, size=CHECK_HASH_BLOCK_SIZE)
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


def create_identity(trustchain_id, trustchain_private_key, user_id):
    trustchain_id_buf = base64.b64decode(trustchain_id)
    private_key_buf = base64.b64decode(trustchain_private_key)
    hashed_user_id = _hash_user_id(trustchain_id_buf, user_id)

    e_public_key, e_secret_key = tankersdk_identity.crypto.sign_keypair()
    to_sign = e_public_key + hashed_user_id
    delegation_signature = tankersdk_identity.crypto.sign_detached(to_sign, private_key_buf)
    random_buf = os.urandom(USER_SECRET_SIZE - 1)
    hashed = tankersdk_identity.crypto.generichash(random_buf + hashed_user_id, size=CHECK_HASH_BLOCK_SIZE)
    user_secret = random_buf + bytearray([hashed[0]])

    identity = {
        "trustchain_id": trustchain_id,
        "user_id": base64.b64encode(hashed_user_id).decode(),
        "user_secret": base64.b64encode(user_secret).decode(),
        "ephemeral_public_signature_key": base64.b64encode(e_public_key).decode(),
        "ephemeral_private_signature_key": base64.b64encode(e_secret_key).decode(),
        "delegation_signature": base64.b64encode(delegation_signature).decode(),
    }

    as_json = json.dumps(identity)
    return base64.b64encode(as_json.encode()).decode()


def create_provisional_identity(trustchain_id, email):
    encryption_keys, signature_keys = _generate_preshare_keys()

    identity = {
        "trustchain_id": trustchain_id,
        "target": "email",
        "value": email,
        "signature_key_pair": signature_keys,
        "encryption_key_pair": encryption_keys,
    }

    as_json = json.dumps(identity)
    return base64.b64encode(as_json.encode()).decode()


def get_public_identity(identity):
    identity_json = base64.b64decode(identity).decode()
    identity_obj = json.loads(identity_json)

    if "user_id" in identity_obj:
        public_identity = {
            "trustchain_id": identity_obj["trustchain_id"],
            "target": "user",
            "value": identity_obj["user_id"],
        }
    elif "encryption_key_pair" in identity_obj and "signature_key_pair" in identity_obj:
        # We have a provisional identity
        public_identity = {
            "trustchain_id": identity_obj["trustchain_id"],
            "target": identity_obj["target"],
            "value": identity_obj["value"],
            "public_signature_key": identity_obj["signature_key_pair"]["public_key"],
            "public_encryption_key": identity_obj["encryption_key_pair"]["public_key"],
        }
    else:
        raise ValueError("Not a valid Tanker identity")

    as_json = json.dumps(public_identity)
    return base64.b64encode(as_json.encode()).decode()


def upgrade_user_token(trustchain_id, user_id, user_token):
    trustchain_id_buf = base64.b64decode(trustchain_id)
    hashed_user_id = _hash_user_id(trustchain_id_buf, user_id)
    token_json = base64.b64decode(user_token)
    token_obj = json.loads(token_json)

    if base64.b64encode(hashed_user_id) != token_obj['user_id']:
        raise ValueError("Invalid user ID provided")

    identity = {
        "trustchain_id": trustchain_id,
        "user_id": token_obj["user_id"],
        "user_secret": token_obj["user_secret"],
        "ephemeral_public_signature_key": token_obj["ephemeral_public_signature_key"],
        "ephemeral_private_signature_key": token_obj["ephemeral_private_signature_key"],
        "delegation_signature": token_obj["delegation_signature"],
    }

    as_json = json.dumps(identity)
    return base64.b64encode(as_json.encode()).decode()
