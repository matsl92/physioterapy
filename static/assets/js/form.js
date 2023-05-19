const proxyURL = 'http://127.0.0.1:8000';
const CSRFToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

// Displayers
const diagnosticFormDisplayer = document.getElementById('diagnostic-form-displayer');
diagnosticFormDisplayer.addEventListener('click', (e) => {
    e.preventDefault();
    patientFormSubmitter.classList.add('d-none');
    diagnosticHomePage.classList.add('d-none');
    diagnosticFormPage.classList.remove('d-none');
})

const evolutionFormDisplayer = document.getElementById('evolution-form-displayer');
evolutionFormDisplayer.addEventListener('click', (e) => {
    e.preventDefault();
    evolutionHomePage.classList.add('d-none');
    evolutionFormPage.classList.remove('d-none');
})

const patientTestFormDisplayer = document.getElementById('patient-test-form-displayer');
patientTestFormDisplayer.addEventListener('click', (e) =>{
    e.preventDefault();
    testHomePage.classList.add('d-none');
    patientTestFormPage.classList.remove('d-none');
});

const testFormDisplayer = document.getElementById('test-form-displayer');
testFormDisplayer.addEventListener('click', (e) => {
    e.preventDefault();
    patientTestFormPage.classList.add('d-none');
    testFormPage.classList.remove('d-none');
})

// Hiders
const diagnosticFormHider = document.getElementById('diagnostic-form-hider');
diagnosticFormHider.addEventListener('click', (e) => {
    e.preventDefault();
    diagnosticFormPage.classList.add('d-none');
    diagnosticHomePage.classList.remove('d-none');
    patientFormSubmitter.classList.remove('d-none');
})

const evolutionFormHider = document.getElementById('evolution-form-hider');
evolutionFormHider.addEventListener('click', (e) => {
    e.preventDefault();
    evolutionFormPage.classList.add('d-none');
    evolutionHomePage.classList.remove('d-none')
})

const patientTestFormHider = document.getElementById('patient-test-form-hider');
patientTestFormHider.addEventListener('click', (e) => {
    e.preventDefault();
    patientTestFormPage.classList.add('d-none');
    testHomePage.classList.remove('d-none');
})

const testFormHider = document.getElementById('test-form-hider');
testFormHider.addEventListener('click', (e) => {
    e.preventDefault();
    testFormPage.classList.add('d-none');
    patientTestFormPage.classList.remove('d-none');
})

// Submitters
const patientFormSubmitter =document.getElementById('patient-form-submitter');

const diagnosticFormSubmitter = document.getElementById('diagnostic-form-submitter');
diagnosticFormSubmitter.addEventListener('click', (e) => {
    submitDiagnosticData(e);
})

const testFormSubmitter = document.getElementById('test-form-submitter');
testFormSubmitter.addEventListener('click', (e) => {
    submitTestData(e);
})

// Containers
const diagnosticHomePage = document.querySelector('#diagnostic-home-page');
const diagnosticFormPage = document.querySelector('#diagnostic-form-page');

const evolutionHomePage = document.querySelector('#evolution-home-page');
const evolutionFormPage = document.querySelector('#evolution-form-page');

const testHomePage = document.querySelector('#test-home-page');
const patientTestFormPage = document.querySelector('#patient-test-form-page');
const testFormPage = document.querySelector('#test-form-page');


// Submitting functions
async function submitDiagnosticData(e) {

    e.preventDefault();

    var code = document.getElementById('id_code').value;
    var description = document.getElementById('id_description').value;
    var is_active = document.getElementById('id_is_active').value;

    const response = await fetch(`${proxyURL}/diagnostico/crear`, {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': CSRFToken
        },
        body: JSON.stringify({
            code: code,
            description: description,
            is_active: is_active
        })
    });
    const data = await response.json();
    const diagnosticSelection = document.getElementById('id_diagnostico');
    var diagnosticOption = document.createElement('option');
    diagnosticOption.value = data.id;
    diagnosticOption.textContent = `${data.code} - ${data.description}`;
    diagnosticSelection.appendChild(diagnosticOption);
    diagnosticSelection.value = data.id;
    diagnosticFormPage.classList.add('d-none');
    diagnosticHomePage.classList.remove('d-none');
    console.log(data);
}

async function submitTestData(e) {

    e.preventDefault();

    var name = document.getElementById('id_test_nombre').value;
    var description = document.getElementById('id_descripcion').value;
    var category = document.getElementById('id_categoria').value;
    var subcategory = document.getElementById('id_subcategoria').value;
    var resutlType = document.getElementById('id_tipo_resultado').value;
    var body = JSON.stringify({
        nombre: name,
        descripcion: description,
        categoria: category, 
        subcategoria: subcategory,
        tipo_resultado: resutlType
    })

    console.log(body);

    const response = await fetch(`${proxyURL}/test/crear`, {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': CSRFToken
        },
        body: JSON.stringify({
            nombre: name,
            descripcion: description,
            categoria: category, 
            subcategoria: subcategory,
            tipo_resultado: resutlType
        })
    });
    const data = await response.json();
    const testSelection = document.getElementById('id_test');
    var testOption = document.createElement('option');
    testOption.value = data.id;
    testOption.textContent = `${data.categoria} - ${data.subcategoria} - ${data.nombre}`;
    testSelection.appendChild(testOption);
    testSelection.value = data.id;
    testFormPage.classList.add('d-none');
    patientTestFormPage.classList.remove('d-none');
    console.log(data);
}






