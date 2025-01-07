from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Producto, Categoria
from .forms import crear_producto, crear_categoria
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.

@login_required
def inventario(request):
    try:
        todos_los_productos = Producto.objects.all()
        return render(request, 'inventario.html', {  
            "productos" : todos_los_productos
        })
    except:
        return render(request, 'inventario.html', {  
            "productos" : []
        })
        
@login_required
@permission_required('inventario.add_producto',raise_exception=True)
def funcion_crear_producto(request):
    if(request.method == "GET"):
        return render(request, 'crear_producto.html' ,{
            "form": crear_producto,
        }) 
    else:
        try:
            form = crear_producto(request.POST)
            nuevo_producto = form.save(commit=False)
            nuevo_producto.usuario = request.user
            nuevo_producto.save()
            return redirect('inventario')
        except ValueError: 
            if(request.method == "POST"):
                return render(request, 'crear_producto.html' ,{
                "form": crear_producto,
                "error": 'Ingrese datos válidos'
            }) 

@login_required
def mostrar_producto(request, producto_id):
    if request.method == 'GET':
        
        producto = get_object_or_404(Producto, pk = producto_id)
        producto_form = crear_producto(instance=producto)
        return render(request, 'detalle_producto.html', {
            "producto": producto,
            "form" : producto_form
        })
    else:
        if not request.user.has_perm('inventario.update_producto'):
            return render(request, '403.html', status=403)
        if(request.method == 'POST'):
            try:
                producto= get_object_or_404(Producto, pk=producto_id)
                producto_actualizado = crear_producto(request.POST, instance=producto)
                producto_actualizado.save()
                return redirect('inventario')
            except ValueError:
                return render(request, 'detalle_producto.html',{
                    "producto": producto,
                    "form": producto_actualizado,
                    "error": 'Ingrese datos válidos'
                })
@login_required
@permission_required('inventario.delete_producto',raise_exception=True)
def funcion_eliminar_producto(request,producto_id):
    if(request.method == 'POST'):
        producto = get_object_or_404(Producto, pk = producto_id)
        producto.delete()
        return redirect('inventario')
            
            
#################################################################################################
##CATEGORIAS##
@login_required
def mostrar_categorias(request):
    try:
        categorias = Categoria.objects.all()
        return render(request, 'categorias.html',{
            'categorias': categorias
        })
    except:
        return render(request, 'categorias.html',{
            'categorias': []
        })
@login_required
@permission_required('inventario.add_categoria',raise_exception=True)
def funcion_crear_categoria(request):
    if request.method == "POST":
        try:
            categoria = crear_categoria(request.POST)
            nueva_categoria = categoria.save(commit=False)
            nueva_categoria.usuario = request.user
            nueva_categoria.save()
            return redirect('categorias')
        except:
            return render(request, 'crear_categoria.html', {
                "form": crear_categoria,
                "error": 'Error al intentar crear la categoria'
            })
    else:
        return render(request, 'crear_categoria.html', {
            "form": crear_categoria
        })

@login_required
#@permission_required('inventario.view_categoria',raise_exception=True)
def obtener_categoria(request, categoria_id):
    if(request.method  == 'GET'):
        categoria = get_object_or_404(Categoria,pk = categoria_id)
        categoria_form = crear_categoria(instance=categoria)
        return render(request, 'detalle_categoria.html', {
            'categoria': categoria,
            'form' : categoria_form
        })
    else:
        if not request.user.has_perm('categoria.update_categoria'):
            return render(request, '403.html', status=403)
        
        if(request.method == 'POST'):
            categoria = get_object_or_404(Categoria, pk = categoria_id)
            categoria_actualizada = crear_categoria(request.POST , instance=categoria) 
            categoria_actualizada.save()
            return redirect('categorias')
            
@login_required
@permission_required('inventario.delete_categoria',raise_exception=True)
def funcion_eliminar_categoria(request, categoria_id):
    if(request.method == 'POST'):
        categoria = get_object_or_404(Categoria, pk = categoria_id)
        categoria.delete()
        return redirect('categorias')
