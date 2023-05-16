// const data = JSON.parse(document.getElementById('js-variables').textContent);
// console.log(data);

const proxyURL = 'http://127.0.0.1:8000';
const CSRFToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

const diagnosticFormAdder = document.getElementById('diagnostic-form-adder');
const evolutionFormAdder = document.getElementById('evolution-form-adder')
const testFormAdder = document.getElementById('test-form-adder');

const diagnosticFormContainer =document.querySelector('#pills-diagnostico .col-md-12');
const evolutionFormContainer = document.querySelector('#pills-evolucion .col-md-12');
const testFormContainer = document.querySelector('#pills-test .col-md-12');


// Replace or add values to these elements

const diagnosticSelection = document.getElementById('id_diagnostico');


function addDiagnosticForm(e) {

    e.preventDefault();

    const diagnosticForm = document.createElement('form');

    const label1 = document.createElement('label');
    label1.setAttribute('for', 'code_id');
    // label1.setAttribute('class', 'bmd-label-floating')
    label1.textContent = 'Código';

    const input1 = document.createElement('input');
    input1.setAttribute('max_length', '20');
    input1.setAttribute('type', 'text');
    input1.setAttribute('class', 'form-control');
    input1.required = true;
    input1.name = 'code';
    input1.id = 'code_id';

    const label2 = document.createElement('label');
    label2.setAttribute('for', 'description_id');
    // label2.setAttribute('class', 'bmd-label-floating')
    label2.textContent = 'Descripción';

    const input2 = document.createElement('input');
    input2.setAttribute('max_length', '200');
    input2.setAttribute('type', 'text');
    input2.setAttribute('class', 'form-control');
    input2.required = true;
    input2.name = 'description';
    input2.id = 'description_id';

    const label3 = document.createElement('label');
    label3.setAttribute('for', 'is_active_id');
    // label3.setAttribute('class', 'bmd-label-floating')
    label3.textContent = 'Activo';

    const input3 = document.createElement('input');
    input3.setAttribute('max_length', '20');
    input3.setAttribute('type', 'checkbox');
    input3.checked = true;
    // input3.setAttribute('class', 'form-control');
    input3.required = true;
    input3.name = 'is_active';
    input3.id = 'is_active_id';

    async function sendDiagnosticData(e) {

        e.preventDefault();

        const response = await fetch(`${proxyURL}/diagnostico/crear`, {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': CSRFToken
            },
            body: JSON.stringify({
                code: input1.value,
                description: input2.value,
                is_active: input3.value
            })
        });
        const data = await response.json();
        var diagnosticOption = document.createElement('option');
        diagnosticOption.value = data.id;
        diagnosticOption.textContent = `${data.code} - ${data.description}`
        diagnosticSelection.appendChild(diagnosticOption);
        diagnosticSelection.value = data.id;
        diagnosticForm.remove();
        console.log(data);
    }

    const formElements = [label1, input1, label2, input2, label3, input3];

    var submitButton = document.createElement('button');
    submitButton.value = 'Guardar diagnóstico';
    submitButton.addEventListener('click', sendDiagnosticData);

    var formGroup;

    for (let i = 0; i < formElements.length; i += 2) {
        formElements[i].setAttribute('class', 'bmd-label-static');
        // formElements[i+1].setAttribute('class', 'form-control');

        formGroup = document.createElement('div');
        formGroup.setAttribute('class', 'form-group');
        formGroup.appendChild(formElements[i]);
        formGroup.appendChild(formElements[i+1]);
        diagnosticForm.appendChild(formGroup);
    }

    // diagnosticForm.appendChild(label1);
    // diagnosticForm.appendChild(input1);
    // diagnosticForm.appendChild(label2);
    // diagnosticForm.appendChild(input2);
    // diagnosticForm.appendChild(label3);
    // diagnosticForm.appendChild(input3);

    diagnosticForm.appendChild(submitButton);
    diagnosticFormContainer.appendChild(diagnosticForm);

}

function addTestForm(e) {
    
    e.preventDefault()


    console.log('add test form');
}

function addEvolutionForm(e) {
    e.preventDefault();
    console.log('add evolution form');
    console.log(e);
}

testFormAdder.addEventListener('click', addTestForm);
// evolutionFormAdder.addEventListener('click', add)
diagnosticFormAdder.addEventListener('click', addDiagnosticForm)