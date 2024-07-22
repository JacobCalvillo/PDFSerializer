# views.py
from django.contrib.auth.views import LoginView
from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from django.views import View
from .forms.forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from firebase_admin import auth as firebase_auth
from firebase_admin.exceptions import FirebaseError
from .models import UserKeyPair, UserCertificate
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponse 
import requests
from django.contrib.auth.mixins import LoginRequiredMixin


class UploadDocumentView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'upload_document.html')
    
class SignedDocumentView(View):
    def get(self, request, *args, **kwargs):
        signed_document_url = request.GET.get('signed_document_url')
        if signed_document_url:
            return render(request, 'signed_document.html', {'signed_document_url': signed_document_url})
        return render(request, 'error.html', {'error': 'No signed document URL provided'})

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        key_pair = UserKeyPair.objects.filter(user=user).first()
        
        if key_pair:
            context['private_key_url'] = key_pair.private_key_url
            context['public_key_url'] = key_pair.public_key_url
            context['keypair_exists'] = True
        else:
            context['keypair_exists'] = False

        return context

class CustomLoginView(LoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('home')  # Redirige a 'home' después del inicio de sesión

    def get_success_url(self):
        return self.success_url

class RegisterView(View):
    def get(self, request, *args, **kwargs):
        form = CustomUserCreationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # Iniciar sesión automáticamente después del registro

            # Registrar en Firebase
            try:
                firebase_user = firebase_auth.create_user(
                    email=user.email,
                    password=user.password,  # Asegúrate de tener el password en el formulario
                    display_name=user.username
                )
                print(f'Usuario registrado en Firebase: {firebase_user.uid}')
            except FirebaseError as e:
                print(f'Error al registrar en Firebase: {str(e)}')
                # Manejo de errores adicional aquí

            return redirect('home')  # Redirige a la página principal u otra página después del registro
        return render(request, 'register.html', {'form': form})


@login_required
def download_key(request, key_id):
    key_pair = get_object_or_404(UserKeyPair, id=key_id, user=request.user)
    try:
        response = requests.get(key_pair.private_key_url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
    except requests.RequestException as e:
        return HttpResponse(f"Error downloading file: {e}", status=500)

    # Return the file as an HTTP response
    response = HttpResponse(response.content, content_type='application/x-pem-file')
    response['Content-Disposition'] = f'attachment; filename={key_pair.private_key_url.split("/")[-1]}'
    return response

