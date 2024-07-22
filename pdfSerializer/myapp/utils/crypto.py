import datetime
from cryptography import x509
from cryptography.x509 import CertificateBuilder, BasicConstraints, SubjectAlternativeName, DNSName
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.x509.oid import NameOID
from .storage import upload_to_firebase, get_download_url


def generate_user_key_pair(user_id, password):
    """Genera un par de claves RSA y sube las claves a Firebase, luego devuelve las URLs de descarga firmadas."""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(password.encode('utf-8'))
    )

    public_key_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Subir claves a Firebase y obtener los nombres de los blobs
    private_key_blob_name = upload_to_firebase(user_id, private_key_pem, 'private_key.pem', 'application/x-pem-file')
    public_key_blob_name = upload_to_firebase(user_id, public_key_pem, 'public_key.pem', 'application/x-pem-file')

    # Generar URLs de descarga firmadas
    private_key_url = get_download_url(private_key_blob_name)
    public_key_url = get_download_url(public_key_blob_name)

    return private_key_url, public_key_url

