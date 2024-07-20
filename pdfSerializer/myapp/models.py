from django.db import models
from django.contrib.auth.models import User
class Certificates(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    certificate_name = models.CharField(max_length=255, null=False)
    url_storage = models.URLField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.certificate_name

class DigitalSigns(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    doc_name = models.CharField(max_length=255, null=False)
    sign_url = models.URLField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return self.doc_name
