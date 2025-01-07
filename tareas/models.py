from django.db import models
from ventas.models import MetodoPago
from django.contrib.auth.models import User
from ventas.models import EstadoVenta

# Create your models here.
class CategoriaGasto(models.Model):
    nombre = models.CharField(max_length=100,null=False)
    descripcion = models.TextField(blank=True, null=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    eliminado_en = models.DateTimeField(blank=True,null=True)
    actualizado_en = models.DateTimeField(blank=True,null=True)
    
    def __str__(self):
        return self.nombre + ' - ' + self.descripcion

class Finanzas(models.Model):
    usuario = models.ForeignKey(User,on_delete=models.CASCADE, blank=True,null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    categoria_gasto = models.ForeignKey(CategoriaGasto, on_delete=models.CASCADE)
    descripcion = models.TextField(blank=True, null=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.ForeignKey(MetodoPago, on_delete=models.CASCADE)
    comprobante_url = models.TextField(blank=True, null=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    eliminado_en = models.DateTimeField(blank=True,null=True)
    actualizado_en = models.DateTimeField(blank=True,null=True)
        
    def __str__(self):
        return self.descripcion + ' - ' + str(self.monto)
    
#class Ingresos(models.Model):
    
class Salarios(models.Model):
    usuario = models.ForeignKey(User,on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.ForeignKey(EstadoVenta, on_delete=models.CASCADE, null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(blank=True, null=True)
    eliminado_en = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return self.usuario.username + ' - ' + str(self.monto)