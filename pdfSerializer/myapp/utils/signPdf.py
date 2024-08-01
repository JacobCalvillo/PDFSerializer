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

def decrypt_pdf(encrypted_pdf_data, private_key_pem):
    try:
        # Load the private key
        private_key = serialization.load_pem_private_key(private_key_pem, password=None, backend=default_backend())
        
        # Create a byte stream from the encrypted PDF data
        encrypted_stream = BytesIO(encrypted_pdf_data)

        # Read the encrypted symmetric key
        encrypted_symmetric_key = encrypted_stream.read(256)  # RSA key size; adjust if needed
        
        # Read the IV used for AES
        iv = encrypted_stream.read(16)  # AES block size; adjust if needed
        
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

        # Write the decrypted PDF data to output
        output = BytesIO()
        output.write(decrypted_pdf_data)
        output.seek(0)
        return output.getvalue()

    except Exception as e:
        logger.error(f"Error in decrypt_pdf: {e}")
        return None