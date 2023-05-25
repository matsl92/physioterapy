let rowHeight;
if (window.innerWidth > 586) {
    rowHeight = 46;
} else {
    rowHeight = 67;
}

const nPatientPerPage = Math.floor((window.innerHeight - 265 - 50 - 24 - 30 - 16) / rowHeight);
//                                                            head pad  mar mar table   66.5
const proxyURL = 'http://127.0.0.1:8000';

async function getPatients() {
    const response = await fetch(`${proxyURL}/paciente/lista`);
    const data = await response.json();
    const totalPages = Math.ceil(data.length / nPatientPerPage);
    if (data.length > nPatientPerPage) {
        createPagination(data, totalPages);
        createPaginationControls(totalPages);
    } else {
        populateTableBody(data);
    }
}

function populateTableBody(data) {
    const tableBody = document.createElement('tbody');

    data.forEach(patient => {
        var row = document.createElement('tr');
        var cedula = document.createElement('td');
        cedula.textContent = patient.cedula;
        row.appendChild(cedula);
        var nombre = document.createElement('td');
        nombre.textContent = patient.nombre;
        row.appendChild(nombre);
        var apellidos = document.createElement('td');
        apellidos.textContent = patient.apellidos;
        row.appendChild(apellidos);
        var telefono = document.createElement('td');
        telefono.textContent = patient.telefono;
        row.appendChild(telefono);
        var updated_at = document.createElement('td');
        updated_at.textContent = patient.updated_at;
        row.appendChild(updated_at);

        var view = document.createElement('td');
        var link = document.createElement('a');
        link.textContent = "Ver";
        link.href = `/paciente/actualizar/${patient.cedula}`
        view.textContent = link;
        row.appendChild(view);
        tableBody.appendChild(row);
    })

    const table = document.querySelector('table');
    table.appendChild(tableBody);
    
}

function createPagination(data, totalPages) {

    

    const tabContent = document.getElementById('pills-tabContent');
    
    // Iterate over the pages
    for (let page = 1; page <= totalPages; page++) {

        const tabPane = document.createElement('div');
        // const table = document.querySelector('table').cloneNode(true);
        const table = document.querySelector('table').cloneNode();
        const tableBody = document.createElement('tbody');

        // Determine the start and end index of objects for the current page
        const startIndex = (page - 1) * nPatientPerPage;
        const endIndex = startIndex + nPatientPerPage;
        
        // Slice the data to get objects for the current page
        const pageData = data.slice(startIndex, endIndex);
        
        // Create a table row for each object on the current page
        pageData.forEach(patient => {
            const row = document.createElement('tr');
            
            // Add table cells with patient information
            row.innerHTML = `
            <td>${patient.cedula}</td>
            <td>${patient.nombre}</td>
            <td>${patient.apellidos}</td>
            <td>${patient.telefono}</td>
            <td>${patient.updated_at}</td>
            <th><a href="/paciente/actualizar/${patient.cedula}">Ver</a></th>
            `;
            
            // Append the row to the table body
            tableBody.appendChild(row);
        });
        table.appendChild(tableBody);
        tabPane.appendChild(table);
        tabPane.id = `pills-${page}`;
        tabPane.setAttribute('aria-labelledby', `pills-${page}-tab`);
        tabPane.setAttribute('role', 'tabpanel');
        tabPane.setAttribute('tabindex', '0'); 
        tabPane.classList.add('tab-pane', 'fade'); // <div class="tab-pane fade show active d-none" id="pills-1" role="tabpanel" aria-labelledby="pills-1-tab" tabindex="0">
        if (page == 1) {
            tabPane.classList.add('show', 'active');
        }
        tabContent.appendChild(tabPane);
    }

    // const navLink = document.getElementById("pills-1-tab");


    // navLink.classList.add('active');
    // const activeTabPane = document.getElementById('pills-1');
    // activeTabPane.classList.add('show', 'active');
}

function createPaginationControls(totalPages) {

    const unorderedList = document.querySelector('.nav.nav-pills');

    function addPaginationLinks() {
        const liTag = document.createElement('a');
        liTag.classList.add('page-item');
        const aTag = document.createElement('a');
        aTag.classList.add('page-link');
        aTag.setAttribute('data-bs-toggle', 'pill');
        aTag.setAttribute('role', 'tab');

        var liElement;
        var aElement;
        for (let index = 1; index <= totalPages; index++) {
            aElement = aTag.cloneNode();
            aElement.id = `pills-${index}-tab`;
            aElement.setAttribute('data-bs-target', `#pills-${index}`);
            aElement.setAttribute('aria-controls', `pills-${index}`);
            aElement.textContent = index;
            liElement = liTag.cloneNode();
            if (index == 1) {
                aElement.classList.add('active');
                aElement.setAttribute('aria-selected', 'true');
            } else {
                aElement.setAttribute('aria-selected', 'false');
            }
            liElement.appendChild(aElement);
            unorderedList.appendChild(liElement)
        }
    }

    if (totalPages > 3) {
        const previousControl = document.querySelector('.arrow-paginator.previous');
        const nextControl = document.querySelector('.arrow-paginator.next');
        unorderedList.appendChild(previousControl);
        addPaginationLinks();
        unorderedList.appendChild(nextControl);
    } else {
        addPaginationLinks()
    }
}

window.addEventListener('load', getPatients);