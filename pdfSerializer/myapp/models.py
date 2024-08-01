from django.db import models
from django.contrib.auth.models import User

class SignedDocument(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_file_url = models.URLField()  # URL del archivo PDF original
    encrypted_file = models.BinaryField(blank=False)  # Archivo encriptado como blob
    created_at = models.DateTimeField(auto_now_add=True)
