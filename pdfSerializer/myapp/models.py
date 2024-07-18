from django.db import models

class Certificado(models.Model):
    nombre = models.CharField(max_length=100)
    nif = models.CharField()
    n_serie = models.CharField(max_length=255, primary_key=True)
    fecha_alta = models.DateTimeField()
    fecha_baja = models.DateTimeField()
    certificado = models.TextField()

    def __str__(self):
        return self.nombre

class Solicitud(models.Model):
    ESTADOS = (
        ('en_proceso', 'En proceso'),
        ('aceptada', 'Aceptada'),
        # Añadir más estados según sea necesario
    )
    nombre = models.CharField(max_length=100)
    nif = models.CharField()
    public_key = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    n_serie = models.CharField(max_length=255, primary_key=True)
    estado_solicitud = models.CharField(max_length=50, choices=ESTADOS, default='en_proceso')

    def __str__(self):
        return self.nombre
