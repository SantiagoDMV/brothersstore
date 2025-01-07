from django import forms
from .models import DetalleVenta, Venta, TotalVentas

class crear_venta(forms.ModelForm):
    class Meta:
        model = Venta
        fields= ['cliente', 'estado', 'usuario_vendedor','total', 'metodo_pago','descuento', 'impuesto']
        

class crear_detalle_venta(forms.ModelForm):
    class Meta:
        model= DetalleVenta
        fields= ['producto','cantidad','precio_unitario', 'descuento_producto','subtotal',]
        widgets= {
     'producto': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'descuento_producto': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'subtotal': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
        }
    
class crear_total_ventas(forms.ModelForm):
    class Meta:
        model = TotalVentas
        fields = ['total'] 