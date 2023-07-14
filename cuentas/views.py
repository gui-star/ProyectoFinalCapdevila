from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from django.contrib.auth import logout as auth_logout

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Crear un perfil para el usuario
            Profile.objects.create(user=user)
            auth_login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('cuentas:profile')
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

@login_required
def profile(request):
    user = request.user
    profile = user.profile # Acceder al campo avatar en lugar de profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            print("Perfil guardado:", profile)
            messages.success(request, 'Perfil actualizado con éxito')
            return redirect('cuentas:profile')
        else:
            messages.error(request, 'Error en el formulario')
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'perfil.html', {'profile': profile, 'form': form})

def logout(request):
    auth_logout(request)
    return redirect('home')

@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado con éxito')
            return redirect('cuentas:profile')
        else:
            messages.error(request, 'Error en el formulario')
    else:
        form = ProfileForm(instance=user.profile)

    return render(request, 'editar_perfil.html', {'form': form})

