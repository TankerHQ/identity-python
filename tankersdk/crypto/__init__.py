from typing import Tuple

import nacl.hash
import nacl.signing
from nacl.exceptions import BadSignatureError
from nacl.encoding import RawEncoder


BLOCK_HASH_SIZE = 32
CHECK_HASH_BLOCK_SIZE = 16
USER_SECRET_SIZE = 32


class Error(Exception):
    pass


class InvalidSignature(Error):
    pass


def generichash(buffer: bytes, *, size: int) -> bytes:
    return nacl.hash.blake2b(buffer, digest_size=size, encoder=RawEncoder)


def sign_keypair() -> Tuple[bytes, bytes]:
    """
    Generate a pair of signing keys and return a tuple (public_key, private_key)
    """
    signing_key = nacl.signing.SigningKey.generate()
    public_key = signing_key.verify_key
    public_key_bytes = public_key.encode(encoder=RawEncoder)
    # SigningKey.encode() would return the *seed*, not the value
    private_key_bytes = signing_key._signing_key
    return public_key_bytes, private_key_bytes


def sign_detached(message: bytes, private_key: bytes) -> bytes:
    """
    Sign a message with a private key and return the detached signature
    """
    # We can't instanciate a signing key directly with the *value*
    # so we instantiate it with a fake seed and then
    # overwrite the ._signing_key member
    fake_seed = b"\0" * 32
    signing_key = nacl.signing.SigningKey(fake_seed)
    signing_key._signing_key = private_key
    signed_message = signing_key.sign(message, encoder=RawEncoder)
    return signed_message.signature


def verify_sign_detached(message: bytes, signature: bytes, public_key: bytes) -> None:
    """
    Verify the signature of the message given the signature and the public key
    """
    try:
        public_key = nacl.signing.VerifyKey(public_key, encoder=RawEncoder)
        public_key.verify(message, signature, encoder=RawEncoder)
    except BadSignatureError:
        raise InvalidSignature()
