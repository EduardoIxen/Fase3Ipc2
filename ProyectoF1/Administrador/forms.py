from django import forms
from .models import *
import datetime

class Cliente(forms.Form):
    cui = forms.IntegerField(required=True, label="CUI")
    nit = forms.IntegerField(required=True, label="NIT")
    nombrecompleto = forms.CharField(required=True, label="Nombre")
    fechanacimiento = forms.DateField(initial=datetime.date.today())
    usuario = forms.CharField(required=True, label="Nombre de usuario")
    contrasenia = forms.CharField(required=True, label="Contraseña")
    class Meta:
        model = Clienteindividual
        fields = ("cui", "nit", "nombrecompleto", "fechanacimiento", "usuario", "contrasenia")


class Empresaa(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ("idtipoempresa", "nombre", "nombrecomercial", "nombrerepresentantelegal", "usuario", "contrasenia")


class CuentaMonetaria(forms.Form):
    codigocuenta = forms.IntegerField(required=True, label="Codigo de la cuenta")
    montopormanejo = forms.DecimalField(required=True, label="Monto por manejo")
    saldo = forms.DecimalField(required=True, label="Saldo")
    lstipoCliente = [(1,"Cliente individual"), (2, "Empresa")]
    tipocliente = forms.CharField(widget=forms.Select(choices=lstipoCliente))
    idcliente = forms.IntegerField(required=True, label="Cui del cliente o ID de la Empresa")

    lista = Moneda.objects.all().values()
    lista2 = []
    for a in lista:
        lista2.append((a.get('codigomoneda'), a.get('nombre')))
    codigomoneda = forms.CharField(widget=forms.Select(choices=lista2))

    class Meta:
        model = Cuentamonetaria
        fields = ('codigocuenta', 'montopormanejo', 'saldo', 'tipocliente', 'idcliente', 'codigomoneda')


class CuentaDeAhorro(forms.Form):
    codigocuenta = forms.IntegerField(required=True, label="Codigo de la cuenta")
    tasainteres = forms.IntegerField(required=True, label="Tasa de interes (%)")
    saldo = forms.DecimalField(required=True, label="Saldo")
    lstipoCliente = [(1,"Cliente individual"), (2, "Empresa")]
    tipocliente = forms.CharField(widget=forms.Select(choices=lstipoCliente))
    idcliente = forms.IntegerField(required=True, label="Cui del cliente o ID de la Empresa")

    lista = Moneda.objects.all().values()
    lista2 = []
    for a in lista:
        lista2.append((a.get('codigomoneda'), a.get('nombre')))
    codigomoneda = forms.CharField(widget=forms.Select(choices=lista2))

    class Meta:
        model = Cuentadeahorro
        fields = ('codigocuenta', 'tasainteres', 'saldo', 'tipocliente', 'idcliente', 'codigomoneda')


class CuentaPlazoFijo(forms.Form):
    codigocuenta = forms.IntegerField(required=True, label="Codigo de la cuenta")
    tasainteres = forms.IntegerField(required=True, label="Tasa de interes (%)")
    periodotiempo = forms.IntegerField(required=True, label="Periodo de tiempo (# meses)")
    saldo = forms.DecimalField(required=True, label="Saldo")
    lstipoCliente = [(1, "Cliente individual"), (2, "Empresa")]
    tipocliente = forms.CharField(widget=forms.Select(choices=lstipoCliente))
    idcliente = forms.IntegerField(required=True, label="Cui del cliente o ID de la Empresa")

    lista = Moneda.objects.all().values()
    lista2 = []
    for a in lista:
        lista2.append((a.get('codigomoneda'), a.get('nombre')))
    codigomoneda = forms.CharField(widget=forms.Select(choices=lista2))

    class Meta:
        model = Cuentaplazofijo
        fields = ('codigocuenta', 'tasainteres', 'periodotiempo', 'saldo', 'tipocliente', 'idcliente', 'codigomoneda')

class Tarjeta(forms.Form):
    numeroTarjeta = forms.IntegerField(required=True, label="Numero de tarjeta")
    #lista = Marca.objects.all().values()
    #lista2 = []
    #for a in lista:
    #    lista2.append((a.get('codigomarca'), a.get('nombre')))
    #marca = forms.CharField(widget=forms.Select(choices=lista2))
    lista3 = Tipodecliente.objects.all().values()
    lista4 = []
    for a in lista3:
        lista4.append((a.get('codigotipocliente'), a.get('nombre')))
    tipoCliente = forms.CharField(widget=forms.Select(choices=lista4), label="Tipo de cliente")
    idCliente = forms.IntegerField(required=True, label="Identificador cliente o empresa")
    #limiteCredito = forms.IntegerField(required=True, label="Limite de credito", min_value=0)
    listaNumTarjetas = ((1, "1"), (2, "2"), (3, "3"))
    cantidadTarjetas = forms.CharField(widget=forms.Select(choices=listaNumTarjetas), label="Numero de tarjeta del cliente (1 - 2 -3)")

    def __init__(self, listaCuenta, listaMarca, listaMoneda, maximo, minimo, moneda, *args, **kwargs):
        super(Tarjeta, self).__init__(*args, **kwargs)
        self.fields['marca'] = forms.CharField(widget=forms.Select(choices=listaMarca))
        self.fields['numeroCuenta'] = forms.CharField(widget=forms.Select(choices=listaCuenta), label="Numero de cuenta")
        self.fields['limiteCredito'] = forms.DecimalField(required=True, label=f"Limite de credito {moneda}{minimo} - {moneda}{maximo}",min_value=minimo ,max_value=maximo, decimal_places=2)
        self.fields['moneda'] = forms.IntegerField(widget=forms.Select(choices=listaMoneda), label="Moneda", )
    class Meta:
        model = Tarjetadecredito
        fields = ('numeroTarjeta', 'marca', 'tipoCLiente', 'idCliente', 'numeroCuenta', 'limiteCredito', 'cantidadTarjetas', 'moneda')

class ConsultarTarjetaClientes(forms.Form):
    idCliente = forms.IntegerField(required=True, label="Codigo del cliente a consultar")
    lista = Marca.objects.all().values()
    lista2 = []
    for a in lista:
        lista2.append((a.get('codigomarca'), a.get('nombre')))
    marca = forms.CharField(widget=forms.Select(choices=lista2), label="Marca deseada")
    lista = Moneda.objects.all().values()
    lista2 = []
    for a in lista:
        lista2.append((a.get('codigomoneda'), a.get('nombre')))
    codigomoneda = forms.CharField(widget=forms.Select(choices=lista2), label="Moneda deseada")
    class Meta:
        fields = ('idCliente', 'marca', 'moneda')