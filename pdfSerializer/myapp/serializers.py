from rest_framework import serializers
from myapp.models import UserCertificate, DigitalSign, UserKeyPair
from django.contrib.auth.models import User
from .models import SignedDocument

class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCertificate
        fields = ['id', 'user', 'certificate_name', 'url_storage', 'timestamp']

class DigitalSignSerializer(serializers.ModelSerializer):
    class Meta:
        model = DigitalSign
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username','first_name', 'last_name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class KeyPairSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserKeyPair
        fields = ['user', 'private_key_url', 'public_key_url', 'created_at']

class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCertificate
        fields = ['user', 'certificate_name', 'issued_at', 'valid_until']

class SignedDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignedDocument
        fields = ['user', 'original_file_url', 'signed_file_url', 'created_at']