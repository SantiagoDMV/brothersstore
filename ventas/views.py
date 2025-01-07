from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import crear_detalle_venta,crear_venta
from .models import Venta, DetalleVenta,EstadoVenta, MetodoPago
from inventario.models import Producto

# Create your views here.
def ventas(request):
    try:
        ventas = Venta.objects.all()
        return render(request, 'ventas.html',{        
        'ventas' : ventas
        })
    except:
        return render(request, 'ventas.html',{        
        'ventas' : []
        })

def funcion_crear_venta(request):
    if request.method == 'POST':
        data =request.POST
        estado_obtenido = get_object_or_404(EstadoVenta, pk = data.get('estado'))
        metodo_obtenido =get_object_or_404(MetodoPago, pk = int(data.get('metodo_pago'))) 
        
        crear_nueva_venta = Venta.objects.create(
            estado = estado_obtenido,
            usuario_vendedor = request.user,
            metodo_pago = metodo_obtenido,
            descuento = float(data.get('descuento',0)),
            impuesto = float(data.get('impuesto',0)),
            total = float(data.get('total',0))
        )
        
        productos = data.getlist('producto')
        cantidades = data.getlist('cantidad')
        precios_unitarios = data.getlist('precio_unitario')
        subtotales = data.getlist('subtotal')
        detalles_venta = []
        
        for i in range(len(productos)):
            detalle = DetalleVenta(
                venta_id = crear_nueva_venta,
                producto = get_object_or_404(Producto,pk = productos[i]),
                cantidad = cantidades[i],
                precio_unitario = float(precios_unitarios[i]),
                descuento_producto = 0,
                subtotal = float(subtotales[i]),
            )
            
            detalles_venta.append(detalle)
        
        DetalleVenta.objects.bulk_create(detalles_venta)
        
        return redirect('ventas')
    else:
        if request.method == 'GET':
            return render(request, 'crear_venta.html',{        
                'form_venta' : crear_venta,
                'form_detalle_venta': crear_detalle_venta
            })
    
def mostrar_detalle_venta(request, venta_id):
    if(request.method == 'GET'):
        detalle_obtenido = DetalleVenta.objects.filter(venta_id = venta_id)
        venta_obtenida = get_object_or_404(Venta, pk = venta_id)
        form_venta_obtenida = crear_venta(instance=venta_obtenida)
        return render(request, 'detalle_venta.html',{
        'form_detalle_ventas': detalle_obtenido,
        'form_venta' : form_venta_obtenida,
        'form_detalle_venta' : crear_detalle_venta,
        'venta_id': venta_id
        })
    else:
        if(request.method == 'POST'):
            
            instancia_venta = get_object_or_404(Venta, pk=venta_id)
            #eliminar_detalles_ids = request.POST.getlist('eliminar_detalle_ids')
            #print(eliminar_detalles_ids)
        
        # Eliminar los detalles seleccionados
            #if eliminar_detalles_ids:
             #   DetalleVenta.objects.filter(id__in=eliminar_detalles_ids).delete()
            
            #instancia_venta = get_object_or_404(Venta, pk=venta_id)
            #print('ssss')
            #print(request.POST)
            instancia_estado = get_object_or_404(EstadoVenta,pk = request.POST['estado'])
            instancias_detalles_venta = DetalleVenta.objects.filter(venta_id = venta_id)
            data= request.POST
            #print(data)
            
            actualizar_instancia_venta = crear_venta({
                'metodo_pago' : data.get('metodo_pago'),
                'descuento': float(data.get('descuento',0)),
                'impuesto': float(data.get('impuesto',0)),
                'estado' : instancia_estado,
                'total': float(data.get('total',0)),
                'usuario_vendedor' : request.user
            }, instance=instancia_venta)
            
            if actualizar_instancia_venta.is_valid():
                actualizar_instancia_venta.save()
            else:
                print(actualizar_instancia_venta.errors) 
            
            nuevo_detalle_ventas = []
            nuevos_productos = data.getlist('producto')
            nuevas_cantidades = data.getlist('cantidad')
            nuevos_precios_unitarios = data.getlist('precio_unitario')
            nuevos_subtotal = data.getlist('subtotal')
            productos_mostrados = data.getlist('mostrados')
            

            len_instancias_detalles_venta = len(instancias_detalles_venta)
            #print(len(instancias_detalles_venta))
            #print(instancias_detalles_venta)
            for i in range(len(productos_mostrados)):
                #print('instancias_detalles_venta[i]')
                #print(instancias_detalles_venta[i])
                #print(instancias_detalles_venta[i].id)
                #print(f'cantidad, {nuevas_cantidades[i]}')
                #print(f'precio_unitario, {float(nuevos_precios_unitarios[i])}')
                #print(f'subtotal, {nuevos_subtotal[i]}')
                registro_existente_actualizar = crear_detalle_venta(
                    {
                        'producto': get_object_or_404(Producto, pk = instancias_detalles_venta[i].producto.id),
                        'descuento_producto': 0,
                        #'venta_id' : get_object_or_404(Venta, pk = venta_id),
                        'cantidad': nuevas_cantidades[i],
                        'precio_unitario': float(nuevos_precios_unitarios[i]),
                        'subtotal' : float(nuevos_subtotal[i]),
                    }, 
                    instance= instancias_detalles_venta[i]
                )
                if registro_existente_actualizar.is_valid():
                    registro_existente_actualizar.save()
                else:
                    print(registro_existente_actualizar.errors)
                    
            
            #print(productos_mostrados)
            #print(instancias_detalles_venta[0].id)
            #print(len_instancias_detalles_venta)
            for i in range (len_instancias_detalles_venta):
                if str(instancias_detalles_venta[i].id) not in productos_mostrados:
                    #print('eliminado')
                    #print(instancias_detalles_venta[i].id in productos_mostrados)
                    eliminar_registro = get_object_or_404(DetalleVenta, pk = instancias_detalles_venta[i].id)    
                    eliminar_registro.delete()
            
            #print(len(nuevos_productos))
            
            if len(nuevos_productos) > 0:
                for i in range(len(nuevos_productos)):
                    detalle_venta = DetalleVenta(
                        venta_id = get_object_or_404(Venta, pk = venta_id),
                        producto = get_object_or_404(Producto, pk = nuevos_productos[i]),
                        cantidad = int(nuevas_cantidades[len(productos_mostrados) + i]),
                        precio_unitario = float(nuevos_precios_unitarios[len(productos_mostrados) + i]),
                        descuento_producto = 0,
                        subtotal = float(nuevos_subtotal[len(productos_mostrados) + i]),
                    )
                
                    nuevo_detalle_ventas.append(detalle_venta)
                DetalleVenta.objects.bulk_create(nuevo_detalle_ventas)
            
            return redirect('ventas')
        
def funcion_elimnar_venta(request, venta_id):
    instancia_venta = get_object_or_404(Venta,pk = venta_id)
    instancia_venta.delete()
    
    return redirect('ventas')