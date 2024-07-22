from django.db import models
from django.contrib.auth.models import User
class UserCertificate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    certificate_name = models.CharField(max_length=255, null=False)
    url_storage = models.URLField()
    issued_at = models.DateTimeField(auto_now_add=True)
    valid_until = models.DateTimeField()
    certificate_type = models.CharField(max_length=50, default='user')  # 'user', 'ca', etc.

    def __str__(self):
        return self.certificate_name

class DigitalSign(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    doc_name = models.CharField(max_length=255, null=False)
    sign_url = models.URLField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.doc_name

class UserKeyPair(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    private_key_url = models.TextField()# Aumenta el tamaño del campo
    public_key_url = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'KeyPair for {self.user.username}'

class SignedDocument(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_file_url = models.URLField()  # URL del archivo PDF original
    signed_file_url = models.URLField()    # URL del archivo PDF firmado
    created_at = models.DateTimeField(auto_now_add=True)
