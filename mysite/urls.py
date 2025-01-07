"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from inventario import views as views_inventario 
from tareas import views as views_tareas
from ventas import views as views_ventas


urlpatterns = [
    path('admin/', admin.site.urls),
    path('registro/', views_tareas.registro, name = 'registro'),
    path('login/', views_tareas.login_usuario, name= 'login'),
    path('salir/', views_tareas.logout_usuario, name= 'salir'),
    path('total-salarios/', views_tareas.calcular_salarios, name= 'total-salarios'),
    path('', views_tareas.home, name= 'home'),
    path('inventario/', views_inventario.inventario, name='inventario'),
    path('inventario/crear_producto/', views_inventario.funcion_crear_producto, name = 'crear_producto'),
    path('inventario/<int:producto_id>/eliminar_producto/', views_inventario.funcion_eliminar_producto, name = 'eliminar_producto'),
    path('inventario/crear_categoria', views_inventario.funcion_crear_categoria, name='crear_categoria'),
    path('inventario/<int:producto_id>', views_inventario.mostrar_producto, name= 'mostrar_producto'),
    path('categorias/', views_inventario.mostrar_categorias, name = 'categorias'),
    path('categorias/<int:categoria_id>', views_inventario.obtener_categoria, name = 'mostrar_categoria'),
    path('categorias/<int:categoria_id>/eliminado', views_inventario.funcion_eliminar_categoria, name='eliminar_categoria'),
    ##VENTAS############################
    path('ventas/', views_ventas.ventas, name= 'ventas'),
    path('ventas/crear_venta/', views_ventas.funcion_crear_venta, name= 'crear_venta'),
    path('ventas/<int:venta_id>/', views_ventas.mostrar_detalle_venta, name= 'detalle_venta'),
    path('ventas/<int:venta_id>/eliminar_venta', views_ventas.funcion_elimnar_venta, name= 'eliminar_venta'),
    ##I/G#################################
    path('gastos/', views_tareas.page_gastos, name = 'gastos'),
    path('mercaderia/', views_tareas.page_mercaderia, name='mercaderia'),
    path('gastos/vista-salarios/', views_tareas.vista_salarios, name = 'vista-salarios'),
    path('gastos/pago-salario/<int:salario_id>', views_tareas.crear_pago_salario, name = 'pago-salario'),
    path('gastos/actualizar-pago-salario/<int:pago_salario_id>', views_tareas.actualizar_pago_salario, name = 'actualizar-pago-salario'),
    path('gastos/actualizar-pago-salario/<int:pago_salario_id>/eliminar', views_tareas.eliminar_pago_salario, name = 'eliminar-pago-salario'),
]
