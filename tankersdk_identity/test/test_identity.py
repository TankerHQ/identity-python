from typing import Dict
import base64
import json

import tankersdk_identity.crypto
import tankersdk_identity
from tankersdk_identity import _deserialize_identity

import pytest
from tankersdk_identity.test.helpers import (
    corrupt_buffer,
    check_user_secret,
    check_signature,
)


def generate_test_identity(test_app: Dict[str, str]) -> Dict[str, str]:
    user_id = "guido@tanker.io"
    b64_identity = tankersdk_identity.create_identity(
        test_app["id"], test_app["secret"], user_id
    )
    identity = _deserialize_identity(b64_identity)
    return identity


def test_generate_identity_happy(test_app: Dict[str, str]) -> None:
    identity = generate_test_identity(test_app)
    delegation_signature = base64.b64decode(identity["delegation_signature"])

    assert identity["trustchain_id"] == test_app["id"]
    check_user_secret(identity, "value")
    check_signature(test_app["public_key"], identity, delegation_signature, "value")


def test_generate_identity_invalid_signature(test_app: Dict[str, str]) -> None:
    identity = generate_test_identity(test_app)
    delegation_signature = base64.b64decode(identity["delegation_signature"])
    invalid_signature = corrupt_buffer(delegation_signature)

    with pytest.raises(tankersdk_identity.crypto.InvalidSignature):
        check_signature(test_app["public_key"], identity, invalid_signature, "value")


def test_provisional_identities_are_different(test_app: Dict[str, str]) -> None:
    identity_alice = _deserialize_identity(
        tankersdk_identity.create_provisional_identity(test_app["id"], "alice@gmail.ru")
    )
    identity_bob = _deserialize_identity(
        tankersdk_identity.create_provisional_identity(
            test_app["id"], "bob@office360.com"
        )
    )

    for key in ["public_encryption_key", "public_signature_key"]:
        assert identity_alice[key] != identity_bob[key]


def test_public_identity_matches_provisional_identity(test_app: Dict[str, str]) -> None:
    encoded_identity = tankersdk_identity.create_provisional_identity(
        test_app["id"], "snowy@nasa.gov"
    )
    identity = _deserialize_identity(encoded_identity)
    public_identity = _deserialize_identity(
        tankersdk_identity.get_public_identity(encoded_identity)
    )

    assert public_identity["trustchain_id"] == test_app["id"]
    assert public_identity["target"] == "email"
    assert public_identity["public_signature_key"] == identity["public_signature_key"]
    assert public_identity["public_encryption_key"] == identity["public_encryption_key"]


def test_public_identity_matches_full_identity(test_app: Dict[str, str]) -> None:
    user_id = "happy@little.cloud"
    encoded_identity = tankersdk_identity.create_identity(
        test_app["id"], test_app["secret"], user_id
    )
    identity = _deserialize_identity(encoded_identity)
    public_identity = _deserialize_identity(
        tankersdk_identity.get_public_identity(encoded_identity)
    )

    assert public_identity["trustchain_id"] == test_app["id"]
    assert public_identity["target"] == "user"
    assert public_identity["value"] == identity["value"]


def test_get_public_from_bad_identity() -> None:
    fake_id = base64.b64encode(json.dumps({"target": "stuffs"}).encode()).decode()
    with pytest.raises(ValueError):
        tankersdk_identity.get_public_identity(fake_id)


def test_mistmatch_app_id_and_secret(test_app: Dict[str, str]) -> None:
    user_id = "guido@tanker.io"
    mismatching_app_id = "rB0/yEJWCUVYRtDZLtXaJqtneXQOsCSKrtmWw+V+ysc="
    with pytest.raises(ValueError):
        tankersdk_identity.create_identity(
            mismatching_app_id, test_app["secret"], user_id
        )
