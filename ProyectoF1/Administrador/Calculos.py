class Calculos:
    def limiteCredito(self, marcaRango, tipoCliente, monedaDec, numeroTarjeta):
        maximo = 0
        minimo = 0
        if numeroTarjeta == 0:
            if marcaRango == '1':
                if tipoCliente == "1":
                    if monedaDec == '1':
                        maximo = 7000.00
                        minimo = 5000.00
                    else:
                        maximo = 7000.00 / 7.63
                        minimo = 5000.00 / 7.63
                elif tipoCliente == '2':
                    if monedaDec == '1':
                        maximo = 15000.00
                        minimo = 10000.00
                    else:
                        maximo = 15000.00 / 7.63
                        minimo = 10000.00 / 7.63
            elif marcaRango == '2':
                if tipoCliente == "1":
                    if monedaDec == '1':
                        maximo = 7000.00
                        minimo = 5000.00
                    else:
                        maximo = 7000.00 / 7.87
                        minimo = 5000.00 / 7.87
                elif tipoCliente == '2':
                    if monedaDec == '1':
                        print("Entro empresa conversion")
                        maximo = 15000.00
                        minimo = 10000.00
                    else:
                        maximo = 15000.00 / 7.87
                        minimo = 10000.00 / 7.87
        elif numeroTarjeta == 1:
            if marcaRango == '1':
                if tipoCliente == "1":  #cliente individual
                    if monedaDec == '1':   #quetzal
                        maximo = 5500.00
                        minimo = 4500.00
                    else:  #dolar
                        maximo = 5500.00 / 7.63
                        minimo = 4500.00 / 7.63
                elif tipoCliente == '2':   #empresa
                    if monedaDec == '1':  #quetzal
                        maximo = 17000.00
                        minimo = 12000.00
                    else:   #dolar
                        maximo = 17000.00 / 7.63
                        minimo = 12000.00 / 7.63
            elif marcaRango == '2':
                if tipoCliente == "1":
                    if monedaDec == '1':
                        maximo = 7000.00
                        minimo = 5000.00
                    else:
                        maximo = 7000.00 / 7.87
                        minimo = 5000.00 / 7.87
                elif tipoCliente == '2':
                    if monedaDec == '1':
                        print("Entro empresa conversion")
                        maximo = 17000.00
                        minimo = 12000.00
                    else:
                        maximo = 17000.00 / 7.87
                        minimo = 12000.00 / 7.87
        elif numeroTarjeta == 2:
            if marcaRango == '1':
                if tipoCliente == "1":  #cliente individual
                    if monedaDec == '1':   #quetzal
                        maximo = 4000.00
                        minimo = 3500.00
                    else:  #dolar
                        maximo = 4000.00 / 7.63
                        minimo = 3500.00 / 7.63
                elif tipoCliente == '2':   #empresa
                    if monedaDec == '1':  #quetzal
                        maximo = 19000.00
                        minimo = 15000.00
                    else:   #dolar
                        maximo = 19000.00 / 7.63
                        minimo = 15000.00 / 7.63
            elif marcaRango == '2':
                if tipoCliente == "1":
                    if monedaDec == '1':
                        maximo = 4000.00
                        minimo = 3500.00
                    else:
                        maximo = 4000.00 / 7.87
                        minimo = 3500.00 / 7.87
                elif tipoCliente == '2':
                    if monedaDec == '1':
                        print("Entro empresa conversion")
                        maximo = 19000.00
                        minimo = 15000.00
                    else:
                        maximo = 19000.00 / 7.87
                        minimo = 15000.00 / 7.87

        return (f"{maximo:.2f}", f"{minimo:.2f}")
