

let medicamentos =[];



window.addEventListener('DOMContentLoaded', async () => {
    const response = await fetch("/api/medicamentos");
    const data = await response.json();
    medicamentos = data
    renderMedicamento(medicamentos)
})


function agregarAlCarritoMedicamentos(idMedicamento) {
  // Realizar una solicitud POST al servidor para agregar al carrito
  fetch('/agregar_al_carrito_medicamentos', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({ id_medicamento: idMedicamento }),
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


function renderMedicamento(medicamentos) {
    const medicamentoLista = document.getElementById('medicamentoListaCard');
    medicamentoLista.innerHTML = ''; // Limpiar contenido existente

    medicamentos.forEach(medicamento => {
      const medicamentoCard = document.createElement('div');
      medicamentoCard.className = 'col-md-4 mb-4'; // Clase Bootstrap para el tamaño de la tarjeta
      medicamentoCard.innerHTML = `
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">${medicamento.nombre_medicamento}</h5>
            <p class="card-text">${medicamento.descripcion_medicamento}</p>
            <p class="card-text">Precio: ${medicamento.precio_medicamento}</p>
            <button class="btn btn-primary" onclick="agregarAlCarritoMedicamentos(${medicamento.id_medicamento})">Agregar al carrito</button>
          </div>
        </div>
      `;

      medicamentoLista.appendChild(medicamentoCard);
    });
  }