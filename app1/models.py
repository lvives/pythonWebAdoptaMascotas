from django.db import models

# Create your models here.
class TipoMascota(models.Model):
    nombre = models.CharField(max_length=64, null=True, blank=True)
    descripcion = models.TextField(max_length=256, null=True, blank=True)

    def __str__(self):
        return self.nombre


# Mascotas disponibles para adopción
class Mascota(models.Model):
    nombre = models.CharField(max_length=128, null=True, blank=True)
    edad = models.IntegerField()
    descripcion = models.TextField(max_length=512, null=True, blank=True)
    foto = models.ImageField(upload_to="mascotas/")
    tipo = models.ForeignKey(TipoMascota, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, default="Disponible")

    def __str__(self):
        return self.nombre


# Persona que adopta
class Persona(models.Model):
    nombre = models.CharField(max_length=128, null=True, blank=True)
    email = models.CharField(max_length=128, null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.nombre


# Registro de adopciones
class Adopcion(models.Model):
    mascota = models.OneToOneField(Mascota, on_delete=models.CASCADE)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    fecha_adopcion = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.persona.nombre} adoptó a {self.mascota.nombre}"