# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class PDFUploadFormEncrypt(forms.Form):
    pdf = forms.FileField(label="PDF Document")
    public_key = forms.FileField(label="Public Key")
    recipient = forms.ModelChoiceField(
        queryset=User.objects.all(),  # Obtén todos los usuarios en la base de datos
        label="Recipient",
        required=True,
        help_text="Select the user who will receive the encrypted file."
    )

class PDFUploadFormDecrypt(forms.Form):
    pdf = forms.FileField(label="PDF Document")
    private_key = forms.FileField(label='Private Key')
