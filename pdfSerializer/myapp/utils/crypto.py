from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

import logging

logger = logging.getLogger(__name__)

def generate_rsa_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()

    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode('utf-8')

    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode('utf-8')

    return private_key_pem, public_key_pem

def load_public_key(file):
    try:
        public_key_pem = file.read()
        public_key = serialization.load_pem_public_key(public_key_pem, backend=default_backend())
        return public_key
    except Exception as e:
        logger.error(f"Error loading public key: {e}")
        return None
    
def load_private_key(private_key_pem):
    try:
        private_key_bytes = private_key_pem.encode('utf-8')
        private_key = serialization.load_pem_private_key(
            private_key_bytes,
            password=None,
            backend=default_backend()
        )
        return private_key
    except Exception as e:
        logger.error(f"Error loading private key: {e}")
        return None