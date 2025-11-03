from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from autos import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Página de inicio
    path('', views.index, name='index'),

    # URLs de la app
    path('', include('autos.urls')),

    # Login / logout de Django
    path('accounts/', include('django.contrib.auth.urls')),




     
    # Gestión de usuarios (solo admin)
    path('usuarios/crear/', views.crear_usuario, name='crear_usuario'),
    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    
    path('usuarios/<int:pk>/editar/', views.editar_usuario, name='editar_usuario'),  # ← NUEVA
    path('usuarios/<int:pk>/eliminar/', views.eliminar_usuario, name='eliminar_usuario'),  # ← NUEVA
    
    # Exportar a CSV
    path('exportar/productos/csv/', views.exportar_productos_csv, name='exportar_productos_csv'),
    path('exportar/clientes/csv/', views.exportar_clientes_csv, name='exportar_clientes_csv'),
    
    # Exportar a PDF
    path('exportar/productos/pdf/', views.exportar_productos_pdf, name='exportar_productos_pdf'),
    path('exportar/clientes/pdf/', views.exportar_clientes_pdf, name='exportar_clientes_pdf'),
]
