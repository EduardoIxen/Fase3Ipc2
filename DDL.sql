create database Proyecto;
use Proyecto;

create table ClienteIndividual(
	cui bigint primary key not null,
    nit varchar(20) not null,
    nombreCompleto varchar(50) not null,
    fechaNacimiento date not null,
    usuario varchar(50) not null,
    contrasenia varchar(100) not null
);
create table TipoEmpresa(
	idTipoEmpresa int primary key auto_increment not null,
    nombre varchar(50) not null,
    descripcion varchar(255) null
);
create table Empresa(
	idEmpresa bigint primary key auto_increment not null,
    idTipoEmpresa int not null,
    nombre varchar(50) not null,
    nombreComercial varchar(50) not null,
    nombreRepresentanteLegal varchar(50) not null,
    usuario varchar(50) not null,
    contrasenia varchar(100) not null,
    foreign key(idTipoEmpresa) references TipoEmpresa(idTipoEmpresa)
);
create table Administrador(
	idAdministrador int primary key auto_increment not null,
    usuario varchar(100) not null,
    contrasenia varchar(100) not null
);
create table Moneda(
	codigoMoneda int auto_increment primary key,
    nombre varchar(50) not null
);
create table CuentaMonetaria(
	codigoCuenta bigint primary key not null,
    codigoMoneda int not null,
    montoPorManejo numeric(5,2),
    saldo numeric(15,2) not null,
    foreign key(codigoMoneda) references Moneda(codigoMoneda)
);

create table CuentaDeAhorro(
	codigoCuenta bigint primary key not null,
    codigoMoneda int not null,
    tasaInteres int not null,
    saldo numeric(15,2) not null,
    foreign key(codigoMoneda) references Moneda(codigoMoneda)
);
create table CuentaPlazoFijo(
	codigoCuenta bigint primary key not null,
    codigoMoneda int not null,
    tasaInteres int not null,
    periodoDeTiempo int not null,
    saldo numeric(15,2) not null,
    foreign key(codigoMoneda) references Moneda(codigoMoneda)
);

create table DetalleClienteCuenta(
	codigoDetalle int not null primary key auto_increment,
	codigoCliente bigint null,
    idEmpresa bigint null,
    codigoCuentaMonetaria bigint null,
    codigoCuentaAhorro bigint null,
    codigoCuentaPlazoFijo bigint null,
    estaActiva boolean not null,
    foreign key(codigoCliente) references ClienteIndividual(cui),
    foreign key(idEmpresa) references Empresa(idEmpresa),
    foreign key(codigoCuentaMonetaria) references CuentaMonetaria(codigoCuenta),
    foreign key(codigoCuentaAhorro) references CuentaDeAhorro(codigoCuenta),
    foreign key(codigoCuentaPlazoFijo) references CuentaPlazoFijo(codigoCuenta)
);

create table Chequera(
	codigoChequera int primary key auto_increment ,
    cantidadDeCheques numeric(2,0) not null,
    codigoCuenta bigint not null,
    foreign key(codigoCuenta) references CuentaMonetaria(codigoCuenta)
);

create table Cheque(
	numeroCheque int primary key,
    codigoChequera int not null,
    foreign key(codigoChequera) references Chequera(codigoChequera)
);
create table AutorizacionCheque(
	numeroCheque int not null,
    cui bigint not null,
    codigoCuenta bigint not null,
    primary key(numeroCheque, cui, codigoCuenta),
    foreign key(numeroCheque) references Cheque(numeroCheque),
    foreign key(cui) references ClienteIndividual(cui),
    foreign key(codigoCuenta) references CuentaMonetaria(codigoCuenta)
);

create table Planilla(
	codigoPlanilla int primary key auto_increment,
    nombre varchar(100) not null,
    idEmpresa bigint not null,
    foreign key(idEmpresa) references Empresa(idEmpresa)
);

create table DetallePlanilla(
	codigoDetalle int auto_increment primary key,
    codigoPlanilla int not null,
    numeroCuenta bigint,
    nombre varchar(100),
    sueldo numeric(15,2),
    formaPago varchar(100),
    foreign key(codigoPlanilla) references Planilla(codigoPlanilla)
);

