import MySQLdb
from django.shortcuts import render, redirect
from .forms import *
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import datetime

host = 'localhost'
db_name = 'Proyecto'
user = 'root'
contra = 'admin'
puerto = 3306

# Create your views here.
def login(request):
    form = loginF()
    mensaje = ""
    variables = {
        'form': form,
        'mensaje': mensaje,
        'usuariologueado': ''
    }
    if request.method == "POST":
        form = loginF(data=request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            usuario = datos.get('usuario')
            password = datos.get('contrasenia')

        #usuario = request.POST['usuariolog']
        #password = request.POST['passwordlog']
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
                form = loginF()
            variables = {
                'form':form,
                'mensaje': mensaje,
            }
    return render(request, "loginCompras.html", variables)

def home(request):
    dic = request.session['datos']
    if dic.get('cui') != None:
        idUsuario = dic.get('cui')
        nombre = dic.get('nombre')
    elif dic.get('idEmpresa') != None:
        idUsuario = dic.get('idEmpresa')
        nombre = dic.get('nombre')

    productos = [{'producto': 'Camisa', 'Precio': 125, 'Moneda': 'Quetzal', 'Descripcion': 'Camisa de maga larga, color gris sin bolsa en el pecho.'},
                 {'producto': 'Pantalon', 'Precio': 160, 'Moneda': 'Quetzal', 'Descripcion': 'Pantalon de mezclilla color azul, corte recto para hombre'},
                 {'producto': 'Zapato', 'Precio': 75, 'Moneda': 'Dolar', 'Descripcion': 'Zapato de cuero color negro, suela de goma sin cordones'},
                 {'producto': 'Reloj', 'Precio': 200, 'Moneda': 'Dolar', 'Descripcion': 'Reloj digital Casio, cobertura de plástico resistente'}
                 ]
    listaProd = []
    for producto in productos:
        if producto['Moneda'] == "Quetzal":
            listaProd.append((f"{producto['producto']} Q{producto['Precio']}", f"{producto['producto']} Q{producto['Precio']}"))
        elif producto['Moneda'] == "Dolar":
            listaProd.append(
                (f"{producto['producto']} ${producto['Precio']}", f"{producto['producto']} ${producto['Precio']}"))
    print(listaProd)
    form = consultarProducto(listaProd)
    variables = {
        'form': form,
        'nombreUsr':nombre
    }
    if request.method == "POST":
        form = consultarProducto(listaProd,data=request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            productoObtenido = datos.get('producto')
            print(productoObtenido)
            prod = productoObtenido.split(" ")
            for producto in productos:
                if producto['producto'] == prod[0]:
                    request.session['producto'] = producto

            return redirect('detalleproducto')


    return render(request, "HomeCompra.html", variables)

def logoutCompras(request):
    request.session['datos'] = {}
    dic = request.session['datos']
    nombre = dic.get('nombre')
    print("nombreeeee", nombre)
    return HttpResponseRedirect(reverse('logincomp'))


def detalleProducto(request):
    #obtener cliente
    dic = request.session['datos']
    if dic.get('cui') != None:
        idUsuario = dic.get('cui')
        nombre = dic.get('nombre')
    elif dic.get('idEmpresa') != None:
        idUsuario = dic.get('idEmpresa')
        nombre = dic.get('nombre')
    #obtener producto
    dicProd = request.session['producto']
    producto = dicProd.get('producto')
    precio = dicProd.get('Precio')
    moneda = dicProd.get('Moneda')
    descripcion = dicProd.get('Descripcion')
    direccion = f"img/{producto}.jpg"
    print(f"mandamdo .{producto}.")

    tarjetasUsuario = Tarjetadecredito.objects.filter(cuicliente=idUsuario).values_list()
    tarjetasEmpresa = Tarjetadecredito.objects.filter(idempresa=idUsuario).values_list()
    listaTarjetas = []
    mensaje = ''
    if tarjetasUsuario:
        for tarjeta in tarjetasUsuario:
            marca = Marca.objects.filter(codigomarca=tarjeta[1]).values_list()
            listaTarjetas.append((tarjeta[0], f"{tarjeta[0]} --- {marca[0][1]}"))
        form = Compra(listaTarjetas)
    elif tarjetasEmpresa:
        for tarjeta in tarjetasEmpresa:
            marca = Marca.objects.filter(codigomarca=tarjeta[1]).values_list()
            listaTarjetas.append((tarjeta[0], f"{tarjeta[0]} --- {marca[0][1]}"))
        form = Compra(listaTarjetas)
    else:
        mensaje = "No posee tarjetas de credito"
        form = Compra([])

    variables = {
        'producto': producto,
        'precio': precio,
        'moneda': moneda,
        'descripcion': descripcion,
        'direccion': direccion,
        'form': form,
        'mensaje': mensaje,
        'nombreUsr': nombre
    }
    if request.method == 'POST':
        form = Compra(listaTarjetas, data=request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            numeroTarjeta = datos.get('numeroTarjeta')
            fecha = datos.get('fecha')
            fecha2 = fecha.strftime("%Y-%m-%d")
            descripcion = datos.get('descripcion')
            cantidad = datos.get('cantidad')
            total = 0
            tarjetaConsulta = Tarjetadecredito.objects.filter(numerotarjeta=numeroTarjeta).values_list()
            monetaTarjeta = tarjetaConsulta[0][5]
            marcaTarjeta = tarjetaConsulta[0][1]
            monedaTarjeta = tarjetaConsulta[0][5]

            if monetaTarjeta == 1: #quetzal
                if moneda == "Quetzal":
                    total = precio * cantidad
                    print("total", total)
                elif moneda == "Dolar":
                    if marcaTarjeta == 1:
                        total = (precio * cantidad) * 7.63
                    elif marcaTarjeta == 2:
                        total = (precio * cantidad) * 7.87
            elif monetaTarjeta == 2: #dolar
                if moneda == "Dolar":
                    total = precio * cantidad
                elif moneda == "Quetzal":
                    if marcaTarjeta == 1:
                        total = (precio * cantidad) / 7.63
                    elif marcaTarjeta == 2:
                        total = (precio * cantidad) / 7.87
            print("total final",total)  #total para la db

            saldo = tarjetaConsulta[0][9] - tarjetaConsulta[0][10]
            print("saldo", saldo)
            if total <= saldo:
                #actualizar saldo
                nuevoSaldo = float(tarjetaConsulta[0][10]) + total
                db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
                cursor = db.cursor()
                consulta = "UPDATE TarjetaDeCredito SET saldo="+str(nuevoSaldo)+"  WHERE numeroTarjeta="+str(tarjetaConsulta[0][0])+""
                print(consulta)
                cursor.execute(consulta)
                db.commit()
                cursor.close()

                #insertar transaccion
                db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
                cursor = db.cursor()
                consulta = "INSERT INTO TransaccionTarjeta(numeroTarjeta, codigoMoneda, fecha, descipcion, monto) VALUES" \
                           "("+str(numeroTarjeta)+", "+str(monedaTarjeta)+", '"+fecha2+"', '"+descripcion+"', "+str(total)+")"
                print(consulta)
                cursor.execute(consulta)
                db.commit()
                cursor.close()

                if monetaTarjeta == 1: #Quetzal
                    # puntos o cashback
                    puntosObtenidos = 0
                    cashBack = 0
                    if marcaTarjeta == 1:  # prefepuntos
                        if total > 0.01 and total < 100.00:
                            puntosObtenidos = total * 0
                        elif total > 100.01 and total < 500.00:
                            puntosObtenidos = total * 0.02
                        elif total > 500.01 and total < 2000.00:
                            puntosObtenidos = total * 0.04
                        elif total > 2000.01:
                            puntosObtenidos = total * 0.05
                        if puntosObtenidos > 0:
                            obtenerTarjeta = []
                            obtenerTarjeta = Tarjetadecredito.objects.filter(numerotarjeta=numeroTarjeta).values_list()
                            puntosActuales = 0
                            puntosActuales = obtenerTarjeta[0][7]
                            totalPuntos = 0
                            totalPuntos = puntosActuales + puntosObtenidos

                            db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
                            cursor = db.cursor()
                            consulta = "UPDATE TarjetaDeCredito SET puntos=" + str(
                                totalPuntos) + " WHERE numeroTarjeta=" + str(numeroTarjeta) + ""
                            print(consulta)
                            cursor.execute(consulta)
                            db.commit()
                            cursor.close()
                            # registar transaccion
                            db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
                            cursor = db.cursor()
                            consulta = "INSERT INTO TransaccionTarjeta(numeroTarjeta, fecha, descipcion, monto) VALUES" \
                                       "(" + str(
                                numeroTarjeta) + ", '" + fecha2 + "', 'Puntos por: " + descripcion + "', " + str(
                                puntosObtenidos) + ")"
                            # print(consulta)
                            cursor.execute(consulta)
                            db.commit()
                            cursor.close()
                    elif marcaTarjeta == 2:  # cashback
                        if total >= 0.01 and total <= 200.00:
                            cashBack = total * 0
                        elif total >= 200.01 and total <= 700.00:
                            cashBack = total * 0.02
                        elif total >= 700.01:
                            cashBack = total * 0.05
                        if cashBack > 0:
                            obtenerTarjeta = []
                            obtenerTarjeta = Tarjetadecredito.objects.filter(numerotarjeta=numeroTarjeta).values_list()
                            cashActual = obtenerTarjeta[0][8]
                            cashTotal = 0
                            cashTotal = float(cashActual) + cashBack
                            print()
                            db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
                            cursor = db.cursor()
                            consulta = "UPDATE TarjetaDeCredito SET cashback=" + str(
                                cashTotal) + " WHERE numeroTarjeta=" + str(numeroTarjeta) + ""
                            print(consulta)
                            cursor.execute(consulta)
                            db.commit()
                            cursor.close()

                            saldoActual = obtenerTarjeta[0][10]
                            saldoTotal = float(saldoActual) - cashBack
                            print("actual", saldoActual)
                            print("nuevo", cashBack)
                            print("total", saldoTotal)
                            db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
                            cursor = db.cursor()
                            consulta = "UPDATE TarjetaDeCredito SET saldo=" + str(
                                saldoTotal) + " WHERE numeroTarjeta=" + str(numeroTarjeta) + ""
                            print(consulta)
                            cursor.execute(consulta)
                            db.commit()
                            cursor.close()

                            # registar transaccion
                            db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
                            cursor = db.cursor()
                            consulta = "INSERT INTO TransaccionTarjeta(numeroTarjeta,codigoMoneda ,fecha, descipcion, monto) VALUES" \
                                       "(" + str(numeroTarjeta) + "," + str(
                                monedaTarjeta) + " ,'" + fecha2 + "', 'Transaccion de cashback por: " + descripcion + "', " + str(
                                cashBack) + ")"
                            print(consulta)
                            cursor.execute(consulta)
                            db.commit()
                            cursor.close()
                elif monetaTarjeta == 2: #Dolar
                    # puntos o cashback
                    puntosObtenidos = 0
                    cashBack = 0
                    if marcaTarjeta == 1:  # prefepuntos
                        if total >= 0.01 and total <= 13.11:
                            puntosObtenidos = total * 0
                        elif total >= 13.12 and total <= 65.53:
                            puntosObtenidos = total * 0.02
                        elif total >= 65.54 and total <= 262.12:
                            puntosObtenidos = total * 0.04
                        elif total >= 262.13:
                            puntosObtenidos = total * 0.05
                        if puntosObtenidos > 0:
                            obtenerTarjeta = []
                            obtenerTarjeta = Tarjetadecredito.objects.filter(numerotarjeta=numeroTarjeta).values_list()
                            puntosActuales = 0
                            puntosActuales = obtenerTarjeta[0][7]
                            totalPuntos = 0
                            totalPuntos = puntosActuales + puntosObtenidos

                            db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
                            cursor = db.cursor()
                            consulta = "UPDATE TarjetaDeCredito SET puntos=" + str(
                                totalPuntos) + " WHERE numeroTarjeta=" + str(numeroTarjeta) + ""
                            print(consulta)
                            cursor.execute(consulta)
                            db.commit()
                            cursor.close()
                            # registar transaccion
                            db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
                            cursor = db.cursor()
                            consulta = "INSERT INTO TransaccionTarjeta(numeroTarjeta, fecha, descipcion, monto) VALUES" \
                                       "(" + str(
                                numeroTarjeta) + ", '" + fecha2 + "', 'Puntos por: " + descripcion + "', " + str(
                                puntosObtenidos) + ")"
                            # print(consulta)
                            cursor.execute(consulta)
                            db.commit()
                            cursor.close()
                    elif marcaTarjeta == 2:  # cashback
                        if total >= 0.01 and total <= 25.41:
                            cashBack = total * 0
                        elif total >= 25.42 and total <= 88.95:
                            cashBack = total * 0.02
                        elif total >= 88.96:
                            cashBack = total * 0.05
                        if cashBack > 0:
                            obtenerTarjeta = []
                            obtenerTarjeta = Tarjetadecredito.objects.filter(numerotarjeta=numeroTarjeta).values_list()
                            cashActual = obtenerTarjeta[0][8]
                            cashTotal = 0
                            cashTotal = float(cashActual) + cashBack
                            print()
                            db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
                            cursor = db.cursor()
                            consulta = "UPDATE TarjetaDeCredito SET cashback=" + str(
                                cashTotal) + " WHERE numeroTarjeta=" + str(numeroTarjeta) + ""
                            print(consulta)
                            cursor.execute(consulta)
                            db.commit()
                            cursor.close()

                            saldoActual = obtenerTarjeta[0][10]
                            saldoTotal = float(saldoActual) - cashBack
                            print("actual", saldoActual)
                            print("nuevo", cashBack)
                            print("total", saldoTotal)
                            db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
                            cursor = db.cursor()
                            consulta = "UPDATE TarjetaDeCredito SET saldo=" + str(
                                saldoTotal) + " WHERE numeroTarjeta=" + str(numeroTarjeta) + ""
                            print(consulta)
                            cursor.execute(consulta)
                            db.commit()
                            cursor.close()

                            # registar transaccion
                            db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
                            cursor = db.cursor()
                            consulta = "INSERT INTO TransaccionTarjeta(numeroTarjeta,codigoMoneda ,fecha, descipcion, monto) VALUES" \
                                       "(" + str(numeroTarjeta) + "," + str(
                                monedaTarjeta) + " ,'" + fecha2 + "', 'Transaccion de cashback por: " + descripcion + "', " + str(
                                cashBack) + ")"
                            print(consulta)
                            cursor.execute(consulta)
                            db.commit()
                            cursor.close()

            else:
                print(f"No cuenta con saldo suficiente {total} -- saldo {saldo}")
                mensaje = f"No cuenta con saldo suficiente: Saldo-> {saldo}   Total->{total}"
                mensaje1 = "No saldo"
                variables = {
                    'mensaje': mensaje,
                    'form': form,
                    'producto': producto,
                    'precio': precio,
                    'moneda': moneda,
                    'descripcion': descripcion,
                    'direccion': direccion,
                    'mensaje2': mensaje1,
                    'nombreUsr': nombre
                }

    return render(request, "detalleProducto.html", variables)