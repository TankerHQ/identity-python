from typing import Tuple, cast
from nacl.exceptions import BadSignatureError
from nacl.bindings.crypto_sign import (
    crypto_sign,
    crypto_sign_keypair,
    crypto_sign_open,
    crypto_sign_BYTES,
)
from nacl.bindings.crypto_box import crypto_box_keypair
from nacl.bindings.crypto_generichash import generichash_blake2b_salt_personal


BLOCK_HASH_SIZE = 32
CHECK_HASH_BLOCK_SIZE = 16
USER_SECRET_SIZE = 32


class Error(Exception):
    pass


class InvalidSignature(Error):
    pass


def generichash(buffer: bytes, size: int) -> bytes:
    return generichash_blake2b_salt_personal(buffer, digest_size=size)  # type: ignore


def sign_keypair() -> Tuple[bytes, bytes]:
    """
    Generate a pair of signing keys and return a tuple (public_key, private_key)
    """
    return crypto_sign_keypair()  # type: ignore


def box_keypair() -> Tuple[bytes, bytes]:
    """
    Generate a pair of encryption keys and return a tuple (public_key, private_key)
    """
    return crypto_box_keypair()  # type: ignore


def sign_detached(message: bytes, private_key: bytes) -> bytes:
    """
    Sign a message with a private key and return the detached signature
    """
    raw_combined = cast(bytes, crypto_sign(message, private_key))
    return raw_combined[:crypto_sign_BYTES]


def verify_sign_detached(message: bytes, signature: bytes, public_key: bytes) -> None:
    """
    Verify the signature of the message given the signature and the public key
    """
    try:
        combined = signature + message
        crypto_sign_open(combined, public_key)
    except BadSignatureError:
        raise InvalidSignature()
