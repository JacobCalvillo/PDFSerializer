from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .api import UserViewSet, KeyPairViewSet
from .views import CustomLoginView, RegisterView, HomeView

router = DefaultRouter()
router.register(r'usuarios', UserViewSet)
router.register(r'key-pairs', KeyPairViewSet, basename='keypair')

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('home/', HomeView.as_view(), name='home'),
    path('key-pairs/create/', KeyPairViewSet.as_view({'post': 'create'}), name='keypair-create'),
    path('', include(router.urls)),  # Incluye las URLs del enrutador
]
