from rest_framework import serializers
from myapp.models import Certificates, DigitalSigns

class CertificatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificates
        fields = '__all__'

class DigitalSignsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DigitalSigns
        fields = '__all__'