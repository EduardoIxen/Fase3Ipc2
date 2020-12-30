from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import *
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
            return redirect('infousr')
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
            return redirect('infousr')
        else:
            mensaje = "Usuario o contraseña incorrectos"

        variables = {
            'mensaje': mensaje,
        }

    return render(request, "login.html", variables)


def transferencia(request):
    return render(request, "transferencia.html")


def prestamo(request):
    return render(request, "prestamo.html")


def estadoDeCeunta(request):
    return render(request, "estadoDeCuenta.html")


def infoUsr(request):
    diccSession = request.session['datos']
    return render(request, "infoUsr.html", diccSession)


def logout(request):
    request.session['datos'] = {}
    dic = request.session['datos']
    nombre = dic.get('nombre')
    print("nombreeeee", nombre)
    return HttpResponseRedirect(reverse('login'))


def tarjeta(request):
    dic = request.session['datos']
    if dic.get('cui') != None:
        idUsuario = dic.get('cui')
    elif dic.get('idEmpresa') != None:
        idUsuario = dic.get('idEmpresa')

    tarjetasUsuario = Tarjetadecredito.objects.filter(cuicliente=idUsuario).values_list()
    tarjetasEmpresa = Tarjetadecredito.objects.filter(idempresa=idUsuario).values_list()
    listaTarjetas = []
    mensaje = ''
    if tarjetasUsuario:
        for tarjeta in tarjetasUsuario:
            marca = Marca.objects.filter(codigomarca=tarjeta[1]).values_list()
            listaTarjetas.append((tarjeta[0], f"{tarjeta[0]} --- {marca[0][1]}"))
        form = consultarTarjeta(listaTarjetas)
    elif tarjetasEmpresa:
        for tarjeta in tarjetasEmpresa:
            marca = Marca.objects.filter(codigomarca=tarjeta[1]).values_list()
            listaTarjetas.append((tarjeta[0], f"{tarjeta[0]} --- {marca[0][1]}"))
        form = consultarTarjeta(listaTarjetas)
    else:
        mensaje = "No posee tarjetas de credito"
    variables = {
        'listaTarjetas': listaTarjetas,
        'mensaje': mensaje,
        'form': form
    }

    if request.method == 'POST':
        form = consultarTarjeta(listaTarjetas, data=request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            numeroTarjeta = datos.get('numeroTarjeta')
            detalleTarjeta = Tarjetadecredito.objects.filter(numerotarjeta=numeroTarjeta).values_list()
            print(detalleTarjeta)
            saldoQ = 0
            saldoS = 0
            puntos = 0
            if detalleTarjeta[0][5] == 1: #quetzal
                if detalleTarjeta[0][1] == 1: #prefepuntos
                    saldoQ = detalleTarjeta[0][9] - detalleTarjeta[0][10]
                    saldoQ = f"{saldoQ:.2f}"
                    puntos = detalleTarjeta[0][7]
                    saldoS = float(detalleTarjeta[0][9] - detalleTarjeta[0][10]) / 7.63
                    saldoS = f"{saldoS:.2f}"
                else: #cashback
                    saldoQ = detalleTarjeta[0][9] - detalleTarjeta[0][10]
                    puntos = None
                    saldoS = float(detalleTarjeta[0][9] - detalleTarjeta[0][10]) / 7.87
                    saldoS = f"{saldoS:.2f}"
            else: #dolar
                if detalleTarjeta[0][1] == 1: #prefepuntos
                    saldoS = detalleTarjeta[0][9] - detalleTarjeta[0][10]
                    saldoS = f"{saldoS:.2f}"
                    saldoQ = float(detalleTarjeta[0][9] - detalleTarjeta[0][10]) * 7.63
                    saldoQ = f"{saldoQ:.2f}"
                    puntos = detalleTarjeta[0][7]
                else:
                    saldoS = detalleTarjeta[0][9] - detalleTarjeta[0][10]
                    saldoS = f"{saldoS:.2f}"
                    saldoQ = float(detalleTarjeta[0][9] - detalleTarjeta[0][10]) * 7.87
                    saldoQ = f"{saldoQ:.2f}"
                    puntos = None

            variables = {
                'form': form,
                'numeroTarjeta': detalleTarjeta[0][0],
                'numeroCuenta': detalleTarjeta[0][6],
                'numeroCuenta': detalleTarjeta[0][6],
                'puntos': puntos,
                'saldoQ': saldoQ,
                'saldoS': saldoS
            }
    return render(request, "tarjetas.html", variables)