create table Prestamo(
	codigoPrestamo int primary key auto_increment,
    montoRequerido numeric(15,2) not null,
    modalidadAPagar numeric(2,0) not null,
    codigoCliente bigint,
    idEmpresa bigint,
    descripcion varchar(100),
    cuenta bigint,
    aprobado boolean,
    foreign key(codigoCliente) references ClienteIndividual(cui),
    foreign key(idEmpresa) references Empresa(idEmpresa)
);
create table TipoDeCliente(
	codigoTipoCliente int auto_increment primary key,
    nombre varchar(50) not null
);
create table Marca(
	codigoMarca int auto_increment primary key,
    nombre varchar(50) not null
);
create table TarjetaDeCredito(
	numeroTarjeta bigint primary key,
    codigoMarca int not null,
    codigoTipoCliente int not null,
    cuiCliente bigint,
    idEmpresa bigint,
    codigoMoneda int,
    numeroCuenta bigint,
    puntos int,
    cashback numeric(15,2),
    limiteCredito numeric(15,2) not null,
    saldo numeric(15,2) not null,
    cantidadTarjetas int not null,
    foreign key(codigoMarca) references Marca(codigoMarca),
    foreign key(codigoTipoCliente) references TipoDeCliente(codigoTipoCliente),
	foreign key(cuiCliente) references ClienteIndividual(cui),
    foreign key(idEmpresa) references Empresa(idEmpresa),
    foreign key(numeroCuenta) references CuentaMonetaria(codigoCuenta),
    foreign key(codigoMoneda) references Moneda(codigoMoneda)
);
create table TransaccionTarjeta(
	codigoTransaccion int auto_increment primary key,
    numeroTarjeta bigint not null,
    codigoMoneda int,
    fecha date,
    descipcion varchar(255),
    monto numeric(15,2),
    foreign key(numeroTarjeta) references TarjetaDeCredito(numeroTarjeta),
    foreign key(codigoMoneda) references Moneda(codigoMoneda)
);

