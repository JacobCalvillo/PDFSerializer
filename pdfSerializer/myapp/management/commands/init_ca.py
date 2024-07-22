from django.core.management.base import BaseCommand
from myapp.utils.crypto import create_ca  # Ajusta el import a la ubicación de tu función `create_ca`
from django.conf import settings

class Command(BaseCommand):
    help = 'Genera el certificado de la CA al iniciar la aplicación'

    def handle(self, *args, **kwargs):
        password = settings.CA_PASSWORD  # Obtén la contraseña de la CA desde la configuración
        private_key_fn = settings.CA_PRIVATE_KEY_PATH
        certificate_fn = settings.CA_CERTIFICATE_PATH

        create_ca(password, private_key_fn, certificate_fn)
        self.stdout.write(self.style.SUCCESS('Certificado de la CA generado con éxito.'))