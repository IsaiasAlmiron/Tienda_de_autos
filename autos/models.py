from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class Marca(models.Model):
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=150)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, related_name='productos')
    modelo = models.CharField(max_length=100, blank=True)  # Campo de texto para modelo/version/año
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    
    def __str__(self):
          return f"{self.marca} {self.nombre} ({self.modelo}) - Stock: {self.stock} - ${self.precio}"

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
    

class Venta(models.Model):
    cliente = models.ForeignKey('Cliente', on_delete=models.PROTECT)
    vendedor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Venta #{self.id} a {self.cliente}"


class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey('Producto', on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def get_subtotal(self):
        return self.cantidad * self.precio_unitario
@property
def is_admin(self):
    return self.role == 'admin'