import MySQLdb
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import *
# Create your views here.

host = 'localhost'
db_name = 'Proyecto'
user = 'root'
contra = 'admin'
puerto = 3306

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
            passL = empresaLogueada[0][6]
            dicSession = {
                'idEmpresa': idEmpresa,
                'tipoEmpresa': tipoEmpresa,
                'nombre': nombre,
                'nombreComercial': nombreComercial,
                'representante': representante,
                'usuarioL': usuarioL,
                'pass': passL
            }
            request.session['datos'] = dicSession
            return redirect('infoempresa')
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


def infoEmpresa(request):
    diccSession = request.session['datos']
    return render(request, "infoEmpresa.html", diccSession)


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

            listaTransacciones = Transacciontarjeta.objects.filter(numerotarjeta=numeroTarjeta).values_list()
            print(listaTransacciones)

            variables = {
                'form': form,
                'numeroTarjeta': detalleTarjeta[0][0],
                'numeroCuenta': detalleTarjeta[0][6],
                'numeroCuenta': detalleTarjeta[0][6],
                'puntos': puntos,
                'saldoQ': saldoQ,
                'saldoS': saldoS,
                'listaTransaccion': listaTransacciones
            }
    return render(request, "tarjetas.html", variables)


def registroPlanilla(request):
    dicEmpresa = request.session['datos']
    idEmpresa = dicEmpresa.get('idEmpresa')
    print(idEmpresa)
    form = RegistroPlanilla()
    variables = {
        'form': form
    }
    if request.method == "POST":
        form = RegistroPlanilla(data=request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            nombrePl = datos.get('nombre')

            db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
            cursor = db.cursor()
            consulta = "INSERT INTO Planilla(nombre, idEmpresa) values('"+nombrePl+"', "+str(idEmpresa)+")"
            cursor.execute(consulta)
            db.commit()
            cursor.close()
            mensaje = f"Planilla {nombrePl} creada correctamente"
            form = RegistroPlanilla()
            variables = {
                'mensaje': mensaje,
                'form': form
            }
    return render(request, "registroPlanilla.html", variables)


def addEmpleadoPlanilla(request):
    dicEmpresa = request.session['datos']
    idEmpresa = dicEmpresa.get('idEmpresa')
    print(idEmpresa)
    obtenerPlanillas = Planilla.objects.filter(idempresa=idEmpresa).values_list()
    listaPlanillas = []
    if len(obtenerPlanillas) > 0:
        for planilla in obtenerPlanillas:
            listaPlanillas.append((planilla[0], planilla[1]))
    else:
        listaPlanillas.append(("No hay planillas", "No hay planillas"))
    print(listaPlanillas)

    form = IngresoUsuarioPlanilla(listaPlanillas)
    variables = {
        'form': form,
    }
    if request.method == "POST":
        form = IngresoUsuarioPlanilla(listaPlanillas, data=request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            cuenta = datos.get('numeroCuentaEmpleado')
            nombre = datos.get('nombre')
            sueldo = datos.get('sueldo')
            formaPago = datos.get('formaPago')
            idPlanilla = datos.get('planilla')
            print(cuenta)
            print(nombre)
            print(sueldo)
            print(formaPago)
            print(idPlanilla)
            cuentaMon = Cuentamonetaria.objects.filter(codigocuenta=cuenta).values_list()
            cuentaAho = Cuentadeahorro.objects.filter(codigocuenta=cuenta).values_list()
            cuentaPlaz = Cuentaplazofijo.objects.filter(codigocuenta=cuenta).values_list()
            if cuentaMon or cuentaAho or cuentaPlaz:
                print("si existe la cuenta")
                db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
                cursor = db.cursor()
                consulta = "INSERT INTO DetallePlanilla(codigoPlanilla, numeroCuenta, nombre, sueldo, formaPago) values" \
                           "(" + str(idPlanilla) + ", " + str(cuenta) + ", '" + nombre + "', " + str(
                    sueldo) + ", '" + formaPago + "')"
                print(consulta)
                cursor.execute(consulta)
                db.commit()
                cursor.close()
                mensaje = "Empleado agregado correctamente"
                form = IngresoUsuarioPlanilla(listaPlanillas)
                variables = {
                    'mensaje': mensaje,
                    'form': form,
                }
            else:
                mensaje = "No existe la cuenta ingresada"
                variables = {
                    'mensaje': mensaje,
                    'form': form,
                }
    return render(request, "addEmpleadoPlanilla.html", variables)