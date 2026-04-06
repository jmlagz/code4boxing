from django.db import models
from django.contrib.auth.models import User


# 🔑 GYM (multi-tenant)
class Gym(models.Model):
    nombre = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class Cliente(models.Model):
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]

    TIPO_INSCRIPCION = [
        ('clase', 'Por clase'),
        ('mensual', 'Mensual'),
        ('anual', 'Anual'),
    ]

    # 🔥 NUEVO: multi-tenant
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)

    # 🔥 NUEVO: auditoría
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='clientes_creados')
    actualizado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='clientes_actualizados')

    # 🔥 NUEVO: CURP
    curp = models.CharField(max_length=18)

    class Meta:
        unique_together = ('gym', 'curp')

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()

    genero = models.CharField(max_length=1, choices=GENERO_CHOICES)

    telefono = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)

    direccion = models.TextField(blank=True, null=True)

    contacto_emergencia = models.CharField(max_length=200)

    certificado_medico = models.FileField(upload_to='certificados/', blank=True, null=True)
    documento_adicional = models.FileField(upload_to='documentos/', blank=True, null=True)

    tipo_inscripcion = models.CharField(max_length=10, choices=TIPO_INSCRIPCION)
    fecha_inscripcion = models.DateField(auto_now_add=True)

    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


# 🔑 PAGOS (multi-tenant)
class Pago(models.Model):
    METODO_PAGO = [
        ('efectivo', 'Efectivo'),
        ('transferencia', 'Transferencia'),
        ('tarjeta', 'Tarjeta'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    registrado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    monto = models.DecimalField(max_digits=8, decimal_places=2)
    metodo = models.CharField(max_length=20, choices=METODO_PAGO)

    fecha_pago = models.DateTimeField(auto_now_add=True)

    # 🔥 opcional pero poderoso
    concepto = models.CharField(max_length=100, default="Mensualidad")