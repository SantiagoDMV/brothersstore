from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Categoria(models.Model):
        nombre = models.CharField(max_length=100)
        descripcion = models.TextField(blank=True)
        creado_en = models.DateTimeField(auto_now_add=True)
        actualizado_en = models.DateTimeField(null=True)
        elimnado_en = models.DateTimeField(null=True)
        usuario = models.ForeignKey(User, on_delete=models.CASCADE)
        
        def __str__(self):
            return self.nombre
            
        
class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion= models.TextField(blank=True, null=True)
    cantidad = models.IntegerField(null=False)
    categoria= models.ForeignKey(Categoria, on_delete=models.CASCADE)
    precio = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    imagen_producto = models.ImageField(upload_to='productos', null=True)
    imagen_url = models.TextField(null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(null=True, blank=True)
    elimnado_en = models.DateTimeField(null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre + ' - ' + str(self.cantidad)