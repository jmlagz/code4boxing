from django.db import models

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