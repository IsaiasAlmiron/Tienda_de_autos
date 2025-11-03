TIENDA DE AUTOS

Versión: 1.0
Compatibilidad: Python 3.12 – Django 5.2.7

Proyecto integrador desarrollado en Django para la gestión de una tienda de autos, cumpliendo con todos los requerimientos funcionales, de autenticación, diseño, documentación y trabajo en equipo establecidos en la rúbrica oficial.

FUNCIONALIDADES

Modelos y Base de Datos

Marca, Modelo, Producto, Cliente y Usuario Personalizado (CustomUser).

Relaciones entre entidades (ForeignKey y OneToMany).

Migraciones automatizadas y uso de ORM de Django.

CRUD Completo

CRUD funcional de Productos, Modelos y Clientes.

Formularios validados con Django Forms y Crispy Forms.

Mensajes de éxito/error tras las operaciones.

Autenticación y Roles

Sistema de login, logout y registro.

Roles definidos: Administrador y Vendedor.

Permisos diferenciados para acceso y edición.

Redirección según rol tras inicio de sesión.

Panel de Administración

Personalización del Django Admin para facilitar la gestión.

Filtros, búsquedas y list displays.

Usuarios administrables desde el panel.

Interfaz Gráfica

Templates con Bootstrap 4 y herencia de plantillas (base.html).

Diseño responsive (móvil y escritorio).

Navegación intuitiva con menús dinámicos según permisos.

Seguridad

Protección CSRF activada.

Validaciones de formulario del lado servidor.

Redirecciones seguras post-login y logout.

Archivos sensibles excluidos del repositorio (.env, venv).

INSTALACIÓN

Clonar el repositorio
git clone -b main https://github.com/IsaiasAlmiron/Tienda_de_autos.git

cd Tienda_de_autos

Crear y activar un entorno virtual
python3 -m venv venv
source venv/bin/activate # En Linux/Mac
venv\Scripts\activate # En Windows

Instalar dependencias
pip install -r requirements.txt

Configurar variables de entorno
Crea un archivo .env basado en .env.example, con los datos necesarios (por ejemplo, credenciales de base de datos o claves secretas).

Aplicar migraciones
python manage.py makemigrations
python manage.py migrate

Crear superusuario
python manage.py createsuperuser

Ejecutar el servidor
python manage.py runserver

Acceder desde el navegador a
http://127.0.0.1:8000/

Panel de administración: /admin/

USUARIOS DE PRUEBA

Usuario: admin
Contraseña: 1234
Rol: Administrador

Usuario: vendedor
Contraseña: 1234
Rol: Vendedor

REQUERIMIENTOS MÍNIMOS CUMPLIDOS

✓ 4+ modelos relacionados
✓ 8+ vistas funcionales
✓ CRUD de 2 entidades mínimo
✓ Login / Registro / Logout
✓ 2 niveles de permisos
✓ Admin personalizado
✓ 8+ templates con herencia
✓ Responsive (Bootstrap 4)
✓ Formularios validados
✓ README con instalación completa
✓ Sistema ejecutable sin errores
✓ Commits de todos los miembros

PUNTOS EXTRA IMPLEMENTADOS

✓ Class-Based Views
✓ Paginación en listado de productos
✓ Búsqueda por nombre y marca
✓ Exportación a CSV y PDF
✓ API REST (Django REST Framework)
✓ Presentación profesional con video demo

ROLES DEL EQUIPO

Backend Lead: [Integrante 1] — Modelos, ORM, migraciones y lógica de negocio
Frontend Lead: [Integrante 2] — Templates, diseño visual, UX y CSS
Auth & Security Lead: [Integrante 3] — Autenticación, permisos, validaciones
Admin & Docs Lead: [Integrante 4] — Panel Admin, documentación, despliegue

EVALUACIÓN Y CALIDAD

Código limpio, modular y comentado.

Queries optimizados con ORM.

Convenciones PEP8 aplicadas.

Uso de .gitignore para excluir venv/ y db.sqlite3.

Sin errores en ejecución ni rutas rotas.

Compatible con Django 5.2.7 y Python 3.12+.

ARCHIVOS DEL PROYECTO

core/ → Configuración principal (settings, urls, wsgi)
autos/ → App principal con modelos, vistas y templates
templates/ → HTML base y vistas extendidas
static/ → CSS, imágenes y JS
requirements.txt → Dependencias del entorno
.env.example → Variables de entorno modelo
.gitignore → Exclusión de archivos sensibles

CHECKLIST PRE-ENTREGA

[x] Repositorio GitHub actualizado
[x] README completo
[x] requirements.txt actualizado
[x] .env.example incluido
[x] Sistema ejecutable sin errores
[x] Usuarios de prueba documentados
[x] Sin carpeta venv/
[x] Funciona en otra PC
[x] Formularios validados
[x] Responsive probado

CONTACTO

Instructor: [Nombre del profesor]
Email: [correo@ejemplo.com
]
Plataforma de comunicación: Discord / Slack
Consultas: [días y horarios]