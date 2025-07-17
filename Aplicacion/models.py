from django.db import models

# Create your models here.

class Usuario(models.Model):
    nombre_usuario = models.CharField(max_length=100, unique=True)
    correo_electronico = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=128)

    def __str__(self):
        return self.nombre_usuario