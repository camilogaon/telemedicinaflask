function mostrarFormulario() {
    // Obtener el elemento del formulario
    var formulario = document.getElementById("formulario");

    // Mostrar el formulario
    formulario.style.display = "block";
}


// **********VACUNAS***********

const vacunaForm = document.querySelector('#vacunaForm');

let vacunas = [];

let editing_vacuna = false;

let vacunaId = null;

window.addEventListener('DOMContentLoaded',async() => {
    const response = await fetch("/api/vacunas");
    const data = await response.json();
    vacunas = data
    renderVacuna(vacunas)
})

vacunaForm.addEventListener('submit', async e=>{
    e.preventDefault();

    const id_vacuna = vacunaForm['id_vacuna'].value
    const nombre_vacuna = vacunaForm['nombre_vacuna'].value
    const descripcion_vacuna = vacunaForm['descripcion_vacuna'].value
    const precio_vacuna = vacunaForm['precio_vacuna'].value

    if (!editing_vacuna){
        const response = await fetch('/api/vacunas',{
            method: 'POST',
            headers:{
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                id_vacuna,
                nombre_vacuna,
                descripcion_vacuna,
                precio_vacuna
            })
        })

        const data = await response.json()

        vacunas.push(data)
    }else{
        const response = await fetch(`/api/vacunas/${vacunaId}`,{
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                id_vacuna,
                nombre_vacuna,
                descripcion_vacuna,
                precio_vacuna
            })
        })
        const updateVacuna = await response.json();
        vacunas = vacunas.map(vacuna => vacuna.id_vacuna === updateVacuna.id_examen ? updateVacuna : vacuna)
        renderVacuna(vacunas)
        editing_vacuna=false
        vacunaId = null
    }

    renderVacuna(vacunas)
    vacunaForm.reset();
})


function renderVacuna (vacunas) {
    const vacunaLista = document.querySelector('#vacunaLista');

    vacunas.forEach(vacuna =>{
        const vacunaItem = document.createElement('tr');
        vacunaItem.innerHTML= `
            <td>${vacuna.id_vacuna}</td>
            <td>${vacuna.nombre_vacuna}</td>
            <td>${vacuna.descripcion_vacuna}</td>
            <td>${vacuna.precio_vacuna}</td>
            <td><button class="btn-edit btn btn-secondary ">Editar</button></td>
            <td><button class="btn-delete btn btn-danger">Eliminar</button></td>
        `;


        const btnDelete = vacunaItem.querySelector('.btn-delete');

        btnDelete.addEventListener('click', async()=>{
            const response = await fetch(`/api/vacunas/${vacuna.id_vacuna}`,{
                method: 'DELETE'
            })
            const data = await response.json()

            vacunas = vacunas.filter(vacuna => vacuna.id_vacuna !== data.id_vacuna)
            renderExamen(vacunas)
        })


        const btnEdit = vacunaItem.querySelector('.btn-edit')

        btnEdit.addEventListener('click', async e =>{
            mostrarFormulario();
            const response = await fetch(`/api/vacunas/${vacuna.id_vacuna}`)
            const data = await response.json()

            vacunaForm["id_vacuna"].value = data.id_vacuna;
            vacunaForm["nombre_vacuna"].value = data.nombre_vacuna;
            vacunaForm["descripcion_vacuna"].value = data.descripcion_vacuna;
            vacunaForm["precio_vacuna"].value = data.precio_vacuna;

            editing_vacuna = true;
            vacunaId = data.id_vacuna;
        })

        vacunaLista.appendChild(vacunaItem);
    })
}