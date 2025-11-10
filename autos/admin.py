from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Marca, Producto, Cliente, CustomUser

@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)



@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'modelo', 'precio', 'stock')
    list_filter = ('modelo',)
    search_fields = ('nombre',)

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('ruc', 'nombre', 'apellido', 'telefono', 'email')
    search_fields = ('ruc', 'nombre', 'apellido')

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    
    # ← AGREGAR ESTO (esta es la parte que faltaba)
    fieldsets = UserAdmin.fieldsets + (
        ('Información Adicional', {
            'fields': ('role', 'phone', 'address')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información Adicional', {
            'fields': ('role', 'phone', 'address')
        }),
    )