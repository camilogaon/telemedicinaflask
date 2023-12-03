

let carrito =[];

window.addEventListener('DOMContentLoaded', async () => {
    const response = await fetch("/api/carrito");
    const data = await response.json();
    carrito = data
    renderCarrito(carrito)
})




  function renderCarrito(carrito){
    const carritoLista = document.getElementById('servicios_carrito');
    carritoLista.innerHTML = '';



    carrito.forEach(carro=> {
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
                        <button class="btn_delete btn btn-danger" >Eliminar</button>
                        <button class="btn_comprar btn btn-success" onclick="comprar(${carro.id_carrito})" >Comprar</button>
                    </div>
                </div>
            </div>
        `;

        const btn_delete = carritoCard.querySelector('.btn_delete');

        btn_delete.addEventListener('click', async() =>{
          const response = await fetch(`/api/carrito/${carro.id_carrito}`, {
            method: 'DELETE',
          })

          const data = await response.json()

          carrito = carrito.filter(carro => carro.id_carrito !==data.id_carrito)
          renderCarrito(carrito)
        })


        carritoLista.appendChild(carritoCard);
    })
  }


  function comprar(idCarrito, carrito) {
    fetch('/comprar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ id_carrito: idCarrito })
    })

    .then(response => response.json())
    .then(data => {
        carrito = carrito.filter(carro => carro.id_carrito !==data.id_carrito)
        renderCarrito()
        alert(data.message);
        
        
    })
    .catch(error => {
        console.error('Error:', error);
    });
}


