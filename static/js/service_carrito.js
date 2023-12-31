let carrito = [];
let total = 0;  // Variable para almacenar el total

window.addEventListener('DOMContentLoaded', async () => {
    const response = await fetch("/api/carrito");
    const data = await response.json();
    carrito = data;
    calcularTotal();  // Calcula el total al cargar la página
    renderCarrito(carrito);
});

function renderCarrito(carrito) {
    const carritoLista = document.getElementById('servicios_carrito');
    carritoLista.innerHTML = '';

    carrito.forEach(carro => {
        const carritoCard = document.createElement('div');
        carritoCard.className = 'card mb-3';
        carritoCard.innerHTML = `
            <div class="card-body">
                <div class="row">
                    <div class="col-8">
                        <h5 class="card-title"><strong>${carro.name_servicio}</strong></h5>
                        <p class="card-text">${carro.descripcion_servicio}</p>
                        <p class="card-text"><strong>Precio:</strong>${carro.precio_servicio}</p>
                    </div>
                    <div class="col-4 text-center mt-4">
                        <button class="btn_delete btn btn-danger" data-id="${carro.id_carrito}">
                            <span class="material-icons">delete</span>
                        </button>
                    </div>
                </div>
            </div>
        `;

        carritoLista.appendChild(carritoCard);
    });

    // Añade el elemento para mostrar el total
    

    // Añade el botón "Comprar" si hay elementos en el carrito
    if (carrito.length > 0) {
        const totalElement = document.createElement('div');
        totalElement.innerHTML = `<p class="card-text mb-3"><strong>Total: </strong>${total}</p>`;
        carritoLista.appendChild(totalElement);
        const comprarButton = document.createElement('button');
        comprarButton.className = 'btn_comprar btn btn-success';
        comprarButton.textContent = 'Comprar';
        comprarButton.addEventListener('click', comprar);
        carritoLista.appendChild(comprarButton);
    }
    


    // Agrega eventos de clic a los botones de eliminación
    const btnDeleteList = document.querySelectorAll('.btn_delete');
    btnDeleteList.forEach(btn => {
        btn.addEventListener('click', async () => {
            const idCarrito = btn.getAttribute('data-id');
            await eliminarDelCarrito(idCarrito);
        });
    });
}

async function eliminarDelCarrito(idCarrito) {
    const response = await fetch(`/api/carrito/${idCarrito}`, {
        method: 'DELETE',
    });

    const data = await response.json();

    carrito = carrito.filter(carro => carro.id_carrito !== data.id_carrito);
    calcularTotal();  // Recalcula el total después de eliminar un producto
    renderCarrito(carrito);
}

async function comprar() {
    if (carrito.length === 0) {
        alert('El carrito está vacío. Agregue servicios antes de comprar.');
        return;
    }

    // Obtiene los IDs de los artículos en el carrito
    const idsCarrito = carrito.map(carro => carro.id_carrito);

    // Realiza la compra de todos los artículos a la vez
    const response = await fetch('/comprar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ ids_carrito: idsCarrito }),
    });

    const data = await response.json();

    // Limpia el carrito después de la compra
    carrito = [];
    calcularTotal();  // Recalcula el total después de realizar la compra
    renderCarrito(carrito);

    alert(data.message);
}

// Función para calcular el total
function calcularTotal() {
    total = carrito.reduce((acc, carro) => acc + carro.precio_servicio, 0);
}
