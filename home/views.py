from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template import loader
from django import template
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.shortcuts import redirect
from .forms import PatientForm, DiagnosticForm, EvolutionForm, TestForm, PatientTestForm
from .models import Patient, Evolution, PatientTest
import json


from bs4 import BeautifulSoup
import requests
from .models import Diagnostic

# def get_errors_with_format(errors):
#     if len(errors.items()) > 0:
#         error_msg = "ERRORES\n"
#         for key, value in errors.items():
#             error_msg += f"\n{key.capitalize().replace('_', ' ')}\n"
#             for inner_key, inner_value in value.items():
#                 error_msg += f"   Campo {inner_key}: "
#                 field_errors = []
#                 for err in inner_value:
#                     field_errors.append(err.strip('.').casefold())
#                 error_msg += f"{', '.join(field_errors).capitalize()}.\n"
#         return error_msg
#     else:
#         return ""

def get_errors_with_format(errors):
    if len(errors.items()) > 0:
        error_msg = "No se guardaron todos los campos. "
        for key, value in errors.items():
            error_msg += f"\n{key.capitalize().replace('_', ' ')}\n"
            for inner_key, inner_value in value.items():
                error_msg += f"   Campo {inner_key}: "
                field_errors = []
                for err in inner_value:
                    field_errors.append(err.strip('.').casefold())
                error_msg += f"{', '.join(field_errors).capitalize()}.\n"
        return error_msg
    else:
        return ""
   
def get_messages_with_format(msgs):
    normalized_messages = [msg.strip('.').casefold() for msg in msgs]
    return f"{', '.join(normalized_messages).capitalize()}."

@login_required
def index(request):
    context = {'segment': 'index'}
    return render(request, 'home/index.html', context)

@login_required
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]
        
        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return render(request, 'home/' + load_template, context)

    except template.TemplateDoesNotExist:
        
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))
    
    except:
        
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

def example(request):
    context = {}
    context['segment'] = 'example'
    return render(request, 'home/example.html', context)

@login_required
def create_patient(request):
    if request.method == 'GET': 
        context = {
            'segment': 'form', 
            'patient_form': PatientForm(), 
            'diagnostic_form': DiagnosticForm(),
            'evolution_form': EvolutionForm(),
            'patient_test_form': PatientTestForm(),
            'test_form': TestForm(),
            'evolution_records': None,
            'patient_tests': None,
        }
        
        return render(request, 'home/form.html', context)
    
    if request.method == 'POST':
        patient_form = PatientForm(request.POST, request.FILES)
        msgs = []
        errors = {}
        if patient_form.is_valid():
            patient = patient_form.save()
            msgs.append("Se guardó el nuevo paciente.")
            
            if request.POST.get('evolution_record') != '':
                evolution_form = EvolutionForm({
                    **request.POST.dict(),
                    **{'patient': patient}
                })
                if evolution_form.is_valid():
                    evolution_form.save()
                    msgs.append("Se añadió una evolución al paciente.")
                else:
                    errors['formulario_de_evolución'] = evolution_form.errors
            
            if request.POST.get('test') != '' or request.POST.get('result') != '':
                patient_test_form = PatientTestForm({
                    **request.POST.dict(),
                    **{'patient': patient}
                })
                if patient_test_form.is_valid():
                    patient_test_form.save()
                    msgs.append("Se añadió un test al paciente.")
                else:
                    errors['formulario_de_test_del_paciente'] = patient_test_form.errors
            
            if len(errors.items()) > 0:
                messages.warning(request, get_errors_with_format(errors))        
                        
            messages.success(request, get_messages_with_format(msgs))
            return redirect('home:patients')
        
        else:
            errors['formulario_de_paciente'] = patient_form.errors
            msgs.append("No se guardó el nuevo paciente.")
            messages.warning(request, get_messages_with_format(msgs))
            messages.warning(request, get_errors_with_format(errors))
            
            return redirect('home:patients')

