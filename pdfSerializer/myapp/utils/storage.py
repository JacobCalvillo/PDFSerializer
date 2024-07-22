from ..firebase.firebase import bucket  # Asegúrate de tener configurado Firebase
import logging
import datetime
from google.auth.exceptions import GoogleAuthError

logger = logging.getLogger(__name__)

def upload_to_firebase(user_id, file_data, file_name, content_type):
    """Sube un archivo al bucket de Firebase Storage."""
    blob = bucket.blob(f'{user_id}/{file_name}')
    
    # Subir el archivo desde una cadena (en bytes)
    blob.upload_from_string(file_data, content_type=content_type)
    
    logger.info(f'Uploaded file {file_name} for user {user_id}')
    
    # No se devuelve la URL pública aquí
    return blob.name  # Devolvemos el nombre del blob para usarlo en la generación de URL


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

