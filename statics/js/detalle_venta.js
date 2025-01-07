let btn_agregar = document.getElementById('btn-agregar');
let div = document.getElementById('div_productos');
let div_producto = document.getElementById('div1');

// Función para agregar un producto (con valores vacíos)
btn_agregar.addEventListener('click', (e) => {
    e.preventDefault();

    // Clonar la primera fila, pero con valores vacíos
    let nuevoProducto = div_producto.cloneNode(true);

    // Obtener el último número de ID y agregar 1 para el nuevo ID
    let elemento = div.lastElementChild.id;
    let numeros = elemento.match(/\d+/g);
    nuevoProducto.id = `div${parseInt(numeros) + 1}`;

    // Limpiar los campos
    let productoSelect = nuevoProducto.querySelector('.producto');
    productoSelect.value = ""; // Vaciar selección de producto

    let cantidadInput = nuevoProducto.querySelector('.cantidad');
    cantidadInput.value = "1"; // Poner valor por defecto

    let precioInput = nuevoProducto.querySelector('.precio_unitario');
    precioInput.value = "0"; // Poner valor por defecto

    let subtotalInput = nuevoProducto.querySelector('.subtotal');
    subtotalInput.value = "0"; // Poner valor por defecto


    // Agregar el nuevo producto a la lista
    div.appendChild(nuevoProducto);

    // Recalcular total
    calcularTotal();
});

// Event listener para eliminar productos
div.addEventListener('click', (e) => {
    if (e.target.classList.contains('btn-eliminar')) {
        let divProducto = e.target.closest('tr');
        divProducto.remove(); // Eliminar el tr
        calcularTotal(); // Recalcular total después de eliminar
    }
});

// Función para habilitar los campos de cantidad y precio solo cuando se seleccione un producto
function habilitarCampos(select) {
    let fila = select.closest('tr');

    // Recalcular subtotal al cambiar el producto
    calcularSubtotal(fila.querySelector('.cantidad'));
}

// Aplicar la habilitación de los campos cuando se selecciona un producto
document.querySelectorAll('.producto').forEach(productoSelect => {
    productoSelect.addEventListener('change', (e) => {
        habilitarCampos(e.target); // Llamar a la función cuando cambia el producto
    });
});

// Función para calcular el subtotal de cada producto
function calcularSubtotal(elemento) {
    let fila = elemento.closest('tr');
    let cantidad = parseFloat(fila.querySelector('.cantidad').value) || 0;
    let precio = parseFloat(fila.querySelector('.precio_unitario').value) || 0;
    let subtotal = cantidad * precio;

    fila.querySelector('.subtotal').value = subtotal.toFixed(2);

    // Recalcular total global
    calcularTotal();
}

// Función para calcular el total de la venta
function calcularTotal() {
    let total = 0;

    // Sumar subtotales de todos los productos
    document.querySelectorAll('.subtotal').forEach(subtotal => {
        total += parseFloat(subtotal.value) || 0;
    });

    // Obtener descuento e impuesto
    let descuento = parseFloat(document.getElementById('descuento').value) || 0;
    let impuesto = parseFloat(document.getElementById('impuesto').value) || 0;

    // Aplicar descuento
    total -= descuento;

    // Aplicar impuesto
    total += total * (impuesto / 100);

    // Mostrar total
    document.getElementById('total').value = total.toFixed(2);
    document.getElementById('total-cálculo').textContent = total.toFixed(2);
}

// Cambiar impuesto si el método de pago es tarjeta
function cambiarImpuesto() {
    let metodoPago = document.getElementById('metodo_pago').value;
    if (metodoPago === "Tarjeta de Crédito/Débito") {
        document.getElementById('impuesto').value = 15;
    } else {
        document.getElementById('impuesto').value = 0;
    }

    // Recalcular total después de cambiar el impuesto
    calcularTotal();
}