@login_required                  
def update_patient(request, id):
    patient = Patient.objects.get(pk=id)
    if request.method == 'GET': 
        context = {
            'segment': 'form', 
            'patient_form': PatientForm(instance=patient), 
            'diagnostic_form': DiagnosticForm(),
            'evolution_form': EvolutionForm(),
            'patient_test_form': PatientTestForm(),
            'test_form': TestForm(),
            'evolution_records': Evolution.objects.filter(patient=patient),
            'patient_tests': PatientTest.objects.filter(patient=patient)
        }
        return render(request, 'home/form.html', context)
    
    if request.method == 'POST':
        patient_form = PatientForm(request.POST, request.FILES, instance=patient)
        msgs = []
        errors = {}
        if patient_form.is_valid():
            patient = patient_form.save()
            msgs.append("Se actualizaron los datos del paciente.")
            
            if request.POST.get('evolution_record') != '':
                evolution_form = EvolutionForm({
                    **request.POST.dict(),
                    **{'patient': patient}
                })
                if evolution_form.is_valid():
                    evolution_form.save()
                    msgs.append("Se añadió una evolución al paciente.")
                else:
                    errors["Formulario_de_evolución: "] = evolution_form.errors
            
            if request.POST.get('test') != '' or request.POST.get('result') != '':
                patient_test_form = PatientTestForm({
                    **request.POST.dict(),
                    **{'patient': patient}
                })
                if patient_test_form.is_valid():
                    patient_test_form.save()
                    msgs.append("Se añadió un test al paciente.")
                else:
                    errors["formulario_de_test:"] = patient_test_form.errors
                    
            if len(errors.items()) > 0:
                messages.warning(request, get_errors_with_format(errors))
                
            messages.success(request, get_messages_with_format(msgs))
            return redirect('home:patients')
        
        else:
            errors["formulario_de_paciente"] = patient_form.errors
            msgs.append("No se actualizaron los datos del paciente.")
            messages.warning(request, get_messages_with_format(msgs))
            messages.warning(request, get_errors_with_format(errors))
            
            return redirect('home:patients')

@login_required            
def patient_list(request):
    context = {
        'object_list': Patient.objects.all().order_by('nombre', 'apellidos'),
        'segment': 'patient_list'
    }
    return render(request, 'home/patient_list.html', context)

def create_diagnostic(request):
    if request.method == 'POST':
        diagnostic_form = DiagnosticForm(json.loads(request.body.decode('utf-8')))
        if diagnostic_form.is_valid():
            diagnostic = diagnostic_form.save()
            return JsonResponse({
                'id': diagnostic.id,
                'code': diagnostic.diagnostic_code,
                'description': diagnostic.diagnostic_description
            })
        else:
            return JsonResponse(diagnostic_form.errors.as_json(), safe=False)
        
def create_test(request):
    if request.method == 'POST':
        test_form = TestForm(json.loads(request.body.decode('utf-8')))
        if test_form.is_valid():
            test = test_form.save()
            return JsonResponse({
                'id': test.id,
                'test_name': test.test_name,
                'test_description': test.test_description,
                'category': test.category.category_name,
                'subcategory': test.subcategory,
                'result_type': test.result_type
            })
        else:
            return JsonResponse(test_form.errors.as_json(), safe=False)
  
def get_patient_list(request):
    data = [
        {
            'cedula': patient.cedula,
            'nombre': patient.nombre,
            'apellidos': patient.apellidos,
            'telefono': patient.telefono,
            'updated_at': patient.updated_at
        }
    for patient in list(Patient.objects.all().order_by('-updated_at'))]
    return JsonResponse(data, safe=False)   

def get_diagnosis_list(request):
    return JsonResponse(
        [{
            'id': diagnosis.id,
            'code': diagnosis.diagnostic_code,
            'description': diagnosis.diagnostic_description
        } for diagnosis in Diagnostic.objects.filter(is_active=True)],
        safe=False
    )

def populatate_database(request):
    url = "https://es.wikipedia.org/wiki/Anexo:CIE-10_Cap%C3%ADtulo_XIII:_Enfermedades_del_sistema_osteomuscular_y_del_tejido_conectivo"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    content = soup.find("div",{"id":"mw-content-text"})
    first_level_uls = [item for item in content.find_all("ul")]

    all_second_level_lis = []
    
    for first_level_ul in first_level_uls:
        if first_level_ul.find_all('li') is not None:

            first_level_lis = [li for li in first_level_ul.find_all('li')]
            for first_level_li in first_level_lis:
                if first_level_li.find_all('ul') is not None:

                    second_level_uls = [ul for ul in first_level_li.find_all('ul')]
                    for second_level_ul in second_level_uls:
                        if second_level_ul.find_all('li') is not None:

                            second_level_lis = [li for li in second_level_ul.find_all('li')]
                            for li in second_level_lis:
                                all_second_level_lis.append(li)
    
    for li in all_second_level_lis:
        string = li.get_text().strip()
        chars = [char for char in string]
        code = ''.join(chars[0:7]).strip('()')
        description = ''.join(chars[7:]).strip()
        
        diagnostic = Diagnostic.objects.create(
            diagnostic_code=code, 
            diagnostic_description=description, 
            is_active=True
        )

        diagnostic.save()
        
    data = [
        {
            'code': diagnostic.diagnostic_code,
            'description': diagnostic.diagnostic_description
        }
    for diagnostic in list(Diagnostic.objects.all())]
    return JsonResponse(data, safe=False)
        






