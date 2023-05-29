const data = JSON.parse(document.getElementById('js-variables').textContent);
const proxyURL = data.root_url;
const CSRFToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
const url = window.location.href;

// Containers
const diagnosisHomePage = document.querySelector('#diagnosis-home-page');
const diagnosisFormPage = document.querySelector('#diagnosis-form-page');

const evolutionHomePage = document.querySelector('#evolution-home-page');
const evolutionFormPage = document.querySelector('#evolution-form-page');

const testHomePage = document.querySelector('#test-home-page');
const patientTestFormPage = document.querySelector('#patient-test-form-page');
const testFormPage = document.querySelector('#test-form-page');

// Items

const pillControllers = document.querySelectorAll('#pills-tab.nav.nav-pills .nav-item .nav-link');

// Displayers
const diagnosisFormDisplayer = document.getElementById('diagnosis-form-displayer');
diagnosisFormDisplayer.addEventListener('click', (e) => {
    e.preventDefault();
    disablePillControllers()
    patientFormSubmitter.classList.add('d-none');
    diagnosisHomePage.classList.add('d-none');
    diagnosisFormPage.classList.remove('d-none');
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
    disablePillControllers()
    patientFormSubmitter.classList.add('d-none');
    patientTestFormPage.classList.add('d-none');
    testFormPage.classList.remove('d-none');
})

// Hiders
const diagnosisFormHider = document.getElementById('diagnosis-form-hider');
diagnosisFormHider.addEventListener('click', (e) => {
    e.preventDefault();
    clearMarkedFields('.django-diagnosis-form');
    diagnosisFormPage.classList.add('d-none');
    diagnosisHomePage.classList.remove('d-none');
    patientFormSubmitter.classList.remove('d-none');
    enablePillControllers();
})

const evolutionFormHider = document.getElementById('evolution-form-hider');
evolutionFormHider.addEventListener('click', (e) => {
    e.preventDefault();
    clearMarkedFields('.django-evolution-form');
    evolutionFormPage.classList.add('d-none');
    evolutionHomePage.classList.remove('d-none')
})

const patientTestFormHider = document.getElementById('patient-test-form-hider');
patientTestFormHider.addEventListener('click', (e) => {
    e.preventDefault();
    clearMarkedFields('.django-patient-test-form');
    patientTestFormPage.classList.add('d-none');
    testHomePage.classList.remove('d-none');
})

