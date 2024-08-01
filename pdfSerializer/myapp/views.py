# views.py
from django.contrib.auth.views import LoginView
from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from .forms.forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from firebase_admin import auth as firebase_auth
from firebase_admin.exceptions import FirebaseError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from myapp.models import EncryptedFile
from myapp.utils.signPdf import encrypt_pdf,decrypt_pdf
from myapp.forms.forms import PDFUploadFormEncrypt
from django.http import HttpResponse 
from myapp.firebase.firebase import bucket
from io import BytesIO
from myapp.utils.crypto import generate_rsa_keys,load_public_key, load_private_key
import zipfile
import logging

logger = logging.getLogger(__name__)

class KeyPairView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'keypairs.html')

    def post(self, request):
        try:
            # Generate keys
            private_key_pem, public_key_pem = generate_rsa_keys()

            # Create a zip file in memory
            zip_buffer = BytesIO()
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
            return redirect('generate_keys')  # Ensure this matches the URL name
        
class PDFEncryptView(View):
    def get(self, request, *args, **kwargs):
        form = PDFUploadFormEncrypt()
        users = User.objects.all()
        return render(request, 'signPDF.html', {'form': form, 'users': users})

    def post(self, request, *args, **kwargs):
        form = PDFUploadFormEncrypt(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = request.FILES.get('pdf')
            public_key_file = request.FILES.get('public_key')
            recipient_id = request.POST.get('recipient')
            private_key_file = request.FILES.get('private_key')

            try:
                # Load the public key
                public_key = load_public_key(public_key_file)
                if not public_key:
                    messages.error(request, "Failed to load public key.")
                    return render(request, 'signPDF.html', {'form': form, 'users': User.objects.all()})

                # Encrypt the PDF
                encrypted_pdf = encrypt_pdf(pdf_file, public_key)
                if not encrypted_pdf:
                    messages.error(request, "Failed to encrypt the PDF.")
                    return render(request, 'signPDF.html', {'form': form, 'users': User.objects.all()})

                # Load the private key
                private_key_pem = private_key_file.read().decode('utf-8')

                # Save to database
                EncryptedFile.objects.create(
                    sender=request.user,
                    receiver_id=recipient_id,  # Use receiver_id instead of receiver for ForeignKey
                    file_name=pdf_file.name,
                    encrypted_file=encrypted_pdf,
                    private_key=private_key_pem  # Save the private key in PEM format
                )

                # Provide feedback to the user
                messages.success(request, "PDF encrypted and saved to database.")

                # Return the encrypted PDF as a response
                response = HttpResponse(encrypted_pdf, content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="{pdf_file.name}"'
                return response

            except Exception as e:
                logger.error(f"An error occurred: {e}")
                messages.error(request, f"An error occurred: {e}")
        
        else:
            messages.error(request, "Invalid form submission.")
        
        users = User.objects.all()
        return render(request, 'signPDF.html', {'form': form, 'users': users})

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'signPDF.html'
    login_url = 'login'
    redirect_field_name = 'next'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()  # Añade la lista de usuarios al contexto
        return context


class CustomLoginView(LoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('home')  # Redirige a 'home' después del inicio de sesión

    def form_valid(self, form):
        # Llama al método base para autenticar al usuario en Django
        response = super().form_valid(form)

        user = form.get_user()
        # Autenticación en Firebase
        try:
            # Autenticación con Firebase
            firebase_user = firebase_auth.get_user_by_email(user.email)
            print(f'Usuario autenticado en Firebase: {firebase_user.uid}')
        except FirebaseError as e:
            print(f'Error al autenticar en Firebase: {str(e)}')
            messages.error(self.request, f'Error authenticating with Firebase: {str(e)}')

        # Autenticación en Django
        auth_login(self.request, user)
        return response

    def get_success_url(self):
        return self.success_url
    
    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password.")
        return super().form_invalid(form)


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        form = CustomUserCreationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)

            # Register in Firebase
            try:
                firebase_user = firebase_auth.create_user(
                    email=user.email,
                    password=form.cleaned_data.get('password1'),  # Ensure password is retrieved correctly
                    display_name=user.username
                )
                print(f'Usuario registrado en Firebase: {firebase_user.uid}')
            except FirebaseError as e:
                print(f'Error al registrar en Firebase: {str(e)}')
                messages.error(request, f'Error registering in Firebase: {str(e)}')

            messages.success(request, 'Registration successful!')
            return redirect('home')
        else:
            for error in form.errors.values():
                messages.error(request, error)
        return render(request, 'register.html', {'form': form})

class ListFilesView(View):
    def get(self, request):
        user_id = request.user.id
        try:
            blobs = bucket.list_blobs(prefix=f'{user_id}/')
            files = [blob.name for blob in blobs]
        except Exception as e:
            logger.error(f"Error retrieving files: {e}")
            files = []

        return render(request, 'list_files.html', {'files': files})

class PDFDecryptView(View):
    def get(self, request):
        # Retrieve user files from the database
        user_files = EncryptedFile.objects.filter(receiver=request.user)
        return render(request, 'decrypt.html', {'files': user_files})

    def post(self, request):
        file_id = request.POST.get('file')

        if not file_id:
            messages.error(request, "File selection is required.")
            user_files = EncryptedFile.objects.filter(receiver=request.user)
            return render(request, 'decrypt.html', {'files': user_files})

        try:
            # Retrieve the encrypted PDF file and associated private key from the database
            try:
                encrypted_file_record = EncryptedFile.objects.get(id=file_id, receiver=request.user)
                encrypted_pdf = encrypted_file_record.encrypted_file
                private_key_pem = encrypted_file_record.private_key
            except EncryptedFile.DoesNotExist:
                messages.error(request, "File not found.")
                user_files = EncryptedFile.objects.filter(receiver=request.user)
                return render(request, 'decrypt.html', {'files': user_files})

            # Load the private key
            private_key = load_private_key(private_key_pem)
            if not private_key:
                messages.error(request, "Failed to load private key.")
                user_files = EncryptedFile.objects.filter(receiver=request.user)
                return render(request, 'decrypt.html', {'files': user_files})

            # Decrypt the PDF
            decrypted_pdf = decrypt_pdf(encrypted_pdf, private_key)
            if not decrypted_pdf:
                messages.error(request, "Failed to decrypt the PDF.")
                user_files = EncryptedFile.objects.filter(receiver=request.user)
                return render(request, 'decrypt.html', {'files': user_files})

            # Provide feedback to the user
            messages.success(request, "PDF decrypted successfully.")

            # Return the decrypted PDF as a response
            response = HttpResponse(decrypted_pdf, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="decrypted_{file_id}.pdf"'
            return response

        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            user_files = EncryptedFile.objects.filter(receiver=request.user)
            return render(request, 'decrypt.html', {'files': user_files})

        

