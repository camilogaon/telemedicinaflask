function mostrarFormulario() {
    // Obtener el elemento del formulario
    var formulario = document.getElementById("formulario");

    // Mostrar el formulario
    formulario.style.display = "block";
}

const medicamentoForm = document.querySelector('#medicamentoForm');

let medicamentos =[];

let editing_medicamento = false;

let medicamentoId = null;

window.addEventListener('DOMContentLoaded', async () => {
    const response = await fetch("/api/medicamentos");
    const data = await response.json();
    medicamentos = data
    renderMedicamento(medicamentos)
    renderMedicamentoCard(medicamentos)
})

medicamentoForm.addEventListener('submit', async e=> {
    e.preventDefault();

    const id_medicamento = medicamentoForm['id_medicamento'].value
    const nombre_medicamento = medicamentoForm['nombre_medicamento'].value
    const descripcion_medicamento = medicamentoForm['descripcion_medicamento'].value
    const precio_medicamento = medicamentoForm['precio_medicamento'].value

    if (!editing_medicamento){
        const response = await fetch('/api/medicamentos', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                id_medicamento,
                nombre_medicamento,
                descripcion_medicamento,
                precio_medicamento
            })
        })

        const data = await response.json()

        medicamentos.push(data)
    }else{
        const response = await fetch(`/api/medicamentos/${medicamentoId}`,{
            method: 'PUT',
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                id_medicamento,
                nombre_medicamento,
                descripcion_medicamento,
                precio_medicamento
            })
        })
        const updateMedicamento = await response.json();
        medicamentos = medicamentos.map(medicamento => medicamento.id_medicamento === updateMedicamento.id_medicamento ? updateMedicamento : medicamento)
        renderMedicamento(medicamentos)
        editing_medicamento = false
        medicamentoId = null
    }

    renderMedicamento(medicamentos) 
    medicamentoForm.reset();
})


function renderMedicamento(medicamentos){
    const medicamentoLista = document.querySelector('#medicamentoLista');

    medicamentos.forEach(medicamento => {
        const medicamentoItem = document.createElement('tr');
        medicamentoItem.innerHTML =`
            <td>${medicamento.id_medicamento}</td>
            <td>${medicamento.nombre_medicamento}</td>
            <td>${medicamento.descripcion_medicamento}</td>
            <td>${medicamento.precio_medicamento}</td>
            <td><button class="btn-edit btn btn-secondary ">Editar</button></td>
            <td><button class="btn-delete btn btn-danger">Eliminar</button></td>
        `;


        const btnDelete = medicamentoItem.querySelector('.btn-delete')

        btnDelete.addEventListener('click', async() =>{
            const response = await fetch(`/api/medicamentos/${medicamento.id_medicamento}`,{
                method: 'DELETE'
            })
            const data = await response.json()

            medicamentos = medicamentos.filter(medicamento => medicamento.id_medicamento !== data.id_medicamento)
            renderMedicamento(medicamentos)

        })

        const btnEdit = medicamentoItem.querySelector('.btn-edit')

        btnEdit.addEventListener('click', async e=>{
            mostrarFormulario();

            const response = await fetch(`/api/medicamentos/${medicamento.id_medicamento}`)
            const data = await response.json()

            medicamentoForm["id_medicamento"].value = data.id_medicamento;
            medicamentoForm["nombre_medicamento"].value = data.nombre_medicamento;
            medicamentoForm["descripcion_medicamento"].value = data.descripcion_medicamento;
            medicamentoForm["precio_medicamento"].value = data.precio_medicamento;

            editing_medicamento = true;
            medicamentoId =data.id_medicamento;
        })

        medicamentoLista.appendChild(medicamentoItem);
    })
}

function renderMedicamentoCard(medicamentos) {
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
            <button class="btn btn-primary" onclick="agregarAlCarrito(${medicamento.id_medicamento})">Agregar al carrito</button>
          </div>
        </div>
      `;

      medicamentoLista.appendChild(medicamentoCard);
    });
  }