# views.py
from django.contrib.auth.views import LoginView
from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from django.views import View
from .forms.forms import CustomUserCreationForm


class CustomLoginView(LoginView):
    template_name = 'login.html'

class RegisterView(View):
    def get(self, request, *args, **kwargs):
        form = CustomUserCreationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # Iniciar sesión automáticamente después del registro
            return redirect('home')  # Redirige a la página principal u otra página después del registro
        return render(request, 'register.html', {'form': form})
