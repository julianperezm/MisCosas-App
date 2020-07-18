from django.db import models
from django.utils import timezone


# Create your models here.
class Alimentador(models.Model):
    alimentadorId = models.CharField(max_length=64, default="")
    nombre = models.CharField(max_length=64, default="")
    enlace = models.CharField(max_length=64, default="")
    puntuacion = models.IntegerField(default=0)
    type = models.CharField(max_length=64,default="")
    pagPrincipal = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Item(models.Model):
    nombre = models.CharField(max_length=64, default="")
    enlace = models.CharField(max_length=64, default="yo ")
    itemId = models.CharField(max_length=64, default="")
    fotoItem = models.CharField(max_length=64, default="")
    descripcion = models.TextField(blank=False, default="")
    votosPositivos = models.IntegerField(default=0)
    votosNegativos = models.IntegerField(default=0)
    votosTotales = models.IntegerField(default=0)
    alimentador = models.ForeignKey(Alimentador, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class Users(models.Model):
    username = models.CharField(max_length=64, default="")
    email = models.EmailField(max_length=64, default="")
    password = models.CharField(max_length=64, default="")
    image = models.ImageField(upload_to='Users', null=True, default="")

    tamañoletra = models.CharField(max_length=64, default="")
    estilo = models.CharField(max_length=64, default="")

    def __str__(self):
        return self.username + " " + self.email + " " + self.password


class Voto(models.Model):
    usuario = models.ForeignKey(Users, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    estado = models.CharField(max_length=64, default="")


class Comentario(models.Model):
    usuario = models.ForeignKey(Users, on_delete=models.CASCADE)
    fecha = models.DateTimeField(default=timezone.now)
    cuerpo = models.TextField(blank=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='Comments', null=True, default="")