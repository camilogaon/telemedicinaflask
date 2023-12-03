
function mostrarFormulario() {
    // Obtener el elemento del formulario
    var formulario = document.getElementById("formulario");

    // Mostrar el formulario
    formulario.style.display = "block";
}


// ************EXAMENES*************

const examenForm = document.querySelector('#examenForm');

let examenes = [];

let editing = false;

let examenId = null;

window.addEventListener('DOMContentLoaded', async () => {
    const response = await fetch("/api/examenes");
    const data = await response.json();
    examenes = data
    renderExamen(examenes)
})

examenForm.addEventListener('submit', async e=>{
    e.preventDefault();


    const id_examen = examenForm['id_examen'].value
    const name_examen = examenForm['name_examen'].value
    const description_examen = examenForm['description_examen'].value
    const precio_examen = examenForm['precio_examen'].value


    if (!editing){
        const response = await fetch('/api/examenes', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                id_examen,
                name_examen,
                description_examen,
                precio_examen
            })
        })
    
        const data = await response.json()
        
        examenes.push(data)
    }else{
        const response = await fetch(`/api/examenes/${examenId}`,{
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                id_examen,
                name_examen,
                description_examen,
                precio_examen
            })
        })
        const updateExamen = await response.json();
        examenes = examenes.map(examen =>examen.id_examen === updateExamen.id_examen ? updateExamen : examen)
        renderExamen(examenes)
        editing = false
        examenId = null
    }

    renderExamen(examenes)

    examenForm.reset();
} )

// function renderExamen(examenes){
//     const examenList =  document.querySelector('#examenList')
//     examenList.innerHTML = ''

//     examenes.forEach(examen => {
//         const examenItem = document.createElement('li')
//         examenItem.innerHTML = `
//             <h5>${examen.name_examen}</h5>
//             <p>${examen.description_examen}</p>
//             <p>${examen.precio_examen}</p>
//         `
//         console.log(examenItem)
//         examenList.append(examenItem)
//     })

    
// }


function renderExamen(examenes) {
    const examLista = document.querySelector('#examLista');
  
    examenes.forEach(examen => {
      const examenItem = document.createElement('tr');
      examenItem.innerHTML = `
        <td>${examen.id_examen}</td>
        <td>${examen.name_examen}</td>
        <td>${examen.description_examen}</td>
        <td>${examen.precio_examen}</td>
        <td><button class="btn-edit btn btn-secondary ">Editar</button></td>
        <td><button class="btn-delete btn btn-danger">Eliminar</button></td>
        
      `;


      //Headle delete Button
      const btnDelete = examenItem.querySelector('.btn-delete')
      
      
      btnDelete.addEventListener('click', async() =>{
        const response = await fetch(`/api/examenes/${examen.id_examen}`,{
            method: 'DELETE'
        })
        const data = await response.json()
        
        
        examenes = examenes.filter(examen => examen.id_examen !== data.id_examen)
        renderExamen(examenes)
      })


      //headle edit button
      const btnEdit = examenItem.querySelector('.btn-edit')

      btnEdit.addEventListener('click', async e => {

        mostrarFormulario();

        const response = await fetch(`/api/examenes/${examen.id_examen}`)
        const data = await response.json()
        
        
        examenForm["id_examen"].value = data.id_examen;
        examenForm["name_examen"].value = data.name_examen;
        examenForm["description_examen"].value = data.description_examen;
        examenForm["precio_examen"].value = data.precio_examen;

        editing = true;
        examenId= data.id_examen;
      })

      examLista.appendChild(examenItem);
    });
  }
