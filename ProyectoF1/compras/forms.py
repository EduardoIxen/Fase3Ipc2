from django import forms
from .models import *
import datetime

class Cliente(forms.ModelForm):

    class Meta:
        model = Clienteindividual
        fields = ("cui", "nit", "nombrecompleto", "fechanacimiento", "usuario", "contrasenia")

class loginF(forms.Form):
    usuario = forms.CharField(label="Usuario")
    contrasenia = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    class Meta:
        fields = ('usuario', 'contrasenia')

class consultarProducto(forms.Form):
    #listaProducto = [("Camisa Q150", "Camisa Q150"), ("Pantalon Q125","Pantalon Q125"), ("Zapatos Q200","Zapatos Q200")]
    def __init__(self, listaProductos, *args, **kwargs):
        super(consultarProducto, self).__init__(*args, **kwargs)
        self.fields['producto'] = forms.CharField(widget=forms.Select(choices=listaProductos))
    class Meta:
        fields = ('producto')

class Compra(forms.Form):
    def __init__(self, listaTarjetas, *args, **kwargs):
        super(Compra, self).__init__(*args, **kwargs)
        self.fields['numeroTarjeta'] = forms.CharField(widget=forms.Select(choices=listaTarjetas), label="Tarjeta")
        self.fields['fecha'] = forms.DateField(initial=datetime.date.today(), label='Fecha')
        self.fields['descripcion'] = forms.CharField(required=True, label="Descripcion")
        self.fields['cantidad'] = forms.IntegerField(required=True, label="Cantidad")