const testFormHider = document.getElementById('test-form-hider');
testFormHider.addEventListener('click', (e) => {
    e.preventDefault();
    clearMarkedFields('.django-test-form');
    testFormPage.classList.add('d-none');
    patientTestFormPage.classList.remove('d-none');
    patientFormSubmitter.classList.remove('d-none');
    enablePillControllers();
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
            `.django-diagnosis-form,
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

async function submitDiagnosisData() {

    if (validateMarkedInputs('.django-diagnosis-form')) {
        enablePillControllers();
        var code = document.getElementById('id_diagnosis_code').value;
        var description = document.getElementById('id_diagnosis_description').value;

        const response = await fetch(`${proxyURL}/diagnosiso/crear`, {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': CSRFToken
            },
            body: JSON.stringify({
                diagnosis_code: code,
                diagnosis_description: description,
                is_active: true
            })
        });
        const data = await response.json();
        diagnoses.push(data);
        var option = document.createElement('li');
        option.textContent = `${data.code} - ${data.description}`
        option.addEventListener('click', () => selectDiagnosis(data.id));
        optionContainer.appendChild(option);
        console.log('data.id', data.id);
        selectDiagnosis(data.id);
        diagnosisFormPage.classList.add('d-none');
        diagnosisHomePage.classList.remove('d-none');
        patientFormSubmitter.classList.remove('d-none');
        console.log(data);
        clearMarkedFields('.django-diagnosis-form');
        return data;
    }
}

async function submitTestData() {

    if (validateMarkedInputs('.django-test-form')) {
        enablePillControllers();
        var name = document.getElementById('id_test_name').value;
        var description = document.getElementById('id_test_description').value;
        var category = document.getElementById('id_category').value;
        var subcategory = document.getElementById('id_subcategory').value;
        var resutlType = document.getElementById('id_result_type').value;

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
        clearMarkedFields('.django-test-form');
        console.log(data);
    }
    
}

// Submitters
const patientFormSubmitter =document.getElementById('patient-form-submitter');
patientFormSubmitter.addEventListener('click', (e) =>{
    e.preventDefault()
    submitMainForm()
})

const diagnosisFormSubmitter = document.getElementById('diagnosis-form-submitter');
diagnosisFormSubmitter.addEventListener('click', (e) => {
    e.preventDefault()
    submitDiagnosisData();
})

const testFormSubmitter = document.getElementById('test-form-submitter');
testFormSubmitter.addEventListener('click', (e) => {
    e.preventDefault()
    submitTestData();
})

const patientDeleter = document.getElementById('patient-deleter');
if (patientDeleter) {
    patientDeleter.addEventListener('click', async () => {
        fetch(`${proxyURL}/paciente/eliminar/${url.split('/')[url.split('/').length-1]}`)
        window.location.replace(proxyURL);
    })
}

// Other functions

function disablePillControllers() {
    pillControllers.forEach(controller => {
        controller.classList.add('disabled');
    }) 
}

function enablePillControllers() {
    pillControllers.forEach(controller => {
        controller.classList.remove('disabled');
    }) 
}

function clearMarkedFields(formLabel) {
    const fields = document.querySelectorAll(formLabel);
    fields.forEach(field => {
        field.value = ""
    })
}









// ----------------------------------- Search input ------------------------------------------

const diagnoses = [];
const optionContainer = document.querySelector('.option-container ul');
const options = optionContainer.querySelectorAll('li');
const searchInput = document.querySelector('.search-input');
const selectDiagnosisButton = document.getElementById('diagnosis-select');
const searchContainer = document.querySelector('.search-container');
const svg = document.querySelector('.select-diagnosis button svg');
const diagnosisInput = document.getElementById('id_diagnosiso');
const buttonText = document.querySelector('.select-diagnosis button div');


async function getDiagnosisOptions() {
    const response = await fetch(`${proxyURL}/diagnosiso/lista`);
    const data = await response.json();

    diagnoses.length = 0;
    data.forEach(diagnosis => {
        diagnoses.push(diagnosis);
    })

    optionContainer.innerHTML = '';
    var option;
    data.forEach(diagnosis => {
        option = document.createElement('li');
        option.textContent = `${diagnosis.code} - ${diagnosis.description}`;
        option.addEventListener('click', () => selectDiagnosis(diagnosis.id))
        optionContainer.appendChild(option);
    })
}

function selectDiagnosis(id) {
    const diagnosis = diagnoses.find(diagnosis => diagnosis.id == id);
    if (diagnosis) {
        console.log('previous value', diagnosisInput.value);
        buttonText.textContent = diagnosis.description;
        searchContainer.classList.remove('active');
        svg.classList.remove('active');
        console.log('id', diagnosis.id);
        diagnosisInput.value = diagnosis.id;
        console.log('value', diagnosisInput.value);
    }
}

function filterAndAppendOptions(string) {
    filteredOptions = diagnoses.filter(diagnosis => {
        return diagnosis.description.toLowerCase().includes(string.toLowerCase()) || 
        diagnosis.code.toLowerCase().includes(string.toLowerCase());
    })
    optionContainer.innerHTML = "";
    var option;
    filteredOptions.forEach(diagnosis => {
        option = document.createElement('li');
        option.textContent = `${diagnosis.code} - ${diagnosis.description}`;
        option.addEventListener('click', () => selectDiagnosis(diagnosis.id))
        optionContainer.appendChild(option);
    })
}

async function setDiagnosisDefault() {
    await getDiagnosisOptions();
    console.log('diagnosis input value', diagnosisInput.value);
    console.log('diagnoses length', diagnoses.length);
    let diagnosis = diagnoses.find(diagnosis => diagnosis.id == diagnosisInput.value);
    if (diagnosis) {
        buttonText.textContent = diagnosis.description;
    }
    console.log('default diagnosis', diagnosis);
    console.log('value', diagnosisInput.value);
}

searchInput.addEventListener('input', (e) => filterAndAppendOptions(e.target.value));
selectDiagnosisButton.addEventListener('click', (e) => {
    e.preventDefault()
    svg.classList.toggle('active');
    searchContainer.classList.toggle('active');
})
window.addEventListener('load', () => {
    setDiagnosisDefault();
})

// testButton = document.getElementById('test-button');
// testButton.addEventListener('click', (e) => {
//     e.preventDefault();
//     setDiagnosisDefault();
// })