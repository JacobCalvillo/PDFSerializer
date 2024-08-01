from ..firebase.firebase import bucket  # Asegúrate de tener configurado Firebase
import logging
import datetime
from google.auth.exceptions import GoogleAuthError

logger = logging.getLogger(__name__)

def upload_to_firebase(user_id, file_data, file_name, content_type):
    try:
        blob = bucket.blob(f'{user_id}/{file_name}')
        blob.upload_from_string(file_data, content_type=content_type)
        blob.make_public()
        return blob.name
    except Exception as e:
        print(f"Error in upload_to_firebase: {e}")
        return None

def get_download_url(file_path):
    """Genera una URL de descarga firmada para un archivo en Firebase Storage."""
    blob = bucket.blob(file_path)

    try:
        # Obtener la URL de descarga firmada
        url = blob.generate_signed_url(
            version='v4',
            expiration=datetime.timedelta(minutes=10),  # Adjust the expiration as needed
            method='GET'
        )
        return url
    except GoogleAuthError as e:
        logger.error(f'Error de autenticación: {e}')
        return None
    except Exception as e:
        logger.error(f'Error: {e}')
        return None


def get_files_from_firebase(user_id):
    files = []
    blobs = bucket.list_blobs(prefix=f'{user_id}/')
    for blob in blobs:
        file_info = {
            'name': blob.name,
            'download_url': blob.generate_signed_url(
                version='v4',
                expiration=datetime.timedelta(minutes=10),  # Adjust the expiration as needed
                method='GET'
            )
        }
        files.append(file_info)
    return files

def download_from_firebase(user_id, file_name):
    file_path = f'{user_id}/{file_name}'
    blob = bucket.blob(file_path)
    
    try:
        logger.info(f"Attempting to download file from Firebase: {file_path}")
        return blob.download_as_bytes()
    except Exception as e:
        logger.error(f"Error downloading from Firebase: {e}")
        return None
