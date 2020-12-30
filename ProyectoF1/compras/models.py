# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Administrador(models.Model):
    idadministrador = models.AutoField(db_column='idAdministrador', primary_key=True)  # Field name made lowercase.
    usuario = models.CharField(max_length=100)
    contrasenia = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'administrador'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Autorizacioncheque(models.Model):
    numerocheque = models.OneToOneField('Cheque', models.DO_NOTHING, db_column='numeroCheque', primary_key=True)  # Field name made lowercase.
    cui = models.ForeignKey('Clienteindividual', models.DO_NOTHING, db_column='cui')
    codigocuenta = models.ForeignKey('Cuentamonetaria', models.DO_NOTHING, db_column='codigoCuenta')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'autorizacioncheque'
        unique_together = (('numerocheque', 'cui', 'codigocuenta'),)


class Cheque(models.Model):
    numerocheque = models.IntegerField(db_column='numeroCheque', primary_key=True)  # Field name made lowercase.
    codigochequera = models.ForeignKey('Chequera', models.DO_NOTHING, db_column='codigoChequera')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'cheque'


class Chequera(models.Model):
    codigochequera = models.AutoField(db_column='codigoChequera', primary_key=True)  # Field name made lowercase.
    cantidaddecheques = models.DecimalField(db_column='cantidadDeCheques', max_digits=2, decimal_places=0)  # Field name made lowercase.
    codigocuenta = models.ForeignKey('Cuentamonetaria', models.DO_NOTHING, db_column='codigoCuenta')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'chequera'


class Clienteindividual(models.Model):
    cui = models.BigIntegerField(primary_key=True)
    nit = models.CharField(max_length=20)
    nombrecompleto = models.CharField(db_column='nombreCompleto', max_length=50)  # Field name made lowercase.
    fechanacimiento = models.DateField(db_column='fechaNacimiento')  # Field name made lowercase.
    usuario = models.CharField(max_length=50)
    contrasenia = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'clienteindividual'


class Cuentadeahorro(models.Model):
    codigocuenta = models.BigIntegerField(db_column='codigoCuenta', primary_key=True)  # Field name made lowercase.
    codigomoneda = models.ForeignKey('Moneda', models.DO_NOTHING, db_column='codigoMoneda')  # Field name made lowercase.
    tasainteres = models.IntegerField(db_column='tasaInteres')  # Field name made lowercase.
    saldo = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'cuentadeahorro'


