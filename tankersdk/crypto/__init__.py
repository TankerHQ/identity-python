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


def generichash(buffer, *, size):
    return nacl.hash.blake2b(buffer, digest_size=size, encoder=RawEncoder)


def sign_keypair():
    signing_key = nacl.signing.SigningKey.generate()
    public_key = signing_key.verify_key
    # SigningKey.encode() return the *seed*, not the value
    return public_key.encode(encoder=RawEncoder), signing_key._signing_key


def sign_detached(message, private_key):
    # We can't instanciate a signing key directly with the *value*
    # so we call generate() with a fake seed an then
    # overwrite the ._signing_key memeber
    fake_seed = b"\0" * 32
    signing_key = nacl.signing.SigningKey(fake_seed)
    signing_key._signing_key = private_key
    signed_message = signing_key.sign(message, encoder=RawEncoder)
    return signed_message.signature


def verify_sign_detached(message, signature, public_key):
    print("verify_sign_detached", signature, message, public_key)
    try:
        public_key = nacl.signing.VerifyKey(public_key, encoder=RawEncoder)
        public_key.verify(message, signature, encoder=RawEncoder)
    except BadSignatureError:
        raise InvalidSignature() from None
