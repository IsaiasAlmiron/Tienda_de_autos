from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Producto, Cliente,CustomUser,Venta, DetalleVenta,Marca
from django.contrib.auth.decorators import login_required, user_passes_test
import csv
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO
from .forms import CustomUserCreationForm,CustomUserEditForm,DetalleVentaForm,VentaForm  # ← AGREGAR
from .models import Marca
from .models import Venta
from django.utils import timezone
from django.forms import modelformset_factory

class MarcaListView(LoginRequiredMixin, ListView):
    model = Marca
    template_name = 'marcas/marca_list.html'
    context_object_name = 'marcas'

class MarcaCreateView(LoginRequiredMixin, CreateView):
    model = Marca
    fields = ['nombre']
    template_name = 'marcas/marca_form.html'
    success_url = reverse_lazy('marca_list')

class MarcaUpdateView(LoginRequiredMixin, UpdateView):
    model = Marca
    fields = ['nombre']
    template_name = 'marcas/marca_form.html'
    success_url = reverse_lazy('marca_list')

class MarcaDeleteView(LoginRequiredMixin, DeleteView):
    model = Marca
    template_name = 'marcas/marca_confirm_delete.html'
    success_url = reverse_lazy('marca_list')

# === PRODUCTOS ===
class ProductoListView(LoginRequiredMixin, ListView):
    model = Producto
    template_name = 'productos/producto_list.html'
    context_object_name = 'productos'

class ProductoCreateView(LoginRequiredMixin, CreateView):
    model = Producto
    fields = ['marca','nombre',  'modelo', 'precio', 'stock']
    template_name = 'productos/producto_form.html'
    success_url = reverse_lazy('producto_list')

class ProductoUpdateView(LoginRequiredMixin, UpdateView):
    model = Producto
    fields = [ 'marca','nombre', 'modelo', 'precio', 'stock']
    template_name = 'productos/producto_form.html'
    success_url = reverse_lazy('producto_list')

class ProductoDeleteView(LoginRequiredMixin, DeleteView):
    model = Producto
    template_name = 'productos/producto_confirm_delete.html'
    success_url = reverse_lazy('producto_list')