class Cuentamonetaria(models.Model):
    codigocuenta = models.BigIntegerField(db_column='codigoCuenta', primary_key=True)  # Field name made lowercase.
    codigomoneda = models.ForeignKey('Moneda', models.DO_NOTHING, db_column='codigoMoneda')  # Field name made lowercase.
    montopormanejo = models.DecimalField(db_column='montoPorManejo', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    saldo = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'cuentamonetaria'


class Cuentaplazofijo(models.Model):
    codigocuenta = models.BigIntegerField(db_column='codigoCuenta', primary_key=True)  # Field name made lowercase.
    codigomoneda = models.ForeignKey('Moneda', models.DO_NOTHING, db_column='codigoMoneda')  # Field name made lowercase.
    tasainteres = models.IntegerField(db_column='tasaInteres')  # Field name made lowercase.
    periododetiempo = models.IntegerField(db_column='periodoDeTiempo')  # Field name made lowercase.
    saldo = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'cuentaplazofijo'


class Detalleclientecuenta(models.Model):
    codigodetalle = models.AutoField(db_column='codigoDetalle', primary_key=True)  # Field name made lowercase.
    codigocliente = models.ForeignKey(Clienteindividual, models.DO_NOTHING, db_column='codigoCliente', blank=True, null=True)  # Field name made lowercase.
    idempresa = models.ForeignKey('Empresa', models.DO_NOTHING, db_column='idEmpresa', blank=True, null=True)  # Field name made lowercase.
    codigocuentamonetaria = models.ForeignKey(Cuentamonetaria, models.DO_NOTHING, db_column='codigoCuentaMonetaria', blank=True, null=True)  # Field name made lowercase.
    codigocuentaahorro = models.ForeignKey(Cuentadeahorro, models.DO_NOTHING, db_column='codigoCuentaAhorro', blank=True, null=True)  # Field name made lowercase.
    codigocuentaplazofijo = models.ForeignKey(Cuentaplazofijo, models.DO_NOTHING, db_column='codigoCuentaPlazoFijo', blank=True, null=True)  # Field name made lowercase.
    estaactiva = models.IntegerField(db_column='estaActiva')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'detalleclientecuenta'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Empresa(models.Model):
    idempresa = models.BigAutoField(db_column='idEmpresa', primary_key=True)  # Field name made lowercase.
    idtipoempresa = models.ForeignKey('Tipoempresa', models.DO_NOTHING, db_column='idTipoEmpresa')  # Field name made lowercase.
    nombre = models.CharField(max_length=50)
    nombrecomercial = models.CharField(db_column='nombreComercial', max_length=50)  # Field name made lowercase.
    nombrerepresentantelegal = models.CharField(db_column='nombreRepresentanteLegal', max_length=50)  # Field name made lowercase.
    usuario = models.CharField(max_length=50)
    contrasenia = models.CharField(max_length=100)

    def __str__(self):
        # return '{} {}'.format(self.idtipoempresa, self.nombre)
        return '{}'.format(self.nombre)

    class Meta:
        managed = False
        db_table = 'empresa'


class Marca(models.Model):
    codigomarca = models.AutoField(db_column='codigoMarca', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=50)

    def __str__(self):
        # return '{} {}'.format(self.idtipoempresa, self.nombre)
        return '{}'.format(self.nombre)

    class Meta:
        managed = False
        db_table = 'marca'


class Moneda(models.Model):
    codigomoneda = models.AutoField(db_column='codigoMoneda', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'moneda'


class Prestamo(models.Model):
    codigoprestamo = models.AutoField(db_column='codigoPrestamo', primary_key=True)  # Field name made lowercase.
    montorequerido = models.DecimalField(db_column='montoRequerido', max_digits=15, decimal_places=2)  # Field name made lowercase.
    modalidadapagar = models.DecimalField(db_column='modalidadAPagar', max_digits=2, decimal_places=0)  # Field name made lowercase.
    codigocliente = models.ForeignKey(Clienteindividual, models.DO_NOTHING, db_column='codigoCliente', blank=True, null=True)  # Field name made lowercase.
    idempresa = models.ForeignKey(Empresa, models.DO_NOTHING, db_column='idEmpresa', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'prestamo'


class Tarjetadecredito(models.Model):
    numerotarjeta = models.BigIntegerField(db_column='numeroTarjeta', primary_key=True)  # Field name made lowercase.
    codigomarca = models.ForeignKey(Marca, models.DO_NOTHING, db_column='codigoMarca')  # Field name made lowercase.
    codigotipocliente = models.ForeignKey('Tipodecliente', models.DO_NOTHING, db_column='codigoTipoCliente')  # Field name made lowercase.
    cuicliente = models.ForeignKey(Clienteindividual, models.DO_NOTHING, db_column='cuiCliente', blank=True, null=True)  # Field name made lowercase.
    idempresa = models.ForeignKey(Empresa, models.DO_NOTHING, db_column='idEmpresa', blank=True, null=True)  # Field name made lowercase.
    codigomoneda = models.ForeignKey(Moneda, models.DO_NOTHING, db_column='codigoMoneda', blank=True, null=True)  # Field name made lowercase.
    numerocuenta = models.ForeignKey(Cuentamonetaria, models.DO_NOTHING, db_column='numeroCuenta', blank=True, null=True)  # Field name made lowercase.
    puntos = models.IntegerField(blank=True, null=True)
    cashback = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    limitecredito = models.DecimalField(db_column='limiteCredito', max_digits=15, decimal_places=2)  # Field name made lowercase.
    saldo = models.DecimalField(max_digits=15, decimal_places=2)
    cantidadtarjetas = models.IntegerField(db_column='cantidadTarjetas')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tarjetadecredito'


class Tipodecliente(models.Model):
    codigotipocliente = models.AutoField(db_column='codigoTipoCliente', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=50)

    def __str__(self):
        # return '{} {}'.format(self.idtipoempresa, self.nombre)
        return '{}'.format(self.nombre)

    class Meta:
        managed = False
        db_table = 'tipodecliente'


class Tipoempresa(models.Model):
    idtipoempresa = models.AutoField(db_column='idTipoEmpresa', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        # return '{} {}'.format(self.idtipoempresa, self.nombre)
        return '{}'.format(self.nombre)

    class Meta:
        managed = False
        db_table = 'tipoempresa'


class Transacciontarjeta(models.Model):
    codigotransaccion = models.AutoField(db_column='codigoTransaccion', primary_key=True)  # Field name made lowercase.
    numerotarjeta = models.ForeignKey(Tarjetadecredito, models.DO_NOTHING, db_column='numeroTarjeta')  # Field name made lowercase.
    codigomoneda = models.ForeignKey(Moneda, models.DO_NOTHING, db_column='codigoMoneda')  # Field name made lowercase.
    fecha = models.DateField(blank=True, null=True)
    descipcion = models.CharField(max_length=255, blank=True, null=True)
    monto = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'transacciontarjeta'


class Planilla(models.Model):
    codigoplanilla = models.AutoField(db_column='codigoPlanilla', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=100)
    idempresa = models.ForeignKey(Empresa, models.DO_NOTHING, db_column='idEmpresa')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'planilla'


class Detalleplanilla(models.Model):
    codigodetalle = models.AutoField(db_column='codigoDetalle', primary_key=True)  # Field name made lowercase.
    codigoplanilla = models.ForeignKey('Planilla', models.DO_NOTHING,
                                       db_column='codigoPlanilla')  # Field name made lowercase.
    numerocuenta = models.BigIntegerField(db_column='numeroCuenta', blank=True, null=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=100, blank=True, null=True)
    sueldo = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    formapago = models.CharField(db_column='formaPago', max_length=100, blank=True,
                                 null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'detalleplanilla'
