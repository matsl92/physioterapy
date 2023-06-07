const data = JSON.parse(document.getElementById('js-variables').textContent);
const proxyURL = data.root_url;
const CSRFToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
const url = window.location.href;

// Containers
const diagnosisHomePage = document.querySelector('#diagnosis-home-page');
const patientDiagnosisFormPage = document.querySelector('#patient-diagnosis-form-page');

const evolutionHomePage = document.querySelector('#evolution-home-page');
const evolutionFormPage = document.querySelector('#evolution-form-page');

const testHomePage = document.querySelector('#test-home-page');
const patientTestFormPage = document.querySelector('#patient-test-form-page');

const documentHomePage = document.querySelector('#document-home-page');
const documentFormPage = document.querySelector('#document-form-page');

// Displayers
const patientDiagnosisFormDisplayer = document.getElementById('patient-diagnosis-form-displayer');
patientDiagnosisFormDisplayer.addEventListener('click', (e) => {
    e.preventDefault();
    diagnosisHomePage.classList.add('d-none');
    patientDiagnosisFormPage.classList.remove('d-none');
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

// const documentFormDisplayer = document.getElementById('document-form-displayer');
// documentFormDisplayer.addEventListener('click', (e) => {
//     e.preventDefault();
//     documentHomePage.classList.add('d-none');
//     documentFormPage.classList.remove('d-none');
// })

// Hiders
const patientDiagnosisFormHider = document.getElementById('patient-diagnosis-form-hider');
patientDiagnosisFormHider.addEventListener('click', (e) => {
    e.preventDefault();
    clearMarkedFields('.django-patient-diagnosis-form');
    document.querySelector('#diagnosis-select div').textContent = "Seleccionar";
    patientDiagnosisFormPage.classList.add('d-none');
    diagnosisHomePage.classList.remove('d-none');
})

const evolutionFormHider = document.getElementById('evolution-form-hider');
evolutionFormHider.addEventListener('click', (e) => {
    e.preventDefault();
    clearMarkedFields('.django-evolution-form');
    evolutionFormPage.classList.add('d-none');
    evolutionHomePage.classList.remove('d-none');
})

const patientTestFormHider = document.getElementById('patient-test-form-hider');
patientTestFormHider.addEventListener('click', (e) => {
    e.preventDefault();
    clearMarkedFields('.django-patient-test-form');
    document.querySelector('#test-select div').textContent = "Seleccionar";
    patientTestFormPage.classList.add('d-none');
    testHomePage.classList.remove('d-none');
})

// const documentFormHider = document.getElementById('document-form-hider');
// documentFormHider.addEventListener('click', (e) => {
//     e.preventDefault();
//     clearMarkedFields('.django-attached-file-form');
//     documentFormPage.classList.add('d-none');
//     documentHomePage.classList.remove('d-none');
// })

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
        const mainForm = document.getElementById('main-form');
        mainForm.submit();
    }
}

async function submitAttachedFileForm() {
    if (validateMarkedInputs('.django-attached-file-form')) {
        const fileInput = document.getElementById('id_file');
        const payload = new FormData();
        payload.append('patient', Number(document.getElementById('id_patient').value));
        payload.append('file', fileInput.files[0])
        const response = await fetch(
            `${proxyURL}/documento_adjunto/crear`,
            {
                method: 'post',
                headers: {
                    'X-CSRFToken': CSRFToken
                },
                body: payload
            }
        );
        const data = await response.json();
        const fileContainer = document.querySelector('.file-container');
        const element = document.createElement('div');
        element.setHTML(
            `
            <div class="d-flex flex-row justify-content-between">
                <div><a href=/media/${data.file}>${data.name}</a></div>
                <div><i>${data.created_at}</i></div>
            </div>
            
            `
        );
        fileContainer.appendChild(element);
        fileInput.value = "";
        HideModal();
    }
}

// Submitters

const patientFormSubmitter =document.getElementById('patient-form-submitter');
patientFormSubmitter.addEventListener('click', (e) =>{
    e.preventDefault()
    submitMainForm()
})

const patientDeleter = document.getElementById('patient-deleter');
if (patientDeleter) {
    patientDeleter.addEventListener('click', async () => {
        fetch(`${proxyURL}/paciente/eliminar/${url.split('/')[url.split('/').length-1]}`)
        window.location.replace(proxyURL);
    })
}

const attachedFileFormSubmitter = document.getElementById('attached-file-form-submitter');
if (attachedFileFormSubmitter) {
    attachedFileFormSubmitter.addEventListener('click', submitAttachedFileForm);
}

// Other functions
function clearMarkedFields(formLabel) {
    const fields = document.querySelectorAll(formLabel);
    fields.forEach(field => {
        field.value = "";
    })
}

function HideModal() {

    closeButton = document.getElementById('attached_file_form_hider');
    closeButton.click();

    // var myModalEl = document.getElementById('exampleModalCenter');
    // console.log(myModalEl);
    // console.log(bootstrap);
    // var modal = bootstrap.Modal.getInstance(myModalEl)
    // modal.hide();

    // const modalContainers = document.querySelectorAll('#exampleModalCenter');
    // const modalBackdrop = document.querySelector('.modal-backdrop.fade');
    // modalContainers.forEach(modal => {
    //     modal.classList.remove('show');
    //     setTimeout(() => {
    //         modal.setAttribute('aria-hidden', 'true');
    //         modal.style.display = 'none';
    //     }, 500)
    //     document.querySelector('body').classList.remove('modal-open');
    // })
    // modalBackdrop.classList.remove('show');
    // setTimeout(() => {
    //     modalBackdrop.style.display = 'none';
    // }, 500)
}

