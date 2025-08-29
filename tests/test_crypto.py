import pytest
from stegx import crypto_utils

def test_encrypt_decrypt_bytes():
    password = "testpass"
    data = b"secret data"
    
    encrypted = crypto_utils.encrypt_bytes(data, password)
    assert encrypted != data  # should be encrypted
    
    decrypted = crypto_utils.decrypt_bytes(encrypted, password)
    assert decrypted == data
