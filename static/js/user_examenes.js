

let examenes =[];



window.addEventListener('DOMContentLoaded', async () => {
    const response = await fetch("/api/examenes");
    const data = await response.json();
    examenes = data
    renderExamen(examenes)
})


function agregarAlCarritoExamenes(idExamen) {
  // Realizar una solicitud POST al servidor para agregar al carrito
  fetch('/agregar_al_carrito_examenes', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({ id_examen: idExamen }),
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


function renderExamen(examenes) {
    const examenLista = document.getElementById('examenListaCard');
    examenLista.innerHTML = ''; // Limpiar contenido existente

    const page = parseInt(new URLSearchParams(window.location.search).get('page')) || 1;
    const perPage = 9;
    const start = (page - 1) * perPage;
    const end = start + perPage;

    const examenesPaginados = examenes.slice(start, end);

    examenesPaginados.forEach(examen => {
      const examenCard = document.createElement('div');
      examenCard.className = 'col-md-4 mb-4'; // Clase Bootstrap para el tamaño de la tarjeta
      examenCard.innerHTML = `
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">${examen.name_examen}</h5>
            <p class="card-text">${examen.description_examen}</p>
            <p class="card-text">Precio: ${examen.precio_examen}</p>
            <button class="btn btn-primary" onclick="agregarAlCarritoExamenes(${examen.id_examen})">Agregar al carrito</button>
          </div>
        </div>
      `;

      examenLista.appendChild(examenCard);
    });
  }