from rest_framework import viewsets
from .models import Certificado, FirmaDigital
from .serializers import CertificadoSerializer, FirmaDigitalSerializer

class CertificadoViewSet(viewsets.ModelViewSet):
    queryset = Certificado.objects.all()
    serializer_class = CertificadoSerializer

class FirmaDigitalViewSet(viewsets.ModelViewSet):
    queryset = FirmaDigital.objects.all()
    serializer_class = FirmaDigitalSerializer
