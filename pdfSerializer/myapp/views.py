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
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from myapp.utils.storage import upload_to_firebase
from myapp.utils.signPdf import sign_pdf
from myapp.forms.forms import PDFUploadForm
from django.http import HttpResponse 
from myapp.utils.crypto import load_private_key

class PdfSignView(View):
    def get(self, request, *args, **kwargs):
        form = PDFUploadForm()
        return render(request, 'home.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = request.FILES.get('pdf')
            private_key_file = request.FILES.get('private_key')

            if not pdf_file or not private_key_file:
                messages.error(request, "Both PDF file and private key must be provided.")
                return render(request, 'home.html', {'form': form})
            
            try:
                # Load and decrypt the private key
                private_key = load_private_key(private_key_file)
                
                # Sign the PDF
                signed_pdf = sign_pdf(pdf_file, private_key)

                # Upload to Firebase
                user_id = request.user.id
                file_name = 'signed_document.pdf'
                content_type = 'application/pdf'
                file_data = signed_pdf.getvalue()

                # Call the function to upload the signed PDF to Firebase
                blob_name = upload_to_firebase(user_id, file_data, file_name, content_type)

                # Provide feedback to the user
                messages.success(request, f"PDF signed and uploaded to Firebase. Blob name: {blob_name}")

                # Return the signed PDF as a response
                response = HttpResponse(signed_pdf, content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="{file_name}"'
                return response

            except Exception as e:
                messages.error(request, f"An error occurred: {e}")
        
        else:
            messages.error(request, "Invalid form submission.")
        
        return render(request, 'home.html', {'form': form})
    
class SignedDocumentView(View):
    def get(self, request, *args, **kwargs):
        signed_document_url = request.GET.get('signed_document_url')
        if signed_document_url:
            return render(request, 'signed_document.html', {'signed_document_url': signed_document_url})
        return render(request, 'error.html', {'error': 'No signed document URL provided'})

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'
    login_url = 'login'
    redirect_field_name = 'next'


class CustomLoginView(LoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('home')  # Redirige a 'home' después del inicio de sesión

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




