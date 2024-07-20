from rest_framework import routers
from django.urls import path, include
from .api import CertificateViewSet, UserViewSet
from .views import CustomLoginView, RegisterView

router = routers.DefaultRouter()

router.register(r'certificados', CertificateViewSet)
router.register(r'usuarios', UserViewSet)

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
]
