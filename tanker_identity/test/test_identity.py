import base64

import tanker_identity.crypto
import tanker_identity.identity

import pytest
from tanker_identity.test.helpers import corrupt_buffer, check_user_secret, check_signature, parse_b64_json


def generate_test_identity(test_trustchain):
    user_id = "guido@tanker.io"
    b64_identity = tanker_identity.identity.create_identity(
        test_trustchain["id"],
        test_trustchain["private_key"],
        user_id
    )
    identity = parse_b64_json(b64_identity)
    return identity


def test_generate_identity_happy(test_trustchain):
    identity = generate_test_identity(test_trustchain)
    delegation_signature = base64.b64decode(identity["delegation_signature"])

    assert identity["trustchain_id"] == test_trustchain["id"].decode()
    check_user_secret(identity)
    check_signature(test_trustchain["public_key"], identity, delegation_signature)


def test_generate_identity_invalid_signature(test_trustchain):
    identity = generate_test_identity(test_trustchain)
    delegation_signature = base64.b64decode(identity["delegation_signature"])
    invalid_signature = corrupt_buffer(delegation_signature)

    with pytest.raises(tanker_identity.crypto.InvalidSignature):
        check_signature(test_trustchain["public_key"], identity, invalid_signature)


def test_provisional_identities_are_different(test_trustchain):
    identity_alice = parse_b64_json(tanker_identity.identity.create_provisional_identity(
        test_trustchain["id"],
        "alice@gmail.ru"
    ))
    identity_bob = parse_b64_json(tanker_identity.identity.create_provisional_identity(
        test_trustchain["id"],
        "bob@office360.com"
    ))

    for key_pair in ["encryption_key_pair", "signature_key_pair"]:
        assert identity_alice[key_pair]["public_key"] != identity_bob[key_pair]["public_key"]


def test_public_identity_matches_provisional_identity(test_trustchain):
    encoded_identity = tanker_identity.identity.create_provisional_identity(
        test_trustchain["id"],
        "snowy@nasa.gov"
    )
    identity = parse_b64_json(encoded_identity)
    public_identity = parse_b64_json(tanker_identity.identity.get_public_identity(encoded_identity))

    assert public_identity["trustchain_id"] == test_trustchain["id"].decode()
    assert public_identity["public_signature_key"] == identity["signature_key_pair"]["public_key"]
    assert public_identity["public_encryption_key"] == identity["encryption_key_pair"]["public_key"]


def test_public_identity_matches_full_identity(test_trustchain):
    user_id = "happy@little.cloud"
    encoded_identity = tanker_identity.identity.create_identity(
        test_trustchain["id"],
        test_trustchain["private_key"],
        user_id
    )
    identity = parse_b64_json(encoded_identity)
    public_identity = parse_b64_json(tanker_identity.identity.get_public_identity(encoded_identity))

    assert public_identity["trustchain_id"] == test_trustchain["id"].decode()
    assert public_identity["target"] == "user"
    assert public_identity["value"] == identity["user_id"]

