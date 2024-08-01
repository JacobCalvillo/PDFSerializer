from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from PyPDF2 import PdfReader, PdfWriter
import logging
from io import BytesIO
import os

logger = logging.getLogger(__name__)

def encrypt_pdf(input_pdf_file, public_key):
    try:
        # Read and prepare the PDF file
        reader = PdfReader(input_pdf_file)
        writer = PdfWriter()

        for page_num in range(len(reader.pages)):
            writer.add_page(reader.pages[page_num])

        # Write the PDF to a byte stream
        pdf_buffer = BytesIO()
        writer.write(pdf_buffer)
        pdf_data = pdf_buffer.getvalue()

        # Generate a symmetric key for AES encryption
        symmetric_key = os.urandom(32)  # AES-256 key
        iv = os.urandom(16)  # Initialization vector

        # Encrypt the PDF data with AES
        cipher = Cipher(algorithms.AES(symmetric_key), modes.CFB(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted_pdf_data = encryptor.update(pdf_data) + encryptor.finalize()

        # Encrypt the symmetric key with the public key
        encrypted_symmetric_key = public_key.encrypt(
            symmetric_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # Write encrypted symmetric key and encrypted data to output
        output = BytesIO()
        output.write(encrypted_symmetric_key)
        output.write(iv)  # Include the IV used for AES encryption
        output.write(encrypted_pdf_data)
        output.seek(0)
        return output.getvalue()

    except Exception as e:
        logger.error(f"Error in encrypt_pdf: {e}")
        return None


def decrypt_pdf(encrypted_pdf_data, private_key):
    try:
        # Create a byte stream from the encrypted PDF data
        encrypted_stream = BytesIO(encrypted_pdf_data)
        print(1)
        # Read the encrypted symmetric key (adjust size as necessary)
        encrypted_symmetric_key = encrypted_stream.read(256)  # Example size for a 2048-bit RSA key
        
        # Read the IV used for AES (16 bytes for AES)
        iv = encrypted_stream.read(16)
        
        # Read the encrypted PDF data
        encrypted_pdf_data = encrypted_stream.read()
        
        # Decrypt the symmetric key with the private key
        symmetric_key = private_key.decrypt(
            encrypted_symmetric_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # Decrypt the PDF data with AES
        cipher = Cipher(algorithms.AES(symmetric_key), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_pdf_data = decryptor.update(encrypted_pdf_data) + decryptor.finalize()

        return decrypted_pdf_data

    except Exception as e:
        logger.error(f"Error in decrypt_pdf: {e}")
        return None