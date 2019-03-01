import base64

import tanker_identity.crypto
import tanker_identity.identity

import pytest
from tanker_identity.test.helpers import corrupt_buffer, check_user_secret, check_signature, parse_b64_json


def generate_test_token(test_trustchain):
    user_id = "guido@tanker.io"
    b64_token = tanker_identity.identity.generate_user_token(
        test_trustchain["id"],
        test_trustchain["private_key"],
        user_id
    )
    token = parse_b64_json(b64_token)
    return token


def test_generate_token_happy(test_trustchain):
    token = generate_test_token(test_trustchain)
    delegation_signature = base64.b64decode(token["delegation_signature"])

    check_user_secret(token)
    check_signature(test_trustchain["public_key"], token, delegation_signature)


def test_generate_token_invalid_signature(test_trustchain):
    token = generate_test_token(test_trustchain)
    delegation_signature = base64.b64decode(token["delegation_signature"])
    invalid_signature = corrupt_buffer(delegation_signature)

    with pytest.raises(tanker_identity.crypto.InvalidSignature):
        check_signature(test_trustchain["public_key"], token, invalid_signature)


