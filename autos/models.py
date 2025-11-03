from django.db import models
from django.contrib.auth.models import AbstractUser

class Marca(models.Model):
    nombre = models.CharField(max_length=100)
    def __str__(self): 
        return self.nombre

class Modelo(models.Model):
    nombre = models.CharField(max_length=100)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, related_name='modelos')
    def __str__(self): 
        return f"{self.marca.nombre} {self.nombre}"

class Producto(models.Model):
    nombre = models.CharField(max_length=150)
    modelo = models.ForeignKey(Modelo, on_delete=models.SET_NULL, null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    def __str__(self): 
        return self.nombre

class Cliente(models.Model):
    ruc = models.CharField(max_length=20, primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    direccion = models.CharField(max_length=200, blank=True)
    def __str__(self): 
        return f"{self.nombre} {self.apellido}"


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Administrador'),
        ('vendedor', 'Vendedor'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='vendedor')
    # Si aún quieres agregar phone y address, debes declararlos aquí
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    

@property
def is_admin(self):
    return self.role == 'admin'