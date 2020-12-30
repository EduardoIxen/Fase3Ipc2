from django.shortcuts import render, redirect
from .forms import *
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def login(request):
    mensaje = ""
    variables = {
        'mensaje': mensaje,
        'usuariologueado': ''
    }
    if request.method == "POST":
        usuario = request.POST['usuariolog']
        password = request.POST['passwordlog']
        print(f"{usuario}, {password}")
        usuarioLogueado = Clienteindividual.objects.filter(usuario=usuario).filter(contrasenia=password).values_list()
        empresaLogueada = Empresa.objects.filter(usuario=usuario).filter(contrasenia=password).values_list()
        if usuarioLogueado:
            print("es usuario")
            cuiL = usuarioLogueado[0][0]
            nitL = usuarioLogueado[0][1]
            nombreL = usuarioLogueado[0][2]
            fechaNacL = usuarioLogueado[0][3]
            usuarioL = usuarioLogueado[0][4]
            passL = usuarioLogueado[0][5]

            dicSession = {
                'cui': cuiL,
                'nit': nitL,
                'nombre': nombreL,
                'fechaNac': str(fechaNacL),
                'usuario': usuarioL,
                'pass': passL
            }
            request.session['datos'] = dicSession
            return redirect('homecompras')
        elif empresaLogueada:
            print("es empresa")
            print(empresaLogueada)
            idEmpresa = empresaLogueada[0][0]
            idTipoEmpresa = Tipoempresa.objects.filter(idtipoempresa=empresaLogueada[0][1]).values_list()
            tipoEmpresa = idTipoEmpresa[0][1]
            nombre = empresaLogueada[0][2]
            nombreComercial = empresaLogueada[0][3]
            representante = empresaLogueada[0][4]
            usuarioL = empresaLogueada[0][5]
            dicSession = {
                'idEmpresa': idEmpresa,
                'tipoEmpresa': tipoEmpresa,
                'nombre': nombre,
                'nombreComercial': nombreComercial,
                'representante': representante,
                'usuarioL': usuarioL
            }
            request.session['datos'] = dicSession
            return redirect('homecompras')
        else:
            mensaje = "Usuario o contraseña incorrectos"

        variables = {
            'mensaje': mensaje,
        }
    return render(request, "loginCompras.html", variables)

def home(request):
    return render(request, "HomeCompra.html")

def logoutCompras(request):
    request.session['datos'] = {}
    dic = request.session['datos']
    nombre = dic.get('nombre')
    print("nombreeeee", nombre)
    return HttpResponseRedirect(reverse('logincomp'))