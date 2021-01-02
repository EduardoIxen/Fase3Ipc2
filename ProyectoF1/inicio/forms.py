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


class RegistroPlanilla(forms.Form):
    nombre = forms.CharField(required=True, label="Nombre de la planilla")
    class Meta:
        fields = ('nombre')


class IngresoUsuarioPlanilla(forms.Form):
    def __init__(self, listaPlanillas, *args, **kwargs):
        super(IngresoUsuarioPlanilla, self).__init__(*args, **kwargs)
        self.fields['planilla'] = forms.CharField(widget=forms.Select(choices=listaPlanillas))
    numeroCuentaEmpleado = forms.IntegerField(required=True, label="Numero de cuenta")
    nombre = forms.CharField(required=True, label="Nombre")
    sueldo = forms.DecimalField(required=True, label="Sueldo")
    listaFormaPago = []
    listaFormaPago.append(("Mensual", "Mensual"))
    listaFormaPago.append(("Quincenal", "Quincenal"))
    formaPago = forms.CharField(widget=forms.Select(choices=listaFormaPago))

    class Meta:
        model = Detalleplanilla;
        fields = ('nombreCuentaEmpleado', 'nombre', 'sueldo', 'formaPago', 'planilla')


class ConsultaPlanilla(forms.Form):
    def __init__(self, listaPlanillas, *args, **kwargs):
        super(ConsultaPlanilla, self).__init__(*args, **kwargs)
        self.fields['planilla'] = forms.CharField(widget=forms.Select(choices=listaPlanillas))

    class Meta:
        fields = ('planilla')

class SolicitudPrestamo(forms.Form):
    def __init__(self, listaCuentas, *args, **kwargs):
        super(SolicitudPrestamo, self).__init__(*args, **kwargs)
        self.fields['cuenta'] = forms.CharField(widget=forms.Select(choices=listaCuentas))
    descripcion = forms.CharField(widget=forms.Textarea, required=True, label="Descripcion")
    montoSolicitado = forms.DecimalField(required=True, label="Monto solicitado", decimal_places=2)
    listaTiempo = []
    listaTiempo.append(("12 meses", "12 meses"))
    listaTiempo.append(("24 meses", "24 meses"))
    listaTiempo.append(("36 meses", "36 meses"))
    listaTiempo.append(("48 meses", "48 meses"))
    tiempoEnDevolver = forms.CharField(widget=forms.Select(choices=listaTiempo), label="Tiempo en que se cancelará el pago")

    class Meta:
        fields = ('cuenta', 'descripcion', 'montoSolicitado', 'moneda', 'tiempoEnDevolver')


class consultarCuenta(forms.Form):
    def __init__(self, listaCuentas, *args, **kwargs):
        super(consultarCuenta, self).__init__(*args, **kwargs)
        self.fields['cuenta'] = forms.CharField(widget=forms.Select(choices=listaCuentas), label="Cuentas")
    class Meta:
        fields = ('cuenta')