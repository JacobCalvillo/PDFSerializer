# urls.py
from django.urls import path, include
from django.shortcuts import redirect
from rest_framework.routers import DefaultRouter
from .api import UserViewSet, KeyPairViewSet
from .views import CustomLoginView, RegisterView, HomeView, PdfSignView

router = DefaultRouter()
router.register(r'usuarios', UserViewSet)
router.register(r'key-pairs', KeyPairViewSet, basename='keypair')

urlpatterns = [
    path('', lambda request: redirect('login')),  # Redirect root URL to login page
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('home/', HomeView.as_view(), name='home'),
    path('home/sign-pdf/', PdfSignView.as_view(), name='sign-pdf'),  # Ensure this matches
    path('generate-keys/', KeyPairViewSet.as_view({'post': 'create'}), name='generate_keys'),
    path('key-pair-password-form/', KeyPairViewSet.as_view({'get': 'create'}), name='key_pair_password_form'),
    path('', include(router.urls)),  # Include the URLs from the router
]
