from django.contrib import admin
from .models import DetalleVenta,Venta,EstadoVenta, MetodoPago

# Register your models here.

admin.site.register(EstadoVenta)
admin.site.register(Venta)
admin.site.register(DetalleVenta)
admin.site.register(MetodoPago)