// ----------------------------------- Diagnosis search input ------------------------------------------

const diagnoses = [];
const diagnosisOptionContainer = document.querySelector('#diagnosis-search-container .option-container ul');
const diagnosisSearchInput = document.querySelector('#diagnosis-search-input');
const selectDiagnosisButton = document.getElementById('diagnosis-select');
const diagnosisSearchContainer = document.querySelector('#diagnosis-search-container');
const diagnosisSvg = document.querySelector('#select-diagnosis button svg');
const diagnosisInput = document.getElementById('id_diagnosis');
const diagnosisButtonText = document.querySelector('#select-diagnosis button div');


async function getDiagnosisOptions() {
    const response = await fetch(`${proxyURL}/diagnostico/lista`);
    const data = await response.json();

    diagnoses.length = 0; 
    data.forEach(diagnosis => {
        diagnoses.push(diagnosis);
    })

    diagnosisOptionContainer.innerHTML = '';
    var option;
    data.forEach(diagnosis => {
        option = document.createElement('li');
        option.textContent = `${diagnosis.code} - ${diagnosis.description}`;
        option.addEventListener('click', () => selectDiagnosis(diagnosis.id))
        diagnosisOptionContainer.appendChild(option);
    })
}

function selectDiagnosis(id) {
    const diagnosis = diagnoses.find(diagnosis => diagnosis.id == id);
    if (diagnosis) {
        diagnosisButtonText.textContent = diagnosis.description;
        diagnosisSearchContainer.classList.remove('active');
        diagnosisSvg.classList.remove('active');
        diagnosisInput.value = diagnosis.id;
    }
}

function filterAndAppendOptions(string) {
    filteredOptions = diagnoses.filter(diagnosis => {
        return diagnosis.description.toLowerCase().includes(string.toLowerCase()) || 
        diagnosis.code.toLowerCase().includes(string.toLowerCase());
    })
    diagnosisOptionContainer.innerHTML = "";
    var option;
    filteredOptions.forEach(diagnosis => {
        option = document.createElement('li');
        option.textContent = `${diagnosis.code} - ${diagnosis.description}`;
        option.addEventListener('click', () => selectDiagnosis(diagnosis.id))
        diagnosisOptionContainer.appendChild(option);
    })
}

async function setDiagnosisDefault() {
    await getDiagnosisOptions();
    let diagnosis = diagnoses.find(diagnosis => diagnosis.id == diagnosisInput.value);
    if (diagnosis) {
        diagnosisButtonText.textContent = diagnosis.description;
    }
}

diagnosisSearchInput.addEventListener('input', (e) => filterAndAppendOptions(e.target.value));
selectDiagnosisButton.addEventListener('click', (e) => {
    e.preventDefault()
    diagnosisSvg.classList.toggle('active');
    diagnosisSearchContainer.classList.toggle('active');

})
// ----------------------------------- Test search input ------------------------------------------

const tests = [];
const testOptionContainer = document.querySelector('#test-search-container .option-container ul');
const selectTestButton = document.getElementById('test-select');
const testSearchContainer = document.querySelector('#test-search-container');
const testSvg = document.querySelector('#select-test button svg');
const testInput = document.getElementById('id_test');
const testButtonText = document.querySelector('#select-test button div');
const testFormSecondary = document.querySelectorAll('.test-form-secondary');
const testDetailContainer = document.getElementById('test-detail-container');

function showTextDetails(id) {
    const test = tests.find(test => test.id === id)
    if (test) {
        testDetailContainer.classList.remove('d-none');
        testDetailContainer.querySelector('div h5').textContent = `${test.category} - ${test.subcategory} - ${test.name}`;
        testDetailContainer.querySelector('div p').textContent = test.description;
    }
    else {
        console.log('No test found.')
    }
}

function selectTest(id) {
    const test = tests.find(test => test.id == id);
    if (test) {
        testButtonText.textContent = `${test.category} - ${test.subcategory} - ${test.name}`;
        testFormSecondary.forEach(element => {
            element.classList.remove('d-none');
        })
        testSearchContainer.classList.remove('active');
        testSvg.classList.remove('active');
        testInput.value = test.id;
    }
}

async function getTestOptions() {
    const response = await fetch(`${proxyURL}/test/lista`);
    const data = await response.json();

    tests.length = 0; 
    data.forEach(test => {
        tests.push(test);
    })

    testOptionContainer.innerHTML = '';
    var option;
    data.forEach(test => {
        option = document.createElement('li');
        option.textContent = `${test.category} - ${test.subcategory} - ${test.name}`;
        option.addEventListener('click', () => selectTest(test.id));
        option.addEventListener('mouseover', () => {
            showTextDetails(test.id);
        });
        option.addEventListener('mouseout', () => {
            testDetailContainer.classList.add('d-none');
        });
        testOptionContainer.appendChild(option);
    })
}

selectTestButton.addEventListener('click', (e) => {
    e.preventDefault()
    testFormSecondary.forEach(element => {
        element.classList.toggle('d-none');
    })
    testSvg.classList.toggle('active');
    testSearchContainer.classList.toggle('active');

})

window.addEventListener('load', () => {
    getDiagnosisOptions();
    getTestOptions();
})


