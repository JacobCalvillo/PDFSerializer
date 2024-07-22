from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import UserKeyPair, SignedDocument
from .serializers import UserSerializer, KeyPairSerializer, SignedDocumentSerializer
from django.contrib.auth.models import User
from .utils.crypto import generate_user_key_pair
from .models import UserKeyPair
from django.conf import settings


class KeyPairViewSet(viewsets.ViewSet):
    queryset = UserKeyPair.objects.all()
    serializer_class = KeyPairSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'User must be logged in'}, status=status.HTTP_403_FORBIDDEN)

        user = request.user
        # Delete existing key pairs if they exist
        UserKeyPair.objects.filter(user=user).delete()

        # Generate new key pairs
        private_key_url, public_key_url = generate_user_key_pair(user.id, settings.SECRET_KEY)

        # Create a new entry in the database for the new key pairs
        key_pair = UserKeyPair.objects.create(
            user=user,
            private_key_url=private_key_url,
            public_key_url=public_key_url
        )
        # Serialize and return the response
        serializer = KeyPairSerializer(key_pair)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        

class SignedDocumentViewSet(viewsets.ModelViewSet):
    queryset = SignedDocument.objects.all()
    serializer_class = SignedDocumentSerializer
    permission_classes = [IsAuthenticated]

    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny] 



