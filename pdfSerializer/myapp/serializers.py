from rest_framework import serializers
from myapp.models import UserCertificate
from django.contrib.auth.models import User
from .models import SignedDocument

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


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCertificate
        fields = ['user', 'certificate_name', 'issued_at', 'valid_until']

class SignedDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignedDocument
        fields = ['user', 'original_file_url', 'signed_file_url', 'created_at']