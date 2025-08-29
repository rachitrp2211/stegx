# stegx/crypto_utils.py
import os
import base64
from typing import Tuple
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet

_KDF_ITERS = 390000
_SALT_LEN = 16  # bytes

def _derive_key(password: str, salt: bytes) -> bytes:
    """Derive a 32-byte key and return base64 urlsafe key for Fernet."""
    if not isinstance(salt, (bytes, bytearray)):
        raise TypeError("salt must be bytes")
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=_KDF_ITERS,
        backend=default_backend(),
    )
    key = kdf.derive(password.encode("utf-8"))
    return base64.urlsafe_b64encode(key)

def encrypt_bytes(data: bytes, password: str) -> bytes:
    """
    Encrypt raw bytes with password. Returns bytes: salt + token.
    salt is _SALT_LEN bytes prepended to the fernet token.
    """
    salt = os.urandom(_SALT_LEN)
    key = _derive_key(password, salt)
    f = Fernet(key)
    token = f.encrypt(data)
    return salt + token

def decrypt_bytes(salted_token: bytes, password: str) -> bytes:
    """
    Decrypt bytes produced by encrypt_bytes (salt + token).
    Returns plaintext bytes.
    """
    if not isinstance(salted_token, (bytes, bytearray)):
        raise TypeError("Data to decrypt must be bytes")
    if len(salted_token) < _SALT_LEN:
        raise ValueError("Encrypted data too short")
    salt = salted_token[:_SALT_LEN]
    token = salted_token[_SALT_LEN:]
    key = _derive_key(password, salt)
    f = Fernet(key)
    return f.decrypt(token)
