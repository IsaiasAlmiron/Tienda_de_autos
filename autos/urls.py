from django.urls import path
from . import views

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

]
