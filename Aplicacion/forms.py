from django import forms
from .models import Usuario

class RegistroUsuarioForms(forms.ModelForm):
    contraseña2 = forms.CharField(label = 'Confirmar contraseña', widget= forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ['nombre_usuario', 'correo_electronico', 'contraseña']
        widgets = {
            'constraseña': forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        contraseña = cleaned_data.get('contraseña')
        contraseña2 = cleaned_data.get('contraseña2')

        if contraseña and contraseña2 and contraseña != contraseña2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data