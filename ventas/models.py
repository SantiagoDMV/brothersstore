from django.db import models
from inventario.models import Producto
from django.contrib.auth.models import User

# Create your models here.

class MetodoPago(models.Model):
    nombre = models.CharField(max_length=100, null=False)
    descripcion = models.TextField(blank=True, null=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    eliminado_en = models.DateTimeField(blank=True,null=True)
    actualizado_en = models.DateTimeField(blank=True,null=True)
    
    def __str__(self):
        return self.nombre

class EstadoVenta(models.Model):
    nombre = models.CharField(max_length=100, null=False)
    descripcion = models.TextField(null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    creado_en = models.DateTimeField(auto_now_add=True)
    eliminado_en = models.DateTimeField(blank=True, null=True)
    actualizado_en = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return self.nombre

class Venta(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='ventas_cliente')
    estado = models.ForeignKey(EstadoVenta, on_delete=models.CASCADE)
    usuario_vendedor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ventas_vendedor')
    total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    metodo_pago = models.ForeignKey(MetodoPago, on_delete=models.CASCADE)
    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Descuento aplicado
    impuesto = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Impuesto sobre el total
    fecha_pago = models.DateTimeField(null=True, blank=True)  # Fecha del pago
    comentarios = models.TextField(null=True, blank=True)  # Notas adicionales sobre la venta
    creado_en = models.DateTimeField(auto_now_add=True)
    eliminado_en = models.DateTimeField(blank=True, null=True)
    actualizado_en = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.usuario_vendedor.username} - {self.estado.nombre} - {self.creado_en}"

class DetalleVenta(models.Model):
    venta_id = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(null=False)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    descuento_producto = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Descuento por producto
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    creado_en = models.DateTimeField(auto_now_add=True, null=True, blank=True) #quitar esto en produccion 
    eliminado_en = models.DateTimeField(blank=True, null=True)
    actualizado_en = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.venta_id.id} - {self.producto.nombre} - {self.cantidad} - {self.subtotal}"


class TotalVentas(models.Model):
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    creado_en = models.DateTimeField(auto_now_add=True)
    eliminado_en = models.DateTimeField(blank=True, null=True)
    actualizado_en = models.DateTimeField(blank=True, null=True)
