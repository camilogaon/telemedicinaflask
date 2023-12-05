function mostrarFormulario() {
    // Obtener el elemento del formulario
    var formulario = document.getElementById("formulario");

    // Mostrar el formulario
    formulario.style.display = "block";
}

const usuarioForm = document.querySelector('#usuarioForm');

let usuarios =[];

let editing_usuario = false;

let usuarioId = null;

window.addEventListener('DOMContentLoaded', async () => {
    const response = await fetch("/api/usuarios");
    const data = await response.json();
    usuarios = data
    renderUsuario(usuarios)

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


function renderUsuario(usuarios){
    const usuarioLista = document.querySelector('#usuarioLista');

    usuarios.forEach(usuario => {
        const usuarioItem = document.createElement('tr');
        usuarioItem.innerHTML =`
            <td>${usuario.id}</td>
            <td>${usuario.username}</td>
            <td>${usuario.lastname}</td>
            <td>${usuario.email}</td>
            <td><button class="btn-edit btn btn-secondary ">Editar</button></td>
            <td><button class="btn-delete btn btn-danger">Eliminar</button></td>
        `;

        usuarioLista.appendChild(usuarioItem);
    })
}

