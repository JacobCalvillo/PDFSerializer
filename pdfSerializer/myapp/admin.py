from django.contrib import admin
from .models import UserCertificate, DigitalSign, UserKeyPair

admin.site.register(UserCertificate)
admin.site.register(DigitalSign)
admin.site.register(UserKeyPair)
