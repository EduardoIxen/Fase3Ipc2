from django.shortcuts import render
from django.shortcuts import redirect
from .forms import *
import MySQLdb
from .Calculos import *
from .models import Empresa

host = 'localhost'
db_name = 'Proyecto'
user = 'root'
contra = 'admin'
puerto = 3306

# Create your views here.
def registroCliente(request):
    form = Cliente()
    nombre = "Registro de cliente individual"
    variables = {
        "form":form,
        "mensaje": nombre
    }
    if request.method == "POST":
        form = Cliente(data=request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            cui = datos.get('cui')
            nit = datos.get('nit')
            nombreCompleto = datos.get('nombrecompleto')
            fechaNacimiento = datos.get('fechanacimiento')
            usuario = datos.get('usuario')
            contrasenia = datos.get('contrasenia')
            db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
            cursor = db.cursor()
            consulta = "INSERT INTO ClienteIndividual VALUES("+str(cui)+",'"+str(nit)+"','"+nombreCompleto+"', '"+str(fechaNacimiento)+"', '"+usuario+"', '"+contrasenia+"')"
            #print(consulta)
            cursor.execute(consulta)
            db.commit()
            cursor.close()
            nombre = f"Usuario {nombreCompleto} registrado de manera correcta"
            form = Cliente()
            variables = {
                "form": form,
                "mensaje": nombre
            }
        else:
            nombre = "Error de registro, intente de nuevo"
            variables = {
                "form":form,
                "mensaje":nombre
            }

    return render(request, 'registroCliente.html', variables)

def registroEmpresa(request):
    form = Empresaa()
    nombre = "Registro de Empresa"
    variables = {
        "form": form,
        "mensaje": nombre
    }
    if request.method == "POST":
        form = Empresaa(data=request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            idTipoEmpresa = datos.get('idtipoempresa')
            print(type(idTipoEmpresa.idtipoempresa), "tipooo")
            nombre = datos.get('nombre')
            nombreComercial = datos.get('nombrecomercial')
            nombreRepresentanteLegal = datos.get('nombrerepresentantelegal')
            usuario = datos.get('usuario')
            contrasenia = datos.get('contrasenia')
            db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
            cursor = db.cursor()
            consulta = "INSERT INTO Empresa(idTipoEmpresa, nombre, nombreComercial, nombreRepresentanteLegal, usuario, contrasenia) VALUES(" + str(
                idTipoEmpresa.idtipoempresa) + ",'" + nombre + "','" + nombreComercial + "', '" + nombreRepresentanteLegal + "', '" + usuario + "', '" + contrasenia + "')"
            print(consulta)
            cursor.execute(consulta)
            db.commit()
            cursor.close()
            nombre = f"Empresa {nombreComercial} registrada de manera correcta"
            form = Empresaa()
            variables = {
                "form": form,
                "mensaje": nombre
            }
        else:
            nombre = "Error de registro, intente de nuevo"
            variables = {
                "form": form,
                "mensaje": nombre
            }
    return render(request, 'registroEmpresa.html', variables)

def loginAdmin(request):
    mensaje = ""
    variables = {
        'mensaje': mensaje
    }
    if request.method == "POST":
        usuario = request.POST['usuariolog']
        password = request.POST['passwordlog']
        print(usuario)
        print(password)
        #consulta = "SELECT * FROM Administrador WHERE usuario = '"+usuario+"' and contrasenia = '"+password+"'"
        admin = Administrador.objects.filter(usuario=usuario).filter(contrasenia=password).values_list()
        if not admin:
            mensaje = "Usuario o contraseña incorrectos"
        else:
            usrL = admin[0][1]
            dicSession = {
                'usuario':usrL
            }
            request.session['datos'] = dicSession
            return redirect('registrocliente')
    variables = {
        'mensaje': mensaje
    }

    return render(request, "adminlogin.html", variables)

def logout(request):
    dic = request.session['datos']
    nombre = dic.get('nombre')
    print("nombreeeee en admin", nombre)
    return redirect('loginadmin')

def addCuentaMonetaria(request):
    form = CuentaMonetaria()
    mensaje = ""
    variables = {
        'form':form,
        'mensaje':mensaje
    }
    if request.method == "POST":
        form = CuentaMonetaria(data=request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            codigoCuenta = datos.get('codigocuenta')
            montoPorManejo = datos.get('montopormanejo')
            saldo = datos.get('saldo')
            tipoCliente = datos.get('tipocliente')
            idCliente = datos.get('idcliente')
            idMoneda = datos.get('codigomoneda')
            print(idMoneda)
            print(type(idMoneda))

            db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)

            cursor = db.cursor()
            cursor2 = db.cursor()
            consulta = "INSERT INTO CuentaMonetaria VALUES(" + str(codigoCuenta) + ","+idMoneda+"," + str(
                montoPorManejo) + "," + str(saldo) + ")"
            print(consulta)
            cursor.execute(consulta)
            db.commit()
            cursor.close()
            if tipoCliente.strip() == "1": #persona individual
                cliente = Clienteindividual.objects.filter(cui=idCliente).values_list()
                if not cliente:
                    mensaje = "El cliente no existe"
                    form = CuentaMonetaria()
                    variables = {
                        'mensaje':mensaje,
                        'form':form
                    }
                else:
                    consulta2 = "INSERT INTO DetalleClienteCuenta(codigoCliente, codigoCuentaMonetaria, estaActiva) VALUES("+str(
                        idCliente)+", "+str(codigoCuenta)+", "+str(True)+")"
                    print(consulta2)
                    cursor2.execute(consulta2)
                    db.commit()
                    cursor2.close()
                    form = CuentaMonetaria()
                    mensaje = "Cuenta creada correctamente"
                    variables = {
                        'form': form,
                        'mensaje': mensaje
                    }
            elif tipoCliente.strip() == "2":
                cliente = Empresa.objects.filter(idempresa=idCliente).values_list()
                if not cliente:
                    mensaje = "El cliente no existe"
                    form = CuentaMonetaria()
                    variables = {
                        'mensaje': mensaje,
                        'form': form
                    }
                else:
                    consulta2 = "INSERT INTO DetalleClienteCuenta(idEmpresa, codigoCuentaMonetaria, estaActiva) VALUES(" + str(
                        idCliente) + ", " + str(codigoCuenta) + ", " + str(True) + ")"
                    print(consulta2)
                    cursor2.execute(consulta2)
                    db.commit()
                    cursor2.close()
                    form = CuentaMonetaria()
                    mensaje = "Cuenta creada correctamente"
                    variables = {
                        'form': form,
                        'mensaje': mensaje
                    }
        else:
            mensaje = "Error de registro de cuenta"
            variables = {
                'form':form,
                'mensaje':mensaje
            }

    return render(request, "addCuentaMonetaria.html", variables)

def addCuentaDeAhorro(request):
    form = CuentaDeAhorro()
    mensaje = ''
    variables = {
        'mensaje': mensaje,
        'form': form
    }
    if request.method == "POST":
        form = CuentaDeAhorro(data=request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            codigoCuenta = datos.get('codigocuenta')
            tasainteres = datos.get('tasainteres')
            saldo = datos.get('saldo')
            tipoCliente = datos.get('tipocliente')
            idCliente = datos.get('idcliente')
            codigoMoneda = datos.get('codigomoneda')
            print(f"{type(tipoCliente)}, id {type(idCliente)}")
            db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
            cursor = db.cursor()
            cursor2 = db.cursor()
            cuenta1 = Cuentadeahorro.objects.filter(codigocuenta=codigoCuenta).values_list()
            cuenta2 = Cuentaplazofijo.objects.filter(codigocuenta=codigoCuenta).values_list()
            cuenta3 = Cuentadeahorro.objects.filter(codigocuenta=codigoCuenta).values_list()
            pasa = False
            if not cuenta1:
                if not cuenta2:
                    if not cuenta3:
                       pasa = True
            if pasa:
                consulta = "INSERT INTO CuentaDeAhorro VALUES(" + str(codigoCuenta) + ","+codigoMoneda+"," + str(
                    tasainteres) + "," + str(saldo) + ")"
                print(consulta)
                cursor.execute(consulta)
                db.commit()
                cursor.close()
                if tipoCliente.strip() == "1": #persona individual
                    cliente = Clienteindividual.objects.filter(cui=idCliente).values_list()
                    if not cliente:
                        mensaje = "El cliente no existe"
                        form = CuentaDeAhorro()
                        variables = {
                            'mensaje':mensaje,
                            'form':form
                        }
                    else:
                        consulta2 = "INSERT INTO DetalleClienteCuenta(codigoCliente, codigoCuentaAhorro, estaActiva) VALUES("+str(
                            idCliente)+", "+str(codigoCuenta)+", "+str(True)+")"
                        print(consulta2)
                        cursor2.execute(consulta2)
                        db.commit()
                        cursor2.close()
                        form = CuentaDeAhorro()
                        mensaje = "Cuenta creada correctamente"
                        variables = {
                            'form': form,
                            'mensaje': mensaje
                        }
                elif tipoCliente.strip() == "2":
                    cliente = Empresa.objects.filter(idempresa=idCliente).values_list()
                    if not cliente:
                        mensaje = "El cliente no existe"
                        form = CuentaDeAhorro()
                        variables = {
                            'mensaje': mensaje,
                            'form': form
                        }
                    else:
                        consulta2 = "INSERT INTO DetalleClienteCuenta(idEmpresa, codigoCuentaAhorro, estaActiva) VALUES(" + str(
                            idCliente) + ", " + str(codigoCuenta) + ", " + str(True) + ")"
                        print(consulta2)
                        cursor2.execute(consulta2)
                        db.commit()
                        cursor2.close()
                        form = CuentaDeAhorro()
                        mensaje = "Cuenta creada correctamente"
                        variables = {
                            'form': form,
                            'mensaje': mensaje
                        }
            else:
                mensaje = "El codigo de la cuenta ya existe"
                form = CuentaDeAhorro()
                variables = {
                    'mensaje': mensaje,
                    'form': form
                }
        else:
            mensaje = "Error de registro de cuenta"
            variables = {
                'form':form,
                'mensaje':mensaje
            }

    return render(request, "addCuentaAhorro.html", variables)

def addCuentaPlazoFijo(request):
    form = CuentaPlazoFijo()
    mensaje = ''
    variables = {
        'mensaje': mensaje,
        'form': form
    }
    if request.method == "POST":
        form = CuentaPlazoFijo(data=request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            codigoCuenta = datos.get('codigocuenta')
            tasainteres = datos.get('tasainteres')
            periodoTiempo = datos.get('periodotiempo')
            saldo = datos.get('saldo')
            tipoCliente = datos.get('tipocliente')
            idCliente = datos.get('idcliente')
            codigoMoneda = datos.get('codigomoneda')
            print(f"{type(tipoCliente)}, id {type(idCliente)}")
            db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
            cursor = db.cursor()
            cursor2 = db.cursor()
            consulta = "INSERT INTO CuentaPlazoFijo VALUES(" + str(codigoCuenta) + ","+codigoMoneda+"," + str(
                tasainteres) + ","+str(periodoTiempo)+" ," + str(saldo) + ")"
            print(consulta)
            cursor.execute(consulta)
            db.commit()
            cursor.close()
            if tipoCliente.strip() == "1":  # persona individual
                cliente = Clienteindividual.objects.filter(cui=idCliente).values_list()
                if not cliente:
                    mensaje = "El cliente no existe"
                    form = CuentaDeAhorro()
                    variables = {
                        'mensaje': mensaje,
                        'form': form
                    }
                else:
                    consulta2 = "INSERT INTO DetalleClienteCuenta(codigoCliente, codigoCuentaPlazoFijo, estaActiva) VALUES(" + str(
                        idCliente) + ", " + str(codigoCuenta) + ", " + str(True) + ")"
                    print(consulta2)
                    cursor2.execute(consulta2)
                    db.commit()
                    cursor2.close()
                    form = CuentaDeAhorro()
                    mensaje = "Cuenta creada correctamente"
                    variables = {
                        'form': form,
                        'mensaje': mensaje
                    }
            elif tipoCliente.strip() == "2":
                cliente = Empresa.objects.filter(idempresa=idCliente).values_list()
                if not cliente:
                    mensaje = "El cliente no existe"
                    form = CuentaDeAhorro()
                    variables = {
                        'mensaje': mensaje,
                        'form': form
                    }
                else:
                    consulta2 = "INSERT INTO DetalleClienteCuenta(idEmpresa, codigoCuentaPlazoFijo, estaActiva) VALUES(" + str(
                        idCliente) + ", " + str(codigoCuenta) + ", " + str(True) + ")"
                    print(consulta2)
                    cursor2.execute(consulta2)
                    db.commit()
                    cursor2.close()
                    form = CuentaDeAhorro()
                    mensaje = "Cuenta creada correctamente"
                    variables = {
                        'form': form,
                        'mensaje': mensaje
                    }
        else:
            mensaje = "Error de registro de cuenta"
            variables = {
                'form': form,
                'mensaje': mensaje
            }
    return render(request, "addCuentaPlazoFijo.html", variables)

def crearTarjeta(request):
    form2 = ConsultarTarjetaClientes()
    variables = {
        'cons': form2
    }
    if request.method == "POST":
        form2 = ConsultarTarjetaClientes(data=request.POST)
        if form2.is_valid():
            datos = form2.cleaned_data
            idCliente = datos.get('idCliente')
            marcaRango = datos.get('marca')
            monedaDec = datos.get('codigomoneda')
            tipoCliente = 0
            consCliente = Clienteindividual.objects.filter(cui=idCliente).values_list()
            consEmpresa = Empresa.objects.filter(idempresa=idCliente).values_list()

            if consCliente:
                tipoCliente = '1'  #cliente individual
                consultarTarjeta = Tarjetadecredito.objects.filter(cuicliente=idCliente).values_list()
                if consultarTarjeta:
                    lsCuentas = Detalleclientecuenta.objects.filter(codigocliente=idCliente).filter(
                        codigocuentamonetaria__isnull=False).values_list()  # codigo cuenta no sea null
                    lista = []
                    for numeroCuenta in lsCuentas:
                        lista.append((numeroCuenta[3], numeroCuenta[3]))
                    numeroTarjeta  = len(consultarTarjeta)
                    calc = Calculos()
                    maximo2,minimo2 = calc.limiteCredito(marcaRango, tipoCliente, monedaDec, numeroTarjeta)
                    listaMarca = []
                    if marcaRango == '1':
                        listaMarca.append(('1', "PREFEPUNTOS"))
                    else:
                        listaMarca.append(('2', "CASHBACK"))
                    listaMoneda = []
                    if monedaDec == '1':
                        listaMoneda.append(('1', "Quetzal"))
                    else:
                        listaMoneda.append(('2', "Dolar"))

                    if monedaDec == '1':
                        form = Tarjeta(lista, listaMarca, listaMoneda, maximo2, minimo2, "Q")
                    elif monedaDec == '2':
                        form = Tarjeta(lista, listaMarca, listaMoneda, maximo2, minimo2, "$")

                    variables = {
                        'form': form,
                        'cons': form2,
                        'lista': consultarTarjeta
                    }
                else:
                    lsCuentas = Detalleclientecuenta.objects.filter(codigocliente=idCliente).filter(
                        codigocuentamonetaria__isnull=False).values_list()  # verificar si tiene cuentas monetarias
                    lista = []
                    if len(lsCuentas) != 0:
                        for numCuenta in lsCuentas:
                            lista.append((numCuenta[3], numCuenta[3]))
                    else:
                        lista.append(
                            ("No posee cuentas monetarias", "No posee cuentas monetarias"))  # mostrar en el select

                    numeroTarjeta = len(consultarTarjeta)
                    calc = Calculos()
                    maximo, minimo = calc.limiteCredito(marcaRango, tipoCliente, monedaDec, numeroTarjeta)

                    listaMarca = []
                    if marcaRango == '1':
                        listaMarca.append(('1', "PREFEPUNTOS"))
                    else:
                        listaMarca.append(('2', "CASHBACK"))
                    listaMoneda = []
                    if monedaDec == '1':
                        listaMoneda.append(('1', "Quetzal"))
                    else:
                        listaMoneda.append(('2', "Dolar"))

                    if monedaDec == '1':
                        form = Tarjeta(lista, listaMarca, listaMoneda, maximo, minimo, "Q")
                    elif monedaDec == '2':
                        form = Tarjeta(lista, listaMarca, listaMoneda, maximo, minimo, "$")
                    variables = {
                        'cons': form2,
                        'mensaje': "No se encontraron registros de tarjetas",
                        'form': form
                    }
            elif consEmpresa:
                tipoCliente = '2'  #empresa
                consultarTarjeta = Tarjetadecredito.objects.filter(idempresa=idCliente).values_list()
                if consultarTarjeta:
                    lsCuentas = Detalleclientecuenta.objects.filter(idempresa=idCliente).filter(codigocuentamonetaria__isnull=False).values_list() #codigo cuenta no sea null
                    lista = []
                    for numCuenta in lsCuentas:
                        lista.append((numCuenta[3], numCuenta[3]))

                    numeroTarjeta  = len(consultarTarjeta)
                    calc = Calculos()
                    maximo2,minimo2 = calc.limiteCredito(marcaRango, tipoCliente, monedaDec, numeroTarjeta)

                    listaMarca = []
                    if marcaRango == '1':
                        listaMarca.append(('1', "PREFEPUNTOS"))
                    else:
                        listaMarca.append(('2', "CASHBACK"))
                    listaMoneda = []
                    if monedaDec == '1':
                        listaMoneda.append(('1', "Quetzal"))
                    else:
                        listaMoneda.append(('2', "Dolar"))

                    if monedaDec == '1':
                        form = Tarjeta(lista, listaMarca, listaMoneda, maximo2, minimo2, "Q")
                    elif monedaDec == '2':
                        form = Tarjeta(lista, listaMarca, listaMoneda, maximo2, minimo2, "$")

                    variables={
                        'form': form,
                        'cons': form2,
                        'lista': consultarTarjeta
                    }
                else:  #no tiene tarjetas registradas
                    lsCuentas = Detalleclientecuenta.objects.filter(idempresa=idCliente).filter(codigocuentamonetaria__isnull=False).values_list() #verificar si tiene cuentas monetarias
                    lista = []
                    if len(lsCuentas) != 0:
                        for numCuenta in lsCuentas:
                            lista.append((numCuenta[3], numCuenta[3]))
                    else:
                        lista.append(("No posee cuentas monetarias", "No posee cuentas monetarias")) #mostrar en el select
                    #maximo = 0
                    #minimo = 0
                    numeroTarjeta  = len(consultarTarjeta)
                    calc = Calculos()
                    maximo,minimo = calc.limiteCredito(marcaRango, tipoCliente, monedaDec, numeroTarjeta)

                    listaMarca = []
                    if marcaRango == '1':
                        listaMarca.append(('1', "PREFEPUNTOS"))
                    else:
                        listaMarca.append(('2', "CASHBACK"))
                    listaMoneda = []
                    if monedaDec == '1':
                        listaMoneda.append(('1', "Quetzal"))
                    else:
                        listaMoneda.append(('2', "Dolar"))

                    if monedaDec == '1':
                        form = Tarjeta(lista, listaMarca, listaMoneda, maximo, minimo, "Q")
                    elif monedaDec == '2':
                        form = Tarjeta(lista, listaMarca, listaMoneda, maximo, minimo, "$")
                    variables = {
                        'cons': form2,
                        'mensaje': "No se encontraron registros de tarjetas",
                        'form': form
                    }
            else:
                variables = {
                    'cons': form2,
                    'invalidUsr': "Usuario inexistente",
                }
        if request.method == 'POST':
            print("Entro al pooost")
            form = Tarjeta("","","",None,None,"",data=request.POST)
            if form.is_valid():
                print("validooooo")
                datos = form.cleaned_data
                numeroTarjeta = datos.get('numeroTarjeta')
                marca = datos.get('marca')
                tipoCliente = datos.get('tipoCliente')
                idCliente2 = datos.get('idCliente')
                limiteCredito = datos.get('limiteCredito')
                cantTarjeta = datos.get('cantidadTarjetas')
                numeroCuenta = datos.get('numeroCuenta')
                codigoMoneda = datos.get('moneda')
                print("monedaaaaa", codigoMoneda)
                print(idCliente2)
                print("moneda tye", type(codigoMoneda))
                print(type(idCliente2))
                db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
                cursor = db.cursor()
                if tipoCliente == "1":
                    if marca == "1":
                        consulta = "INSERT INTO TarjetaDeCredito(numeroTarjeta, codigoMarca, codigoTipoCliente, cuiCliente," \
                                   " puntos, limiteCredito, saldo, cantidadTarjetas, numeroCuenta, codigoMoneda) VALUES ("+str(numeroTarjeta)+", "+marca+\
                                   ","+tipoCliente+","+str(idCliente2)+",0,"+str(limiteCredito)+", 0, "+cantTarjeta+", "+numeroCuenta+", "+str(codigoMoneda)+")"
                    else:
                        consulta = "INSERT INTO TarjetaDeCredito(numeroTarjeta, codigoMarca, codigoTipoCliente, cuiCliente," \
                                   " cashback, limiteCredito, saldo, cantidadTarjetas, numeroCuenta, codigoMoneda) VALUES ("+str(numeroTarjeta)+", "+marca+\
                                   ","+tipoCliente+","+str(idCliente2)+",0,"+str(limiteCredito)+", 0, "+cantTarjeta+", "+numeroCuenta+", "+str(codigoMoneda)+")"
                else:
                    if marca == "1":
                        consulta = "INSERT INTO TarjetaDeCredito(numeroTarjeta, codigoMarca, codigoTipoCliente, idEmpresa, " \
                               "puntos, limiteCredito, saldo, cantidadTarjetas, numeroCuenta, codigoMoneda) VALUES ("+str(numeroTarjeta)+", "+marca+\
                                   ","+tipoCliente+","+str(idCliente2)+",0,"+str(limiteCredito)+", 0, "+cantTarjeta+", "+numeroCuenta+", "+str(codigoMoneda)+")"
                    else:
                        consulta = "INSERT INTO TarjetaDeCredito(numeroTarjeta, codigoMarca, codigoTipoCliente, idEmpresa, " \
                               "cashback, limiteCredito, saldo, cantidadTarjetas, numeroCuenta, codigoMoneda) VALUES ("+str(numeroTarjeta)+", "+marca+\
                                   ","+tipoCliente+","+str(idCliente2)+",0,"+str(limiteCredito)+", 0, "+cantTarjeta+", "+numeroCuenta+", "+str(codigoMoneda)+")"
                print(consulta)
                cursor.execute(consulta)
                db.commit()
                cursor.close()

                form2 = ConsultarTarjetaClientes()
                variables = {
                    'cons': form2,
                    'mensaje': "Tarjeta registrada correctamente"
                }
            else:
                print("forn no valido")


    return render(request, 'creartarjeta.html', variables)


def listarSolicitudes(request):
    solicitudes = Prestamo.objects.filter(aprobado=False).values_list()
    #print(solicitudes)
    variables = {
        'lista': solicitudes
    }
    return render(request, "listarSolicitudesPrestamos.html", variables)


def aprobarPrestamo(request, idPrestamo):
    print(idPrestamo)
    solicitudes = Prestamo.objects.filter(codigoprestamo=idPrestamo).values_list()
    cuenta = solicitudes[0][6]
    monto = solicitudes[0][1]

    monet = Cuentamonetaria.objects.filter(codigocuenta=cuenta).values_list()
    ahor = Cuentadeahorro.objects.filter(codigocuenta=cuenta).values_list()
    plz = Cuentaplazofijo.objects.filter(codigocuenta=cuenta).values_list()

    if monet:
        saldoActual = monet[0][3]
        saldoTotal = float(saldoActual + monto)
        db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
        cursor = db.cursor()
        consulta = "update CuentaMonetaria set saldo="+str(saldoTotal)+" where codigoCuenta="+str(cuenta)+""
        cursor.execute(consulta)
        db.commit()
        cursor.close()
    elif ahor:
        saldoActual = monet[0][3]
        saldoTotal = float(saldoActual + monto)
        db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
        cursor = db.cursor()
        consulta = "update CuentaMonetaria set saldo="+str(saldoTotal)+" where codigoCuenta="+str(cuenta)+""
        cursor.execute(consulta)
        db.commit()
        cursor.close()
    elif plz:
        saldoActual = monet[0][4]
        saldoTotal = float(saldoActual + monto)
        db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
        cursor = db.cursor()
        consulta = "update CuentaMonetaria set saldo="+str(saldoTotal)+" where codigoCuenta="+str(cuenta)+""
        cursor.execute(consulta)
        db.commit()
        cursor.close()

    db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
    cursor = db.cursor()
    consulta = "update Prestamo set aprobado=" + str(True) + " where codigoPrestamo=" + str(idPrestamo) + ""
    cursor.execute(consulta)
    db.commit()
    cursor.close()

    return redirect('listarPrestamo')