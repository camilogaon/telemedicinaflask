let ordenes =[];



window.addEventListener('DOMContentLoaded', async () => {
    const response = await fetch("/api/historialordenes");
    const data = await response.json();
    ordenes = data
    renderOrden(ordenes)
})


function renderOrden(ordenes){
    const ordenLista = document.querySelector('#ordenLista');

    ordenes.forEach(orden => {
        const ordenItem = document.createElement('tr');
        ordenItem.innerHTML =`
            <td>${orden.name_servicio}</td>
            <td>${orden.precio_servicio}</td>
            <td>${orden.fecha_creacion}</td>

        `;


        ordenLista.appendChild(ordenItem);
    })
}