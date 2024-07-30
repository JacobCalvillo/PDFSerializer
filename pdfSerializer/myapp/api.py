from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import SignedDocument
from .serializers import UserSerializer, SignedDocumentSerializer
from django.contrib.auth.models import User
from .utils.crypto import generate_user_key_pair
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
import zipfile
import io
from myapp.utils.crypto import generate_user_key_pair
from myapp.forms.passwordform import PasswordForm

class KeyPairViewSet(LoginRequiredMixin, viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        if request.method == 'POST':
            password_form = PasswordForm(request.POST)
            if password_form.is_valid():
                # Get the password from the form
                password = password_form.cleaned_data['password']
                
                try:
                    # Generate keys with the provided password
                    private_key_pem, public_key_pem = generate_user_key_pair(password)

                    # Create a zip file in memory
                    zip_buffer = io.BytesIO()
                    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
                        zip_file.writestr('private_key.pem', private_key_pem)
                        zip_file.writestr('public_key.pem', public_key_pem)

                    zip_buffer.seek(0)

                    # Respond with the zip file for download
                    response = HttpResponse(zip_buffer, content_type='application/zip')
                    response['Content-Disposition'] = 'attachment; filename=key_pair.zip'

                    messages.success(request, "Se han generado las claves.")
                    return response

                except Exception as e:
                    messages.error(request, f"Error al generar las claves: {str(e)}")
                    return Response({'error': 'Error al generar las claves'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                messages.error(request, "Formulario de contraseña inválido.")
                return redirect('key_pair_password_form')

        # If GET request, show the password form
        else:
            password_form = PasswordForm()
            return render(request, 'home.html', {'form': password_form})

class SignedDocumentViewSet(viewsets.ModelViewSet):
    queryset = SignedDocument.objects.all()
    serializer_class = SignedDocumentSerializer
    permission_classes = [IsAuthenticated]

    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny] 



