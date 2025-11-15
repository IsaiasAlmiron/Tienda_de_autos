from django.urls import path
from . import views
from .views import MarcaListView, MarcaCreateView, MarcaUpdateView, MarcaDeleteView,VentaListView, VentaCreateView, VentaDetailView, crear_venta
urlpatterns = [
    # Productos
    path('productos/', views.ProductoListView.as_view(), name='producto_list'),
    path('productos/nuevo/', views.ProductoCreateView.as_view(), name='producto_create'),
    path('productos/<int:pk>/editar/', views.ProductoUpdateView.as_view(), name='producto_update'),
    path('productos/<int:pk>/eliminar/', views.ProductoDeleteView.as_view(), name='producto_delete'),

    # Clientes
    path('clientes/', views.ClienteListView.as_view(), name='cliente_list'),
    path('clientes/nuevo/', views.ClienteCreateView.as_view(), name='cliente_create'),
    path('clientes/<str:pk>/editar/', views.ClienteUpdateView.as_view(), name='cliente_update'),
    path('clientes/<str:pk>/eliminar/', views.ClienteDeleteView.as_view(), name='cliente_delete'),

    # Venta
    path('exportar/ventas/pdf/', views.exportar_ventas_pdf, name='exportar_ventas_pdf'),

  path('marcas/', MarcaListView.as_view(), name='marca_list'),
    path('marcas/nuevo/', MarcaCreateView.as_view(), name='marca_create'),
    path('marcas/<int:pk>/editar/', MarcaUpdateView.as_view(), name='marca_update'),
    path('marcas/<int:pk>/eliminar/', MarcaDeleteView.as_view(), name='marca_delete'),

  path('ventas/', VentaListView.as_view(), name='venta_list'),
    path('ventas/nueva/', crear_venta, name='venta_create'),  # ← función personalizada
    path('ventas/<int:pk>/', VentaDetailView.as_view(), name='venta_detail'),


]
