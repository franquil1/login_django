from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import RegistroUsuarioForms, LoginForm


def mostrarHome(request):
    return render(request, 'html/home.html')

def mostrarComunidad(request):
    return render(request, 'html/comunidad.html')


def mostrarRutas(request):
    return render(request, 'html/rutas.html')

def mostrarJuegos(request):
    return render(request, 'html/juegos/juegos.html')

def mostrarRanking(request):
    return render(request, 'html/ranking.html')


def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForms(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.contraseña = make_password(form.cleaned_data['contraseña'])
            usuario.save()

            try:
                user_django = User.objects.create_user(
                    username=form.cleaned_data['nombre_usuario'],
                    email=form.cleaned_data['correo_electronico'],
                    password=form.cleaned_data['contraseña']
                )
                user_django.save()
            except Exception as e:
                messages.error(request, f'Error al crear usuario de autenticación: {e}')
                print(f"Error al crear usuario de autenticación: {e}")
                return render(request, 'mi_app_registro/registro.html', {'form': form})

            messages.success(request, '¡Cuenta creada exitosamente! Por favor, inicia sesión.')
            return redirect('mi_app_registro:login')
    else:
        form = RegistroUsuarioForms()

    return render(request, 'mi_app_registro/registro.html', {'form': form})

def registro_exitoso(request):
    return render(request, 'mi_app_registro/registro_exitoso.html')


def login_usuario(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'¡Bienvenido de nuevo, {username}!')
                return redirect('mi_app_registro:mi_pagina')
            else:
                messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
    else:
        form = LoginForm()

    return render(request, 'mi_app_registro/login.html', {'form': form})

def mi_pagina(request):
    if request.user.is_authenticated:
        return render(request, 'mi_app_registro/mi_pagina.html', {'username': request.user.username})
    else:
        messages.warning(request, 'Debes iniciar sesión para acceder a esta página.')
        return redirect('mi_app_registro:login')

def logout_usuario(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente.')
    return redirect('mi_app_registro:login')