from django.urls import path
from .views import home
from rest_framework import routers
from .api import CertificadoViewSet, RegistrarSolicitudView

router = routers.DefaultRouter()

router.register('api/certificados', CertificadoViewSet, 'certificados')
router.register('api/solicitudes', RegistrarSolicitudView, 'solicitudes')

urlpatterns = router.urls
