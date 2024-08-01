from django.db import models
from django.contrib.auth.models import User
class EncryptedFile(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_files')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_files')
    file_name = models.CharField(max_length=255)
    encrypted_file = models.BinaryField()  # Guarda el archivo encriptado como blob binario
    private_key = models.TextField()  # Guarda la clave privada en formato PEM como texto
    created_at = models.DateTimeField(auto_now_add=True)