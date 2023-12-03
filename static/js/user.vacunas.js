

let vacunas =[];



window.addEventListener('DOMContentLoaded', async () => {
    const response = await fetch("/api/vacunas");
    const data = await response.json();
    vacunas = data
    renderVacuna(vacunas)
})


function agregarAlCarrito(idVacuna) {
  // Realizar una solicitud POST al servidor para agregar al carrito
  fetch('/agregar_al_carrito', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({ id_vacuna: idVacuna }),
  })
  .then(response => response.json())
  .then(data => {
      // Manejar la respuesta del servidor (opcional)
      console.log(data);
  })
  .catch(error => {
      console.error('Error al agregar al carrito:', error);
  });
}



function renderVacuna(vacunas) {
    const vacunaLista = document.getElementById('vacunaListaCard');
    vacunaLista.innerHTML = ''; // Limpiar contenido existente

    vacunas.forEach(vacuna => {
      const vacunaCard = document.createElement('div');
      vacunaCard.className = 'col-md-4 mb-4'; // Clase Bootstrap para el tamaño de la tarjeta
      vacunaCard.innerHTML = `
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">${vacuna.nombre_vacuna}</h5>
            <p class="card-text">${vacuna.descripcion_vacuna}</p>
            <p class="card-text">Precio: ${vacuna.precio_vacuna}</p>
            <button class="btn btn-primary" onclick="agregarAlCarrito(${vacuna.id_vacuna})">Agregar al carrito</button>
          </div>
        </div>
      `;

      vacunaLista.appendChild(vacunaCard);
    });
  }