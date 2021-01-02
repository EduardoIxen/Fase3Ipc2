import MySQLdb
import csv, io
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
    idUsuario = 0
    idUsuario2 = 0
    idEmpresa = 0
    interes = 0
    dic = request.session['datos']
    if dic.get('cui') != None:
        idUsuario = dic.get('cui')
        idUsuario2 = dic.get('cui')
    elif dic.get('idEmpresa') != None:
        idUsuario = dic.get('idEmpresa')
        idEmpresa = dic.get('idEmpresa')

    cuentasCl = Detalleclientecuenta.objects.filter(codigocliente=idUsuario).values_list()
    cuentasEmp = Detalleclientecuenta.objects.filter(idempresa=idUsuario).values_list()
    listaCuentas = []
    if cuentasCl:
        for cuenta in cuentasCl:
            if cuenta[3] != None:
                listaCuentas.append((cuenta[3], cuenta[3]))
            elif cuenta[4] != None:
                listaCuentas.append((cuenta[4], cuenta[4]))
            elif cuenta[5] != None:
                listaCuentas.append((cuenta[5], cuenta[5]))
            else:
                listaCuentas.append(("No tiene cuentas", "No tiene cuentas"))
    elif cuentasEmp:
        for cuenta in cuentasEmp:
            if cuenta[3] != None:
                listaCuentas.append((cuenta[3], cuenta[3]))
            elif cuenta[4] != None:
                listaCuentas.append((cuenta[4], cuenta[4]))
            elif cuenta[5] != None:
                listaCuentas.append((cuenta[5], cuenta[5]))
            else:
                listaCuentas.append(("No tiene cuentas", "No tiene cuentas"))

    form = SolicitudPrestamo(listaCuentas)
    variables = {
        'form': form,
        'idEmpresa': idEmpresa
    }

    if request.method == "POST":
        form = SolicitudPrestamo(listaCuentas, data=request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            cuentaSeleccionada = datos.get('cuenta')
            descripcion = datos.get('descripcion')
            montoSolicitado = datos.get('montoSolicitado')
            tiempo = datos.get('tiempoEnDevolver')
            cuotaSinInteres = 0
            cuotaConInteres = 0
            if montoSolicitado >= 100 and montoSolicitado <= 5000:
                if tiempo == "12 meses":
                    interes = 0.05
                    cuotaSinInteres = montoSolicitado / 12
                    cuotaConInteres = float(montoSolicitado/12)*interes
                    cuotaConInteres = float(cuotaSinInteres) + cuotaConInteres
                elif tiempo == "24 meses":
                    interes = 0.04
                    cuotaSinInteres = montoSolicitado / 24
                    cuotaConInteres = float(montoSolicitado/24)*interes
                    cuotaConInteres = float(cuotaSinInteres) + cuotaConInteres
                elif tiempo == "36 meses":
                    interes = 0.0335
                    cuotaSinInteres = montoSolicitado / 36
                    cuotaConInteres = float(montoSolicitado/36)*interes
                    cuotaConInteres = float(cuotaSinInteres) + cuotaConInteres
                elif tiempo == "48 meses":
                    interes = 0.025
                    cuotaSinInteres = montoSolicitado / 48
                    cuotaConInteres = float(montoSolicitado/48)*interes
                    cuotaConInteres = float(cuotaSinInteres) + cuotaConInteres
            elif montoSolicitado >= 5000.01 and montoSolicitado <= 15000:
                if tiempo == "12 meses":
                    interes = 0.0525
                    cuotaSinInteres = montoSolicitado / 12
                    cuotaConInteres = float(montoSolicitado/12)*interes
                    cuotaConInteres = float(cuotaSinInteres) + cuotaConInteres
                elif tiempo == "24 meses":
                    interes = 0.0415
                    cuotaSinInteres = montoSolicitado / 24
                    cuotaConInteres = float(montoSolicitado/24)*interes
                    cuotaConInteres = float(cuotaSinInteres) + cuotaConInteres
                elif tiempo == "36 meses":
                    interes = 0.035
                    cuotaSinInteres = montoSolicitado / 36
                    cuotaConInteres = float(montoSolicitado/36)*interes
                    cuotaConInteres = float(cuotaSinInteres) + cuotaConInteres
                elif tiempo == "48 meses":
                    interes = 0.026
                    cuotaSinInteres = montoSolicitado / 48
                    cuotaConInteres = float(montoSolicitado/48)*interes
                    cuotaConInteres = float(cuotaSinInteres) + cuotaConInteres
            elif montoSolicitado >= 15000.01 and montoSolicitado <= 30000:
                if tiempo == "12 meses":
                    interes = 0.0530
                    cuotaSinInteres = montoSolicitado / 12
                    cuotaConInteres = float(montoSolicitado/12)*interes
                    cuotaConInteres = float(cuotaSinInteres) + cuotaConInteres
                elif tiempo == "24 meses":
                    interes = 0.0420
                    cuotaSinInteres = montoSolicitado / 24
                    cuotaConInteres = float(montoSolicitado/24)*interes
                    cuotaConInteres = float(cuotaSinInteres) + cuotaConInteres
                elif tiempo == "36 meses":
                    interes = 0.0355
                    cuotaSinInteres = montoSolicitado / 36
                    cuotaConInteres = float(montoSolicitado/36)*interes
                    cuotaConInteres = float(cuotaSinInteres) + cuotaConInteres
                elif tiempo == "48 meses":
                    interes = 0.0265
                    cuotaSinInteres = montoSolicitado / 48
                    cuotaConInteres = float(montoSolicitado/48)*interes
                    cuotaConInteres = float(cuotaSinInteres) + cuotaConInteres
            elif montoSolicitado >= 30000.01 and montoSolicitado <= 60000:
                if tiempo == "12 meses":
                    interes = 0.0535
                    cuotaSinInteres = montoSolicitado / 12
                    cuotaConInteres = float(montoSolicitado/12)*interes
                    cuotaConInteres = float(cuotaSinInteres) + cuotaConInteres
                elif tiempo == "24 meses":
                    interes = 0.0425
                    cuotaSinInteres = montoSolicitado / 24
                    cuotaConInteres = float(montoSolicitado/24)*interes
                    cuotaConInteres = float(cuotaSinInteres) + cuotaConInteres
                elif tiempo == "36 meses":
                    interes = 0.0360
                    cuotaSinInteres = montoSolicitado / 36
                    cuotaConInteres = float(montoSolicitado/36)*interes
                    cuotaConInteres = float(cuotaSinInteres) + cuotaConInteres
                elif tiempo == "48 meses":
                    interes = 0.0270
                    cuotaSinInteres = montoSolicitado / 48
                    cuotaConInteres = float(montoSolicitado/48)*interes
                    cuotaConInteres = float(cuotaSinInteres) + cuotaConInteres
            elif montoSolicitado >= 60000.01:
                if tiempo == "12 meses":
                    interes = 0.0545
                    cuotaSinInteres = montoSolicitado / 12
                    cuotaConInteres = float(montoSolicitado/12)*interes
                    cuotaConInteres = float(cuotaSinInteres) + cuotaConInteres
                elif tiempo == "24 meses":
                    interes = 0.0435
                    cuotaSinInteres = montoSolicitado / 24
                    cuotaConInteres = float(montoSolicitado/24)*interes
                    cuotaConInteres = float(cuotaSinInteres) + cuotaConInteres
                elif tiempo == "36 meses":
                    interes = 0.0370
                    cuotaSinInteres = montoSolicitado / 36
                    cuotaConInteres = float(montoSolicitado/36)*interes
                    cuotaConInteres = float(cuotaSinInteres) + cuotaConInteres
                elif tiempo == "48 meses":
                    interes = 0.0280
                    cuotaSinInteres = montoSolicitado / 48
                    cuotaConInteres = float(montoSolicitado/48)*interes
                    cuotaConInteres = float(cuotaSinInteres) + cuotaConInteres

            pagos = 0
            if tiempo == "12 meses":
                pagos = 12
            elif tiempo == "24 meses":
                pagos = 24
            elif tiempo == "36 meses":
                pagos = 36
            elif tiempo == "48 meses":
                pagos = 48
            totalCI = pagos * cuotaConInteres

            if idUsuario2 != 0:

                db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
                cursor = db.cursor()
                consulta = "INSERT INTO Prestamo(montoRequerido, modalidadAPagar, codigoCliente, descripcion, cuenta, aprobado)" \
                           " values("+str(montoSolicitado)+", "+str(pagos)+", "+str(idUsuario2)+", '"+descripcion+"',"+str(cuentaSeleccionada)+", "+str(0)+")"
                print(consulta)
                cursor.execute(consulta)
                db.commit()
                cursor.close()
            elif idEmpresa != 0:
                db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
                cursor = db.cursor()
                consulta = "INSERT INTO Prestamo(montoRequerido, modalidadAPagar, idEmpresa, descripcion, cuenta, aprobado)" \
                           " values(" + str(montoSolicitado) + ", " + str(
                    pagos) + ", " + str(idEmpresa) + ", '" + descripcion + "',"+cuentaSeleccionada+" ," + str(0) + ")"
                print(consulta)
                cursor.execute(consulta)
                db.commit()
                cursor.close()

            form = SolicitudPrestamo(listaCuentas)
            variables = {
                'montoSolicitado': montoSolicitado,
                'meses': tiempo,
                'cuotaSinInteres': f"{cuotaSinInteres:.2f}",
                'cuotaConInteres': f"{cuotaConInteres:.2f}",
                'pagos': pagos,
                'totalConInteres': f"{totalCI:.2f}",
                'form': form
            }

    return render(request, "prestamo.html", variables)


def estadoDeCeunta(request):
    return render(request, "estadoDeCuenta.html")


def infoUsr(request):
    diccSession = request.session['datos']
    cui = diccSession.get('cui')
    nit = diccSession.get('nit')
    nombre = diccSession.get('nombre')
    usuario = diccSession.get('usuario')

    cuentas = Detalleclientecuenta.objects.filter(codigocliente=cui).values_list()
    listaCuentas = []
    for cuenta in cuentas:
        if cuenta[3] != None:
            cuentaMonetaria = Cuentamonetaria.objects.filter(codigocuenta=cuenta[3]).values_list()
            listaCuentas.append(cuentaMonetaria)
        elif cuenta[4] != None:
            cuentaAhorro = Cuentadeahorro.objects.filter(codigocuenta=cuenta[4]).values_list()
            listaCuentas.append(cuentaAhorro)
        elif cuenta[5] != None:
            cuentaPlazo = Cuentaplazofijo.objects.filter(codigocuenta=cuenta[5]).values_list()
            listaCuentas.append(cuentaPlazo)

    print(listaCuentas)
    variables = {
        'listaCuentas': listaCuentas,
        'cui': nombre,
        'nit': nit,
        'nombre': nombre,
        'usuario': usuario
    }
    return render(request, "infoUsr.html", variables)


def infoEmpresa(request):
    diccSession = request.session['datos']
    idEmpresa = diccSession.get('idEmpresa')
    nombre = diccSession.get('nombre')
    nombreCom = diccSession.get('nombreComercial')
    representante = diccSession.get('representante')
    usrio = diccSession.get('usuarioL')
    cuentas = Detalleclientecuenta.objects.filter(idempresa=idEmpresa).values_list()
    listaCuentas = []
    for cuenta in cuentas:
        if cuenta[3] != None:
            cuentaMonetaria = Cuentamonetaria.objects.filter(codigocuenta=cuenta[3]).values_list()
            listaCuentas.append(cuentaMonetaria)
        elif cuenta[4] != None:
            cuentaAhorro = Cuentadeahorro.objects.filter(codigocuenta=cuenta[4]).values_list()
            listaCuentas.append(cuentaAhorro)
        elif cuenta[5] != None:
            cuentaPlazo = Cuentaplazofijo.objects.filter(codigocuenta=cuenta[5]).values_list()
            listaCuentas.append(cuentaPlazo)

    print(listaCuentas)
    variables = {
        'listaCuentas': listaCuentas,
        'idEmpresa': idEmpresa,
        'nombre': nombre,
        'nombreCom': nombreCom,
        'repre': representante,
        'usr': usrio
    }


    return render(request, "infoEmpresa.html", variables)


def logout(request):
    request.session['datos'] = {}
    dic = request.session['datos']
    nombre = dic.get('nombre')
    print("nombreeeee", nombre)
    return HttpResponseRedirect(reverse('login'))


def tarjeta(request):
    idUsuario = 0
    idEmpresa = 0
    dic = request.session['datos']
    if dic.get('cui') != None:
        idUsuario = dic.get('cui')
    elif dic.get('idEmpresa') != None:
        idUsuario = dic.get('idEmpresa')
        idEmpresa = dic.get('idEmpresa')

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
        listaAlterna = []
        listaAlterna.append(("No cuenta con tarjetas", "No cuenta con tarjetas"))
        form = consultarTarjeta(listaAlterna)
    variables = {
        'listaTarjetas': listaTarjetas,
        'mensaje': mensaje,
        'form': form,
        'idEmpresa': idEmpresa
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
                'moneda': detalleTarjeta[0][5],
                'puntos': puntos,
                'saldoQ': saldoQ,
                'saldoS': saldoS,
                'listaTransaccion': listaTransacciones,
                'idEmpresa': idEmpresa
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


def CargarCSV(request):
    prompt = {
        'orden': 'nombre, cuenta, sueldo'
    }

    if request.method == "GET":
        return render(request, "cargarCSV.html", prompt)

    csvFile = request.FILES['file']
    dataSet = csvFile.read().decode('UTF-8')
    io_string = io.StringIO(dataSet)
    #print(io_string)
    contador = 0
    listaRegistro = []
    for columna in csv.reader(io_string, delimiter=',', quotechar='|'):
        dicRegistro = {}
        dicRegistro['Nombre'] = columna[0]
        dicRegistro['Cuenta'] = columna[1]
        dicRegistro['Sueldo'] = columna[2]
        listaRegistro.append(dicRegistro)

    request.session['csv'] = listaRegistro
    return redirect('seleccionarplanilla')

def cargarCSV2(request):
    noExistentes = ''
    dicEmpresa = request.session['datos']
    idEmpresa = dicEmpresa.get('idEmpresa')
    obtenerPlanillas = Planilla.objects.filter(idempresa=idEmpresa).values_list()
    listaPlanillas = []
    if len(obtenerPlanillas) > 0:
        for planilla in obtenerPlanillas:
            listaPlanillas.append((planilla[0], planilla[1]))
    else:
        listaPlanillas.append(("No hay planillas", "No hay planillas"))
    #print(listaPlanillas)
    form = ConsultaPlanilla(listaPlanillas)
    variables = {
        'form': form
    }
    registrosCSV = request.session['csv']
    #print("tiiipooo", registrosCSV)
    if request.method == 'POST':
        form = ConsultaPlanilla(listaPlanillas, data=request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            planilla = datos.get('planilla')
            print(planilla)
            contador = 0
            for registro in registrosCSV:
                contador += 1
                if contador > 1:
                    #print(registro['Nombre'])
                    existeCuentaMon = Detalleclientecuenta.objects.filter(codigocuentamonetaria=registro['Cuenta']).values_list()
                    existeCuentaAh = Detalleclientecuenta.objects.filter(codigocuentaahorro=registro['Cuenta']).values_list()
                    existeCuentaPl = Detalleclientecuenta.objects.filter(codigocuentaplazofijo=registro['Cuenta']).values_list()
                    if existeCuentaMon or existeCuentaAh or existeCuentaPl:
                        db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
                        cursor = db.cursor()
                        consulta = "INSERT INTO DetallePlanilla(codigoPlanilla, numeroCuenta, nombre, sueldo) values(" + str(
                            planilla) + ", " + str(
                            registro['Cuenta']) + ", '" + registro['Nombre'] + "', " + registro['Sueldo'] + ")"
                        # print(consulta)
                        cursor.execute(consulta)
                        db.commit()
                        cursor.close()
                        mensaje = "Usuarios registrados con exito"
                        form = ConsultaPlanilla(listaPlanillas)
                        variables = {
                            'mensaje': mensaje,
                            'form': form
                        }
                    else:
                        noExistentes = noExistentes +" ||| "+ registro['Cuenta']
                        mensaje = f"No existe la cuenta {noExistentes}"
                        form = ConsultaPlanilla(listaPlanillas)
                        variables = {
                            'mensaje': mensaje,
                            'form': form
                        }



    return render(request, "seleccionarPlanilla.html", variables)


def pagarPlanilla(request):
    idUsuario = 0
    idEmpresa = 0
    cuentasGlobales = []
    detallePlanilla = []
    total = 0
    total2 = 0
    dic = request.session['datos']
    if dic.get('cui') != None:
        idUsuario = dic.get('cui')
    elif dic.get('idEmpresa') != None:
        idEmpresa = dic.get('idEmpresa')

    planillasDisponibles = Planilla.objects.filter(idempresa=idEmpresa).values_list()
    listaPlanillas = []
    for planilla in planillasDisponibles:
        listaPlanillas.append((planilla[0], planilla[1]))
    form = ConsultaPlanilla(listaPlanillas)
    variables = {
        'form': form
    }
    if request.method == "POST":
        form = ConsultaPlanilla(listaPlanillas, data=request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            planillaSeleccionada = datos.get('planilla')
            detallePlanilla = Detalleplanilla.objects.filter(codigoplanilla=planillaSeleccionada).values_list()
            listaSueldos = []
            for registro in detallePlanilla:
                listaSueldos.append(registro[4])
            total = sum(listaSueldos)
            total2 = sum(listaSueldos)
            lsCuentas = []
            cuentasUsr = Detalleclientecuenta.objects.filter(idempresa=idEmpresa).values_list()
            print(cuentasUsr)
            for cuenta in cuentasUsr:
                if cuenta[3] != None:
                    lsCuentas.append((cuenta[3], cuenta[3]))
                elif cuenta[4] != None:
                    lsCuentas.append((cuenta[4], cuenta[4]))
                elif cuenta[5] != None:
                    lsCuentas.append((cuenta[5], cuenta[5]))

            print(lsCuentas)
            cuentasGlobales = lsCuentas
            total2 = total
            fCuentas = consultarCuenta(lsCuentas)
            variables = {
                'form': form,
                'lista': detallePlanilla,
                'total': total,
                'fCuentas': fCuentas
            }
            listaCobro = []
            for detalle in detallePlanilla:
                listaCobro.append(detalle)
            variables2 = {
                'total': float(total),
                'planilla': planillaSeleccionada
            }
            request.session['pagoPlanilla'] = variables2

        fCuentas = consultarCuenta(cuentasGlobales, data=request.POST)
        if fCuentas.is_valid():
            print(detallePlanilla)
            datos2 = fCuentas.cleaned_data
            cuentaPago = datos2.get('cuenta')
            consCuentaAh = Cuentadeahorro.objects.filter(codigocuenta=cuentaPago).values_list()
            consCuentaMn = Cuentamonetaria.objects.filter(codigocuenta=cuentaPago).values_list()
            consCuentaPl = Cuentaplazofijo.objects.filter(codigocuenta=cuentaPago).values_list()
            dic = request.session['pagoPlanilla']
            total = dic.get('total')
            plSelec = dic.get('planilla')
            detallePlanilla = Detalleplanilla.objects.filter(codigoplanilla=plSelec).values_list()
            if consCuentaAh:
                print("entro1\n")
                saldo = consCuentaAh[0][3]
                if saldo >= total:
                    for detalle in detallePlanilla:
                        cuentaEmp = detalle[2]
                        sueldoEmp = detalle[4]
                        consulta1 = Cuentadeahorro.objects.filter(codigocuenta=cuentaEmp).values_list()
                        consulta2 = Cuentamonetaria.objects.filter(codigocuenta=cuentaEmp).values_list()
                        consulta3 = Cuentaplazofijo.objects.filter(codigocuenta=cuentaEmp).values_list()

                        if consulta1:
                            db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
                            cursor = db.cursor()
                            consulta = "UPDATE CuentaDeAhorro set saldo=saldo+"+str(sueldoEmp)+" where codigoCuenta="+str(cuentaEmp)+""
                            print(consulta)
                            cursor.execute(consulta)
                            db.commit()
                            cursor.close()
                        elif consulta2:
                            db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
                            cursor = db.cursor()
                            consulta = "UPDATE CuentaMonetaria set saldo=saldo+"+str(sueldoEmp)+" where codigoCuenta="+str(cuentaEmp)+""
                            print(consulta)
                            cursor.execute(consulta)
                            db.commit()
                            cursor.close()
                        elif consulta3:
                            db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
                            cursor = db.cursor()
                            consulta = "UPDATE CuentaPlazoFijo set saldo=saldo+"+str(sueldoEmp)+" where codigoCuenta="+str(cuentaEmp)+""
                            print(consulta)
                            cursor.execute(consulta)
                            db.commit()
                            cursor.close()
                        db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
                        cursor = db.cursor()
                        consulta = "UPDATE CuentaDeAhorro set saldo=saldo-" + str(
                            sueldoEmp) + " where codigoCuenta=" + str(cuentaPago) + ""
                        print(consulta)
                        cursor.execute(consulta)
                        db.commit()
                        cursor.close()
                else:
                    print("noooooo hay saldo!!!!")
                    mensaje = "No hay suficiente saldo"
                    variables = {
                        'form':form,
                        'mensaje': mensaje,
                        'total': total
                    }
            elif consCuentaMn:
                print("entro2\n")
                saldo = consCuentaMn[0][3]
                print(saldo)
                print(total2)
                if saldo >= total:
                    print("entro 2.2")
                    for detalle in detallePlanilla:
                        cuentaEmp = detalle[2]
                        sueldoEmp = detalle[4]
                        print("sueldo emp", sueldoEmp)
                        print("cuenta emo", cuentaEmp)
                        consulta1 = Cuentadeahorro.objects.filter(codigocuenta=cuentaEmp).values_list()
                        consulta2 = Cuentamonetaria.objects.filter(codigocuenta=cuentaEmp).values_list()
                        consulta3 = Cuentaplazofijo.objects.filter(codigocuenta=cuentaEmp).values_list()

                        if consulta1:
                            db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name,
                                                 connect_timeout=5)
                            cursor = db.cursor()
                            consulta = "UPDATE CuentaDeAhorro set saldo=saldo+" + str(
                                sueldoEmp) + " where codigoCuenta=" + str(cuentaEmp) + ""
                            print(consulta)
                            cursor.execute(consulta)
                            db.commit()
                            cursor.close()
                        elif consulta2:
                            db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name,
                                                 connect_timeout=5)
                            cursor = db.cursor()
                            consulta = "UPDATE CuentaMonetaria set saldo=saldo+" + str(
                                sueldoEmp) + " where codigoCuenta=" + str(cuentaEmp) + ""
                            print(consulta)
                            cursor.execute(consulta)
                            db.commit()
                            cursor.close()
                        elif consulta3:
                            db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name,
                                                 connect_timeout=5)
                            cursor = db.cursor()
                            consulta = "UPDATE CuentaPlazoFijo set saldo=saldo+" + str(
                                sueldoEmp) + " where codigoCuenta=" + str(cuentaEmp) + ""
                            print(consulta)
                            cursor.execute(consulta)
                            db.commit()
                            cursor.close()
                        db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
                        cursor = db.cursor()
                        consulta = "UPDATE CuentaMonetaria set saldo=saldo-" + str(
                            sueldoEmp) + " where codigoCuenta=" + str(cuentaPago) + ""
                        print(consulta)
                        cursor.execute(consulta)
                        db.commit()
                        cursor.close()
                else:
                    print("noooooo hay saldo!!!!")
                    mensaje = "No hay suficiente saldo"
                    variables = {
                        'form':form,
                        'mensaje': mensaje,
                        'total': total
                    }
            elif consCuentaPl:
                print("entro3\n")
                saldo = consCuentaPl[0][3]
                if saldo >= total:
                    for detalle in detallePlanilla:
                        cuentaEmp = detalle[2]
                        sueldoEmp = detalle[4]
                        consulta1 = Cuentadeahorro.objects.filter(codigocuenta=cuentaEmp).values_list()
                        consulta2 = Cuentamonetaria.objects.filter(codigocuenta=cuentaEmp).values_list()
                        consulta3 = Cuentaplazofijo.objects.filter(codigocuenta=cuentaEmp).values_list()

                        if consulta1:
                            db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name,
                                                 connect_timeout=5)
                            cursor = db.cursor()
                            consulta = "UPDATE CuentaDeAhorro set saldo=saldo+" + str(
                                sueldoEmp) + " where codigoCuenta=" + str(cuentaEmp) + ""
                            print(consulta)
                            cursor.execute(consulta)
                            db.commit()
                            cursor.close()
                        elif consulta2:
                            db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name,
                                                 connect_timeout=5)
                            cursor = db.cursor()
                            consulta = "UPDATE CuentaMonetaria set saldo=saldo+" + str(
                                sueldoEmp) + " where codigoCuenta=" + str(cuentaEmp) + ""
                            print(consulta)
                            cursor.execute(consulta)
                            db.commit()
                            cursor.close()
                        elif consulta3:
                            db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name,
                                                 connect_timeout=5)
                            cursor = db.cursor()
                            consulta = "UPDATE CuentaPlazoFijo set saldo=saldo+" + str(
                                sueldoEmp) + " where codigoCuenta=" + str(cuentaEmp) + ""
                            print(consulta)
                            cursor.execute(consulta)
                            db.commit()
                            cursor.close()
                        db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name,
                                             connect_timeout=5)
                        cursor = db.cursor()
                        consulta = "UPDATE CuentaPlazoFijo set saldo=saldo-" + str(
                            sueldoEmp) + " where codigoCuenta=" + str(cuentaPago) + ""
                        print(consulta)
                        cursor.execute(consulta)
                        db.commit()
                        cursor.close()
                else:
                    print("noooooo hay saldo!!!!")
                    mensaje = "No hay suficiente saldo"
                    variables = {
                        'form':form,
                        'mensaje': mensaje,
                        'total': total
                    }




    return render(request, "visualizarPlanilla.html", variables)