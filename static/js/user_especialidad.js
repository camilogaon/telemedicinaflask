

let especialidades =[];

var miVariableEnJavaScript = document.getElementById('contenedor').getAttribute('data-mi-variable');
    console.log(miVariableEnJavaScript);  

window.addEventListener('DOMContentLoaded', async () => {
    const response = await fetch("/api/especialidades");
    const data = await response.json();
    especialidades = data
    renderEspecialidad(especialidades)
})

// function agregarAlCarritoEspecialidades(idEspecialidad, miVariableEnJavaScript) {
//   console.log(miVariableEnJavaScript);  
//   if (miVariableEnJavaScript == 1) {
//     fetch('/agregar_al_carrito_especialidades', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({ id_especialidad: idEspecialidad }),
//     })
//     .then(response => response.json())
//     .then(data => {
//         // Manejar la respuesta del servidor (opcional)
//         console.log(data);
//     })
//     .catch(error => {
//         console.error('Error al agregar al carrito:', error);
//     });

//   } else {
//     window.location.href = "/login";
//   }

  

// }

function agregarAlCarritoEspecialidades(idEspecialidad, miVariableEnJavaScript) {

    fetch('/agregar_al_carrito_especialidades', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ id_especialidad: idEspecialidad }),
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






function renderEspecialidad(especialidades) {
    const especialidadLista = document.getElementById('especialidadListaCard');
    especialidadLista.innerHTML = ''; // Limpiar contenido existente

    const page = parseInt(new URLSearchParams(window.location.search).get('page')) || 1;
    const perPage = 9;
    const start = (page - 1) * perPage;
    const end = start + perPage;

    const especialidadesPaginados = especialidades.slice(start, end);

    especialidadesPaginados.forEach(especialidad => {
      const especialidadCard = document.createElement('div');
      especialidadCard.className = 'col-md-4 mb-4'; // Clase Bootstrap para el tamaño de la tarjeta
      especialidadCard.innerHTML = `
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">${especialidad.nombre_especialidad}</h5>
            <p class="card-text">${especialidad.descripcion_especialidad}</p>
            <p class="card-text">Precio: ${especialidad.precio_especialidad}</p>
            <button class="btn btn-primary" onclick="agregarAlCarritoEspecialidades(${especialidad.id_especialidad}, ${miVariableEnJavaScript})">Agregar al carrito</button>
          </div>
        </div>
      `;

      especialidadLista.appendChild(especialidadCard);
    });
  }