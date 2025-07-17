from django.urls import path
from . import views

app_name = 'mi_app_registro' # Define un nombre para el namespace de la app

urlpatterns = [
    path('registro/', views.registro_usuario, name='registro'),
    path('registro/exito/', views.registro_exitoso, name='registro_exitoso'),
    path('login/', views.login_usuario, name='login')
]