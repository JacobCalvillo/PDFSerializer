from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import Certificates, DigitalSigns
from .serializers import CertificateSerializer, DigitalSignSerializer, UserSerializer
from .firebase.firebase import bucket
from django.contrib.auth.models import User

class CertificateViewSet(viewsets.ModelViewSet):
    queryset = Certificates.objects.all()
    serializer_class = CertificateSerializer
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden acceder

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'error': 'No autenticado'}, status=status.HTTP_403_FORBIDDEN)

        usuario = request.user
        nombre_certificado = request.data.get('nombre_certificado')
        certificado_file = request.FILES.get('certificado')

        if not certificado_file or not certificado_file.name.endswith('.pem'):
            return Response({'error': 'Archivo inválido. Debe ser un archivo .pem'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            blob = bucket.blob(f'certificados/{usuario.id}/{certificado_file.name}')
            blob.upload_from_file(certificado_file, content_type='application/x-pem-file')

            file_url = blob.public_url

            certificado = Certificates.objects.create(
                user=usuario,  # Debe ser una instancia de User
                certificate_name=nombre_certificado,
                url_storage=file_url
            )
            serializer = self.get_serializer(certificado)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class DigitalSignViewSet(viewsets.ModelViewSet):
    queryset = DigitalSigns.objects.all()
    serializer_class = DigitalSignSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny] 
