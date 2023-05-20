const proxyURL = 'http://127.0.0.1:8000';
const CSRFToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

// Containers
const diagnosticHomePage = document.querySelector('#diagnostic-home-page');
const diagnosticFormPage = document.querySelector('#diagnostic-form-page');

const evolutionHomePage = document.querySelector('#evolution-home-page');
const evolutionFormPage = document.querySelector('#evolution-form-page');

const testHomePage = document.querySelector('#test-home-page');
const patientTestFormPage = document.querySelector('#patient-test-form-page');
const testFormPage = document.querySelector('#test-form-page');

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
    patientFormSubmitter.classList.add('d-none');
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
    patientFormSubmitter.classList.remove('d-none');
})

// functions related to input validation
function setActiveTab(tabId) {
    var tabElement = document.getElementById(tabId);
    if (tabElement) {
        // Remove 'active' class from all tab links
        var tabLinks = document.getElementsByClassName('nav-link');
        for (var i = 0; i < tabLinks.length; i++) {
        tabLinks[i].classList.remove('active');
        }

        // Add 'active' class to the selected tab link
        tabElement.classList.add('active');

        // Show the corresponding tab content
        var tabContentId = tabElement.getAttribute('data-bs-target');
        var tabContentElement = document.querySelector(tabContentId);
        if (tabContentElement) {
        // Remove 'active' class from all tab panes
        var tabPanes = document.getElementsByClassName('tab-pane');
        for (var j = 0; j < tabPanes.length; j++) {
            tabPanes[j].classList.remove('show', 'active');
        }

        // Add 'active' class to the selected tab pane
        tabContentElement.classList.add('show', 'active');
        }
    }
}
  
function getMessageFromValidity(inputElement) {
    if (inputElement.validity.valueMissing) {
      return 'Campo requerido.';
    }
  
    if (inputElement.validity.typeMismatch) {
      return 'Tipo de dato incorrecto.';
    }
  
    if (inputElement.validity.patternMismatch) {
      return 'Patrón inválido.';
    }
  
    return 'Valor inválido.';
}
  
function validateMarkedInputs(tagClass) {
    const inputs = document.querySelectorAll(tagClass);

    if (inputs.length > 0) {

        // for (let input of inputs) {
        //     console.log(input, input.validity.valid);
        // }

        let formIsValid = true
        for (let input of inputs) {

            if (!input.validity.valid) {

                let invalidInputTabPane = input.closest('.tab-pane');

                if (invalidInputTabPane) {
                    let tabId = invalidInputTabPane.getAttribute('aria-labelledby');
                    setActiveTab(tabId);
                } else {
                    console.log('closest tab-pane not found :(')
                }

                const message = document.createElement('div');
                message.textContent=getMessageFromValidity(input);
                message.classList.add('detected-as-invalid');
                input.parentNode.appendChild(message);

                setTimeout(() => {
                    message.remove();
                }, 5000)

                formIsValid = false;
                break;
            }
        }

        return formIsValid;

    } else {
        console.log(`No inputs with class "${tagClass}".`)
        return false
    }
    
}

// Submit functions
function submitMainForm() {
    if (validateMarkedInputs('.django-patient-form')) {

        const secundaryInputs = document.querySelectorAll(
            `.django-diagnostic-form,
            .django-evolution-form,
            .django-patient-test-form,
            .django-test-form`
        )

        secundaryInputs.forEach(input => {
            console.log(input.name);
            console.log(input.required);
            input.required = false;
            console.log(input.required);
        })

        const mainForm = document.getElementById('main-form')
        mainForm.submit();

    }
}

async function submitDiagnosticData() {

    if (validateMarkedInputs('.django-diagnostic-form')) {
        var code = document.getElementById('id_diagnostic_code').value;
        var description = document.getElementById('id_diagnostic_description').value;

        const response = await fetch(`${proxyURL}/diagnostico/crear`, {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': CSRFToken
            },
            body: JSON.stringify({
                diagnostic_code: code,
                diagnostic_description: description,
                is_active: true
            })
        });
        const data = await response.json();
        const diagnosticSelection = document.getElementById('id_diagnostico');
        var diagnosticOption = document.createElement('option');
        diagnosticOption.value = data.id;
        diagnosticOption.textContent = `${data.diagnostic_code} - ${data.diagnostic_description}`;
        diagnosticSelection.appendChild(diagnosticOption);
        diagnosticSelection.value = data.id;
        diagnosticFormPage.classList.add('d-none');
        diagnosticHomePage.classList.remove('d-none');
        patientFormSubmitter.classList.remove('d-none');
        console.log(data);
    }
}

async function submitTestData() {

    if (validateMarkedInputs('.django-test-form')) {
        var name = document.getElementById('id_test_name').value;
        var description = document.getElementById('id_test_description').value;
        var category = document.getElementById('id_category').value;
        var subcategory = document.getElementById('id_subcategory').value;
        var resutlType = document.getElementById('id_result_type').value;
        // var body = JSON.stringify({
        //     nombre: name,
        //     descripcion: description,
        //     categoria: category, 
        //     subcategoria: subcategory,
        //     tipo_resultado: resutlType
        // })

        // console.log(body);

        const response = await fetch(`${proxyURL}/test/crear`, {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': CSRFToken
            },
            body: JSON.stringify({
                test_name: name,
                test_description: description,
                category: category, 
                subcategory: subcategory,
                result_type: resutlType
            })
        });
        const data = await response.json();
        const testSelection = document.getElementById('id_test');
        var testOption = document.createElement('option');
        testOption.value = data.id;
        testOption.textContent = `${data.category} - ${data.subcategory} - ${data.test_name}`;
        testSelection.appendChild(testOption);
        testSelection.value = data.id;
        testFormPage.classList.add('d-none');
        patientTestFormPage.classList.remove('d-none');
        patientFormSubmitter.classList.remove('d-none');
        console.log(data);
    }
    
}

// Submitters
const patientFormSubmitter =document.getElementById('patient-form-submitter');
patientFormSubmitter.addEventListener('click', (e) =>{
    e.preventDefault()
    submitMainForm()
})

const diagnosticFormSubmitter = document.getElementById('diagnostic-form-submitter');
diagnosticFormSubmitter.addEventListener('click', (e) => {
    e.preventDefault()
    submitDiagnosticData();
})

const testFormSubmitter = document.getElementById('test-form-submitter');
testFormSubmitter.addEventListener('click', (e) => {
    e.preventDefault()
    submitTestData();
})







// // Tests
// function buttonFunction() {
//     const pageInputs = document.querySelectorAll('.django-patient-form, .django-test-form');
//     pageInputs.forEach(input => {
        
//         console.log(input.name);
//     })
//     console.log(pageInputs.length);;    

// }

// const testButton = document.getElementById('test-button');
// testButton.addEventListener('click', buttonFunction);