insert into TipoEmpresa(nombre, descripcion) values('Sociedad anonima', 'Descripcion pendiente');
insert into TipoEmpresa(nombre, descripcion) values('Compañia limitada', 'Descripcion pendiente');
insert into TipoEmpresa(nombre, descripcion) values('Empresa Individual', 'Descripcion pendiente');
insert into Moneda(nombre) values ('Quetzal');
insert into Moneda(nombre) values ('Dolar');
insert into Administrador(usuario, contrasenia) value('admin','admin');
insert into TipoDeCliente(nombre) values('Cliente Individual');
insert into TipoDeCliente(nombre) values('Empresa');
insert into Marca(nombre) values('PREFEPUNTOS');
insert into Marca(nombre) values('CASHBACK');
insert into Empresa(idTipoEmpresa, nombre, nombreComercial, nombreRepresentanteLegal, usuario, contrasenia) values(1, 'Empre1', 'Empre1.SA', 'Eduardo Ixen', 'empre1', 'asd');
insert into Empresa(idTipoEmpresa, nombre, nombreComercial, nombreRepresentanteLegal, usuario, contrasenia) values(2, 'EmbuLac', 'Embulac.CO', 'Tomas Rucuch', 'embulac', 'asdf');
insert into ClienteIndividual values(2121, 2332233, 'Eduardo Ixen', '1999-02-12', 'eduardo', 'asdff');
insert into ClienteIndividual values(2222, 1211221, 'Tomas Rucuch', '1999-02-12', 'tomas', 'asd');
insert into ClienteIndividual values(3130, 3345461, 'DIEGO FERNANDO CORTEZ LOPEZ', '1990-02-12', 'diegof', 'diegof');
insert into ClienteIndividual values(3131, 9345462, 'KARINA NOHEMI RAMIREZ ORELLANA', '1990-02-12', 'karinan', 'karinan');
insert into ClienteIndividual values(3132, 8345463, 'ANGEL GEOVANY ARAGON PEREZ', '1990-02-12', 'angelg', 'angelg');
insert into ClienteIndividual values(3133, 7345464, 'CARLOS ROBERTO QUIXTAN PEREZ', '1990-02-12', 'carlosr', 'carlosr');
insert into ClienteIndividual values(3134, 6345465, 'ERICK IVAN MAYORGA RODRIGUEZ', '1990-02-12', 'ericki', 'ericki');
insert into ClienteIndividual values(3135, 5345466, 'BYRON ESTUARDO CAAL CATUN', '1990-02-12', 'byrone', 'byrone');
insert into ClienteIndividual values(3136, 4345467, 'RONALD RODRIGO MARIN SALAS', '1990-02-12', 'ronaldr', 'ronaldr');
insert into ClienteIndividual values(3137, 3345468, 'OSCAR DANIEL OLIVA', '1990-02-12', 'oscard', 'oscard');
insert into ClienteIndividual values(3138, 2345469, 'EDUARDO ABRAHAM BARILLAS', '1990-02-12', 'eduardoa', 'eduardoa');
insert into ClienteIndividual values(3139, 1345460, 'CARLOS ESTUARDO MONTERROSO SANTOS', '1990-02-12', 'carlose', 'carlose');
insert into CuentaMonetaria values(541234, 1, 15.00, 0.00);
insert into CuentaMonetaria values(263769, 1, 15.00, 0.00);
insert into CuentaMonetaria values(481366, 1, 15.00, 0.00);
insert into CuentaMonetaria values(152352, 1, 15.00, 0.00);
insert into CuentaMonetaria values(358054, 1, 15.00, 0.00);
insert into CuentaMonetaria values(503944, 1, 15.00, 0.00);
insert into CuentaMonetaria values(316167, 1, 15.00, 0.00);
insert into CuentaMonetaria values(374296, 1, 15.00, 0.00);
insert into CuentaMonetaria values(556658, 1, 15.00, 0.00);
insert into CuentaMonetaria values(462978, 1, 15.00, 0.00);
insert into CuentaMonetaria values(444455, 1, 15.00, 100000.00);
insert into CuentaMonetaria values(223344, 1, 15.00, 100.00);
insert into CuentaDeAhorro values(111222, 1, 5, 200.00);
insert into CuentaPlazoFijo values(333333, 1, 15, 24, 300.00);
insert into DetalleClienteCuenta(idEmpresa, codigoCuentaMonetaria, estaActiva) values(1,444455,True);
insert into DetalleClienteCuenta(codigoCliente, codigoCuentaPlazoFijo, estaActiva) values(2121,333333 ,True);
insert into DetalleClienteCuenta(codigoCliente, codigoCuentaAhorro, estaActiva) values(2121,111222 ,True);
insert into DetalleClienteCuenta(codigoCliente, codigoCuentaMonetaria, estaActiva) values(2121,223344 ,True);
insert into DetalleClienteCuenta(codigoCliente, codigoCuentaMonetaria, estaActiva) values(3130,541234 ,True);
insert into DetalleClienteCuenta(codigoCliente, codigoCuentaMonetaria, estaActiva) values(3131,263769,True);
insert into DetalleClienteCuenta(codigoCliente, codigoCuentaMonetaria, estaActiva) values(3132,481366,True);
insert into DetalleClienteCuenta(codigoCliente, codigoCuentaMonetaria, estaActiva) values(3133,152352,True);
insert into DetalleClienteCuenta(codigoCliente, codigoCuentaMonetaria, estaActiva) values(3134,358054,True);
insert into DetalleClienteCuenta(codigoCliente, codigoCuentaMonetaria, estaActiva) values(3135,503944,True);
insert into DetalleClienteCuenta(codigoCliente, codigoCuentaMonetaria, estaActiva) values(3136,316167,True);
insert into DetalleClienteCuenta(codigoCliente, codigoCuentaMonetaria, estaActiva) values(3137,374296,True);
insert into DetalleClienteCuenta(codigoCliente, codigoCuentaMonetaria, estaActiva) values(3138,556658,True);
insert into DetalleClienteCuenta(codigoCliente, codigoCuentaMonetaria, estaActiva) values(3139,462978,True);