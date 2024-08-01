from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from rest_framework.routers import DefaultRouter
from .api import UserViewSet
from .views import CustomLoginView, RegisterView, HomeView, PDFEncryptView, KeyPairView, PDFDecryptView

router = DefaultRouter()
router.register(r'usuarios', UserViewSet)

urlpatterns = [
    path('', lambda request: redirect('login')),  # Redirect root URL to login page
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('home/', HomeView.as_view(), name='home'),
    path('home/sign-pdf/', PDFEncryptView.as_view(), name='sign-pdf'),
    path('generate-keys/', KeyPairView.as_view(), name='pairs'),  # Updated URL name
    path("home/decrypt", PDFDecryptView.as_view(), name="decrypt"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', include(router.urls)),  # Include the URLs from the router
]
