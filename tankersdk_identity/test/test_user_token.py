import base64

import tankersdk_identity.crypto
import tankersdk_identity

import pytest
from tankersdk_identity.test.helpers import corrupt_buffer, check_user_secret, check_signature, parse_b64_json


def generate_test_token(test_trustchain):
    user_id = "guido@tanker.io"
    b64_token = tankersdk_identity.generate_user_token(
        test_trustchain["id"],
        test_trustchain["private_key"],
        user_id
    )
    token = parse_b64_json(b64_token)
    return token


def test_generate_token_happy(test_trustchain):
    token = generate_test_token(test_trustchain)
    delegation_signature = base64.b64decode(token["delegation_signature"])

    check_user_secret(token, "user_id")
    check_signature(test_trustchain["public_key"], token, delegation_signature, "user_id")


def test_generate_token_invalid_signature(test_trustchain):
    token = generate_test_token(test_trustchain)
    delegation_signature = base64.b64decode(token["delegation_signature"])
    invalid_signature = corrupt_buffer(delegation_signature)

    with pytest.raises(tankersdk_identity.crypto.InvalidSignature):
        check_signature(test_trustchain["public_key"], token, invalid_signature, "user_id")
