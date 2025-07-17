from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password # Para hashear contraseñas
from .forms import RegistroUsuarioForms
from django.contrib import messages

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
# Create your views here.

# funciones para el registro de usuario
def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForms(request.POST)
        if form.is_valid():
            # Paso 1: Guardar el usuario en tu modelo personalizado 'Usuario'
            usuario = form.save(commit=False)
            # Hashear la contraseña antes de guardarla en tu modelo
            usuario.contraseña = make_password(form.cleaned_data['contraseña'])
            usuario.save()

            # Paso 2: Crear un usuario en el sistema de autenticación de Django
            # Esto es crucial para poder usar las funciones de login de Django
            try:
                user_django = User.objects.create_user(
                    username=form.cleaned_data['nombre_usuario'],
                    email=form.cleaned_data['correo_electronico'],
                    password=form.cleaned_data['contraseña'] # Django se encargará de hashear esta contraseña
                )
                user_django.save()
            except Exception as e:
                # Si hay un error al crear el usuario de Django (ej. nombre de usuario ya existe)
                messages.error(request, f'Error al crear usuario de autenticación: {e}')
                print(f"Error al crear usuario de autenticación: {e}")
                # Puedes decidir qué hacer aquí:
                # 1. Eliminar el usuario de tu modelo si el de Django falla: usuario.delete()
                # 2. Redirigir de nuevo al formulario de registro con un error más específico.
                return render(request, 'mi_app_registro/registro.html', {'form': form})


            # Paso 3: Añadir un mensaje de éxito
            messages.success(request, '¡Cuenta creada exitosamente! Por favor, inicia sesión.')

            # Paso 4: Redirigir al usuario a la página de login
            # Asegúrate de que 'login' sea el 'name' de la URL de tu página de login
            return redirect('Aplicacion:login') # Asumiendo que tu app se llama 'Aplicacion' y la URL de login se llama 'login'
        # Si el formulario NO es válido, el código CONTINÚA a la línea 'return render' de abajo
        # para mostrar el formulario con los errores.
    else:
        # Si la solicitud es GET (carga inicial del formulario),
        # crea un formulario vacío.
        form = RegistroUsuarioForms()

    # Esta línea se ejecutará si es un GET o si el POST no fue válido
    return render(request, 'mi_app_registro/registro.html', {'form': form})

def registro_exitoso(request):
    # Esta vista ya no será necesaria si redirigimos directamente al login
    # Pero la mantengo por si la usas en otro lugar.
    return render(request, 'mi_app_registro/registro_exitoso.html')

# Nueva función para la página de login (la crearemos más adelante)
def login_usuario(request):
    # Por ahora, solo un placeholder
    return render(request, 'mi_app_registro/login.html')