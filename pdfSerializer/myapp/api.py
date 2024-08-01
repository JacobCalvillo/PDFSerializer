from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import SignedDocument
from .serializers import UserSerializer, SignedDocumentSerializer
from django.contrib.auth.models import User

class SignedDocumentViewSet(viewsets.ModelViewSet):
    queryset = SignedDocument.objects.all()
    serializer_class = SignedDocumentSerializer
    permission_classes = [IsAuthenticated]

    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny] 



