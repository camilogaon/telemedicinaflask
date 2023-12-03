function mostrarFormulario() {
    // Obtener el elemento del formulario
    var formulario = document.getElementById("formulario");

    // Mostrar el formulario
    formulario.style.display = "block";
}



const especialidadForm = document.getElementById("#especialidadForm");

let especialidades =[];

let editing_especialidad = false;

let especialidadId= null;

window.addEventListener('DOMContentLoaded', async() => {
    const response = await fetch('/api/especialidades');
    const data = await response.json();
    especialidades = data
    renderEspecialidad(especialidades)
})

especialidadForm.addEventListener('submit', async e=>{
    e.preventDefault();

    const id_especialidad = especialidadForm['id_especialidad'].value
    const nombre_especialidad = especialidadForm['nombre_especialidad'].value
    const descripcion_especialidad = especialidadForm['descripcion_especialidad'].value
    const precio_medicamento = especialidadForm['precio_especialidad'].value

    if (!editing_especialidad){
        const response = await fetch('/api/especialidades',{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                id_especialidad,
                nombre_especialidad,
                descripcion_especialidad,
                precio_especialidad
            })
        })

        const data = await response.json()

        especialidades.push(data)
    }else{
        const response = await fetch(`/api/especialidades/${especialidadId}`,{
            method: 'PUT',
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                id_especialidad,
                nombre,especialidad,
                descripcion_especialidad,
                precio_especialidad
            })
        })
        const uodateEspecialidad = await response.json();
        especialidades = especialidades.map(especialidad => especialidad.id_especialidad === updateEspecialidad.id_especialidad ? updateEspecialidad : especialidad)
        renderEspecialidad(especialidades)
        editing_especialidad = false;
        especialidadId = null;
    }

    renderEspecialidad(especialidades)

    especialidadForm.reset()
})


function renderEspecialidad(especialidades) {
    const especialidadLista = document.querySelector('#especialidadLista');

    especialidades.forEach(especialidad =>{
        const especialidadItem = document.createElement('tr');
        especialidadItem.innerHTML =`
            <td>${especialidad.id_especialidad}</td>
            <td>${especialidad.nombre_especialidad}</td>
            <td>${especialidad.descripcion_especialidad}</td>
            <td>${especialidad.precio_especialidad}</td>
            <td><button class="btn-edit btn btn-secondary ">Editar</button></td>
            <td><button class="btn-delete btn btn-danger">Eliminar</button></td>
        `;



    const btnDelete = especialidadItem.querySelector('.btn-delete');

    btnDelete.addEventListener('click', async() =>{
        const response = await fetch(`/api/especialidades/${especialidad.id_especialidad}`,{
            method: 'DELETE',
        })
        const data = await response.json();

        especialidades = especialidades.filter(especialidad => especialidad.id_especialidad !== data.id_especialidad)
        renderEspecialidad(especialidades)
    })

    const btnEdit = especialidadItem.querySelector('.btn-edit');

    btnEdit.addEventListener('click', async e=>{
        mostrarFormulario();

        const response = await fetch(`/api/especialidades/${especialidad.id_especialidad}`)
        const data = await response.json()

        especialidadForm["id_especialidad"].value = data.id_especialidad;
        especialidadForm["nombre_especialidad"].value = data.nombre_especialidad;
        especialidadForm["descripcion_especialidad"].value = data.descripcion_especialidad;
        especialidadForm["precio_especialidad"].value = data.precio_especialidad;

        editing_especialidad = true;
        especialidadId = data.id_especialidad;
    })

    especialidadLista.appendChild(especialidadItem);


})



}