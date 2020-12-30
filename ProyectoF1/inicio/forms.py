from django import forms
from .models import *

class Cliente(forms.ModelForm):

    class Meta:
        model = Clienteindividual
        fields = ("cui", "nit", "nombrecompleto", "fechanacimiento", "usuario", "contrasenia")

class consultarTarjeta(forms.Form):
    def __init__(self, listaCuentas, *args, **kwargs):
        super(consultarTarjeta, self).__init__(*args, **kwargs)
        self.fields['numeroTarjeta'] = forms.CharField(widget=forms.Select(choices=listaCuentas))
    class Meta:
        fields = ('numeroTarjeta')