import base64
import tanker_identity.crypto

from tanker_identity.test.helpers import corrupt_buffer

import pytest


def test_hash():
    hex_vector = 'BA80A53F981C4D0D6A2797B69F12F6E94C212F14685AC4B74B12BB6FDBFFA2D17D87C5392AAB792DC252D5DE4533CC9518D38AA8DBF1925AB92386EDD4009923'  # noqa
    vector = bytearray.fromhex(hex_vector)
    buffer = b'abc'
    output = tanker_identity.crypto.generichash(buffer, size=64)

    assert output == vector


def test_valid_signature_hard_coded(test_trustchain):
    message = b'message'
    public_key = base64.b64decode(test_trustchain["public_key"])
    private_key = base64.b64decode(test_trustchain["private_key"])
    signature = tanker_identity.crypto.sign_detached(message, private_key)
    tanker_identity.crypto.verify_sign_detached(message, signature, public_key)


def test_valid_signature_generated_keys():
    message = b'message'
    public_key, private_key = tanker_identity.crypto.sign_keypair()
    signature = tanker_identity.crypto.sign_detached(message, private_key)
    tanker_identity.crypto.verify_sign_detached(message, signature, public_key)


def test_sign_invalid_message():
    message = b'message'
    public_key, secret_key = tanker_identity.crypto.sign_keypair()
    signature = tanker_identity.crypto.sign_detached(message, secret_key)

    invalid_message = b'm3ss4ge'
    with pytest.raises(tanker_identity.crypto.InvalidSignature):
        tanker_identity.crypto.verify_sign_detached(invalid_message, signature, public_key)


def test_sign_invalid_signature():
    message = b'message'
    public_key, secret_key = tanker_identity.crypto.sign_keypair()
    signature = tanker_identity.crypto.sign_detached(message, secret_key)

    invalid_signature = corrupt_buffer(signature)
    with pytest.raises(tanker_identity.crypto.InvalidSignature):
        tanker_identity.crypto.verify_sign_detached(message, invalid_signature, public_key)