# === CLIENTES ===
class ClienteListView(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = 'clientes/cliente_list.html'
    context_object_name = 'clientes'

class ClienteCreateView(LoginRequiredMixin, CreateView):
    model = Cliente
    fields = ['ruc', 'nombre', 'apellido', 'telefono', 'email', 'direccion']
    template_name = 'clientes/cliente_form.html'
    success_url = reverse_lazy('cliente_list')

class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Cliente
    fields = ['nombre', 'apellido', 'telefono', 'email', 'direccion']
    template_name = 'clientes/cliente_form.html'
    success_url = reverse_lazy('cliente_list')

class ClienteDeleteView(LoginRequiredMixin, DeleteView):
    model = Cliente
    template_name = 'clientes/cliente_confirm_delete.html'
    success_url = reverse_lazy('cliente_list')
# ========== Ventas==========
class VentaListView(LoginRequiredMixin, ListView):
    model = Venta
    template_name = 'ventas/venta_list.html'
    context_object_name = 'ventas'
class VentaCreateView(LoginRequiredMixin, CreateView):
    model = Venta
    fields = ['cliente']  # Quitar 'vendedor' del formulario, se asigna automáticamente
    template_name = 'ventas/venta_form.html'
    success_url = reverse_lazy('venta_list')

    def form_valid(self, form):
        form.instance.vendedor = self.request.user
        return super().form_valid(form)

class VentaDetailView(LoginRequiredMixin, DetailView):
    model = Venta
    template_name = 'ventas/venta_detail.html'
# ========== VERIFICACIÓN DE PERMISOS ==========

def es_administrador(user):
    """Verifica si el usuario es superuser o tiene rol admin"""
    return user.is_superuser or (user.is_authenticated and user.role == 'admin')


# ========== VISTAS DE USUARIO ==========

@login_required(login_url='login')
def index(request):
    """Página de inicio"""
    productos_count = Producto.objects.count()
    clientes_count = Cliente.objects.count()
    usuarios_count = CustomUser.objects.count()
    
    context = {
        'productos_count': productos_count,
        'clientes_count': clientes_count,
        'usuarios_count': usuarios_count,
    }
    return render(request, 'index.html', context)


@login_required(login_url='login')
@user_passes_test(es_administrador, login_url='index')
def crear_usuario(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)  # ← CAMBIAR AQUÍ
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario creado exitosamente.')
            return redirect('listar_usuarios')
    else:
        form = CustomUserCreationForm()  # ← CAMBIAR AQUÍ
    
    return render(request, 'usuarios/crear_usuario.html', {'form': form})

@login_required(login_url='login')
@user_passes_test(es_administrador, login_url='index')
def listar_usuarios(request):
    """Listar todos los usuarios (SOLO ADMIN)"""
    usuarios = CustomUser.objects.all().order_by('-date_joined')
    return render(request, 'usuarios/listar_usuarios.html', {'usuarios': usuarios})


# ========== VISTAS DE EXPORTACIÓN (CSV) ==========

@login_required(login_url='login')
def exportar_productos_csv(request):
    """Exportar productos a CSV"""
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="productos.csv"'
    response.write('\ufeff')  # BOM para UTF-8 en Excel
    
    writer = csv.writer(response)
    writer.writerow(['ID', 'Nombre', 'Modelo', 'Precio', 'Stock'])
    
    for producto in Producto.objects.all():
        writer.writerow([
            producto.id,
            producto.nombre,
            producto.modelo if producto.modelo else 'N/A',  # 👈 acá el cambio
            f"${producto.precio}",
            producto.stock,
        ])
    
    return response



@login_required(login_url='login')
def exportar_clientes_csv(request):
    """Exportar clientes a CSV"""
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="clientes.csv"'
    response.write('\ufeff')
    
    writer = csv.writer(response)
    writer.writerow(['RUC', 'Nombre', 'Apellido', 'Teléfono', 'Email', 'Dirección'])
    
    for cliente in Cliente.objects.all():
        writer.writerow([
            cliente.ruc,
            cliente.nombre,
            cliente.apellido,
            cliente.telefono,
            cliente.email,
            cliente.direccion
        ])
    
    return response


# ========== VISTAS DE EXPORTACIÓN (PDF) ==========

@login_required(login_url='login')
def exportar_productos_pdf(request):
    """Exportar productos a PDF"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=20,
        alignment=1
    )
    
    title = Paragraph("Reporte de Productos", title_style)
    elements.append(title)
    elements.append(Spacer(1, 12))
    
    # Datos
    data = [['ID', 'Nombre', 'Modelo', 'Precio', 'Stock']]

    for producto in Producto.objects.all():
        data.append([
        str(producto.id),
        producto.nombre,
        producto.modelo if producto.modelo else 'N/A',
        f"${producto.precio}",
        str(producto.stock),
    ])
    
    # Tabla
    table = Table(data, colWidths=[0.8*inch, 2.5*inch, 1.5*inch, 1*inch, 1*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(table)
    doc.build(elements)
    
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="productos.pdf"'
    return response

@login_required(login_url='login')
def exportar_ventas_pdf(request):
    """Exportar listado de ventas a PDF (resumen por venta)"""
    # Respuesta HTTP como PDF descargable
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_ventas.pdf"'

    # Documento base
    doc = SimpleDocTemplate(
        response,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    elements = []
    styles = getSampleStyleSheet()

    # Título
    titulo = Paragraph("Reporte de Ventas", styles['Heading1'])
    fecha_gen = Paragraph(
        f"Generado el {timezone.localtime(timezone.now()).strftime('%d/%m/%Y %H:%M')}",
        styles['Normal']
    )

    elements.append(titulo)
    elements.append(fecha_gen)
    elements.append(Spacer(1, 12))

    # Encabezados de tabla
    data = [['ID', 'Fecha', 'Cliente', 'Vendedor', 'Total (Gs)']]

    # Consultar ventas (con cliente y vendedor)
    ventas = (
        Venta.objects
        .select_related('cliente', 'vendedor')
        .order_by('-fecha')
    )

    for venta in ventas:
        data.append([
            str(venta.id),
            venta.fecha.strftime('%d/%m/%Y %H:%M'),
            str(venta.cliente),
            str(venta.vendedor),
            f"{venta.total:,.2f}",
        ])

    # Si no hay ventas, agregar una fila indicando eso
    if len(data) == 1:
        data.append(['-', '-', 'Sin ventas registradas', '-', '-'])

    # Crear tabla
    table = Table(
        data,
        colWidths=[40, 90, 140, 120, 80],
        hAlign='LEFT',
    )

    # Estilos de la tabla
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f2937')),  # header
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),

        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (-1, 1), (-1, -1), 'RIGHT'),

        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),

        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 9),

        ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1),
            [colors.whitesmoke, colors.HexColor('#e5e7eb')]),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('TOPPADDING', (0, 0), (-1, 0), 6),
    ])

    table.setStyle(style)
    elements.append(table)

    # Construir el PDF
    doc.build(elements)
    return response


@login_required(login_url='login')
def exportar_clientes_pdf(request):
    """Exportar clientes a PDF"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=20,
        alignment=1
    )
    
    title = Paragraph("Reporte de Clientes", title_style)
    elements.append(title)
    elements.append(Spacer(1, 12))
    
    # Datos
    data = [['RUC', 'Nombre', 'Apellido', 'Teléfono', 'Email']]
    
    for cliente in Cliente.objects.all():
        data.append([
            cliente.ruc,
            cliente.nombre,
            cliente.apellido,
            cliente.telefono,
            cliente.email
        ])
    
    # Tabla
    table = Table(data, colWidths=[1.2*inch, 1.8*inch, 1.8*inch, 1.5*inch, 2*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(table)
    doc.build(elements)
    
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="clientes.pdf"'
    return response 


@login_required(login_url='login')
@user_passes_test(es_administrador, login_url='index')
def editar_usuario(request, pk):
    """Editar usuario (SOLO ADMIN)"""
    usuario = get_object_or_404(CustomUser, pk=pk)
    
    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, f'Usuario {usuario.username} actualizado exitosamente.')
            return redirect('listar_usuarios')
    else:
        form = CustomUserEditForm(instance=usuario)
    
    return render(request, 'usuarios/editar_usuario.html', {'form': form, 'usuario': usuario})


@login_required(login_url='login')
@user_passes_test(es_administrador, login_url='index')
def eliminar_usuario(request, pk):
    """Eliminar usuario (SOLO ADMIN)"""
    usuario = get_object_or_404(CustomUser, pk=pk)
    
    # No permitir eliminarse a sí mismo
    if usuario.id == request.user.id:
        messages.error(request, 'No puedes eliminar tu propia cuenta.')
        return redirect('listar_usuarios')
    
    if request.method == 'POST':
        username = usuario.username
        usuario.delete()
        messages.success(request, f'Usuario {username} eliminado correctamente.')
        return redirect('listar_usuarios')
    
    return render(request, 'usuarios/confirmar_eliminar.html', {'usuario': usuario})


@login_required
def crear_venta(request):
    DetalleFormSet = modelformset_factory(DetalleVenta, form=DetalleVentaForm, extra=1)
    
    if request.method == "POST":
        venta_form = VentaForm(request.POST)
        formset = DetalleFormSet(request.POST, queryset=DetalleVenta.objects.none())
        
        if venta_form.is_valid() and formset.is_valid():
            venta = venta_form.save(commit=False)
            venta.vendedor = request.user
            venta.save()
            total = 0
            for detalle_form in formset:
                if detalle_form.cleaned_data:
                    detalle = detalle_form.save(commit=False)
                    detalle.venta = venta
                    detalle.precio_unitario = detalle.producto.precio
                    detalle.save()
                    total += detalle.cantidad * detalle.precio_unitario
            venta.total = total
            venta.save()
            return redirect('venta_list')
    else:
        venta_form = VentaForm()
        formset = DetalleFormSet(queryset=DetalleVenta.objects.none())

    return render(request, 'ventas/venta_form.html', {
        'venta_form': venta_form,
        'formset': formset,
    })