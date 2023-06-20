from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.timezone import localtime
from django.contrib import messages
from django.template import loader
from django import template
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.core.handlers.wsgi import WSGIRequest
import json
import os
from .forms import (
    PatientForm, 
    DiagnosisForm, 
    EvolutionForm, 
    TestForm, 
    PatientTestForm,
    PatientDiagnosisForm,
    AttachedFileForm
)
from .models import (
    Patient, 
    Evolution, 
    PatientTest, 
    PatientDiagnosis, 
    AttachedFile, 
    Test
)
from dotenv import load_dotenv

# For web scraping. Used in populate_database view.
from bs4 import BeautifulSoup
import requests
from .models import Diagnosis

# Variables
load_dotenv()
root_url = os.getenv('ROOT_URL')


# Functions
def get_errors_with_format(errors):
    if len(errors.items()) > 0:
        error_msg = ""
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


# Views
@login_required
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        
        a = 4 / 0

        # load_template = request.path.split('/')[-1]
        
        # if load_template == 'admin':
        #     return HttpResponseRedirect(reverse('admin:index'))
        # context['segment'] = load_template

        # html_template = loader.get_template('home/' + load_template)
        # return render(request, 'home/' + load_template, context)

    except template.TemplateDoesNotExist:
        
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))
    
    except:
        
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

@login_required
def create_patient(request):
    if request.method == 'GET': 
        context = {
            'segment': 'form',
            'patient': None,
            'patient_form': PatientForm(), 
            # 'diagnosis_form': DiagnosisForm(),
            'patient_diagnosis_form': PatientDiagnosisForm(),
            'evolution_form': EvolutionForm(),
            'patient_test_form': PatientTestForm(),
            'attached_file_form': AttachedFileForm(),
            # 'test_form': TestForm(),
            'evolution_records': None,
            'patient_tests': None,
            'patient_diagnoses': None,
            'patient_attached_files': None,
            'js_variables': {'root_url': root_url}
        }
        
        return render(request, 'home/form.html', context)
    
    if request.method == 'POST':
        patient_form = PatientForm(request.POST, request.FILES)
        msgs = []
        errors = {}
        if patient_form.is_valid():
            patient = patient_form.save()
            msgs.append("Se guardó el nuevo paciente.")
            
            if request.FILES.get('file') != None:
                attached_file_form = AttachedFileForm(request.POST, request.FILES)
                if attached_file_form.is_valid():
                    attached_file = attached_file_form.save(commit=False)
                    attached_file.patient = patient
                    attached_file.save()
                    # msgs.append("Se añadió un archivo al paciente.")
                else:
                    errors['No_se_añadió_un_archivo_al_paciente'] = attached_file_form.errors
            
            if request.POST.get('diagnosis') != '':
                patient_diagnosis_form = PatientDiagnosisForm({
                    **request.POST.dict(),
                    **{'patient': patient}
                })
                if patient_diagnosis_form.is_valid():
                    patient_diagnosis_form.save()
                    # msgs.append("Se añadió un diagnóstico al paciente.")
                else:
                    errors['No_se_añadió_un_diagnóstico_al_paciente'] = patient_diagnosis_form.errors
            
            if request.POST.get('evolution_record') != '':
                evolution_form = EvolutionForm({
                    **request.POST.dict(),
                    **{'patient': patient}
                })
                if evolution_form.is_valid():
                    evolution_form.save()
                    # msgs.append("Se añadió una evolución al paciente.")
                else:
                    errors['No_se_añadió_una_evolución_al_paciente'] = evolution_form.errors
            
            if request.POST.get('test') != '' or request.POST.get('result') != '':
                patient_test_form = PatientTestForm({
                    **request.POST.dict(),
                    **{'patient': patient}
                })
                if patient_test_form.is_valid():
                    patient_test_form.save()
                    # msgs.append("Se añadió un test al paciente.")
                else:
                    errors['No_se_añadió_un_test_al_paciente'] = patient_test_form.errors
            
            if len(errors.items()) > 0:
                messages.warning(request, get_errors_with_format(errors))        
                        
            messages.success(request, get_messages_with_format(msgs))
            return redirect('home:patients')
        
        else:
            errors['No_se_pudo_añadir_el_paciente'] = patient_form.errors
            msgs.append("No se guardó el nuevo paciente.")
            messages.warning(request, get_messages_with_format(msgs))
            messages.warning(request, get_errors_with_format(errors))
            
            return redirect('home:patients')

@login_required
def update_patient(request, id):
    patient = Patient.objects.get(pk=id)
    if request.method == 'GET': 
        context = {
            'segment': 'patient_list', 
            'patient': patient,
            'patient_form': PatientForm(instance=patient),
            # 'diagnosis_form': DiagnosisForm(),
            'patient_diagnosis_form': PatientDiagnosisForm(),
            'evolution_form': EvolutionForm(),
            'patient_test_form': PatientTestForm(),
            'attached_file_form': AttachedFileForm(),
            # 'test_form': TestForm(),
            'evolution_records': Evolution.objects.filter(patient=patient).order_by('-id'),
            'patient_tests': PatientTest.objects.filter(patient=patient).order_by('-id'),
            'patient_diagnoses': PatientDiagnosis.objects.filter(patient=patient).order_by('-id'),
            'patient_attached_files': AttachedFile.objects.filter(patient=patient).order_by('-id'),
            'js_variables': {'root_url': root_url}
        }
        
        return render(request, 'home/form.html', context)
    
    if request.method == 'POST':
        patient_form = PatientForm(request.POST, request.FILES, instance=patient)
        msgs = []
        errors = {}
        if patient_form.is_valid():
            patient = patient_form.save()
            msgs.append("Se actualizaron los datos del paciente.")
            
            # if request.FILES.get('file') != None:
            #     attached_file_form = AttachedFileForm(
            #         request.POST, 
            #         request.FILES
            #     )
            #     if attached_file_form.is_valid():
            #         attached_file_form.save()
            #         # msgs.append("Se añadió un archivo al paciente.")
            #     else:
            #         errors['No_se_añadió_un_archivo_al_paciente'] = attached_file_form.errors
            
            if request.POST.get('diagnosis') != '':
                patient_diagnosis_form = PatientDiagnosisForm({
                    **request.POST.dict(),
                    **{'patient': patient}
                })
                if patient_diagnosis_form.is_valid():
                    patient_diagnosis_form.save()
                    # msgs.append("Se añadió un diagnóstico al paciente.")
                else:
                    errors['No_se_añadió_un_diagnóstico_al_paciente'] = patient_diagnosis_form.errors
            
            if request.POST.get('evolution_record') != '':
                evolution_form = EvolutionForm({
                    **request.POST.dict(),
                    **{'patient': patient}
                })
                if evolution_form.is_valid():
                    evolution_form.save()
                    # msgs.append("Se añadió una evolución al paciente.")
                else:
                    errors["No_se_añadió_una_evolución_al_paciente: "] = evolution_form.errors
            
            if request.POST.get('test') != '' or (request.POST.get('result') != '' and request.POST.get('result') != None):
                print('test: ', request.POST.get('test'))
                print('result: ', request.POST.get('result'))
                patient_test_form = PatientTestForm({
                    **request.POST.dict(),
                    **{'patient': patient}
                })
                if patient_test_form.is_valid():
                    patient_test_form.save()
                    # msgs.append("Se añadió un test al paciente.")
                else:
                    errors["No_se_añadió_un_test_al_paciente:"] = patient_test_form.errors
                    
            if len(errors.items()) > 0:
                messages.warning(request, get_errors_with_format(errors))
                
            messages.success(request, get_messages_with_format(msgs))
            return redirect('home:patients')
        
        else:
            errors["No_se_pudo_añadir_el_paciente"] = patient_form.errors
            msgs.append("No se actualizaron los datos del paciente.")
            messages.warning(request, get_messages_with_format(msgs))
            messages.warning(request, get_errors_with_format(errors))
            
            return redirect('home:patients')

@login_required            
def patient_list(request):
    context = {
        # 'object_list': len(Patient.objects.all()) != 0,
        'list_length': len(Patient.objects.all()),
        'segment': 'patient_list',
        'js_variables': {'root_url': root_url}
    }
    return render(request, 'home/patient_list.html', context)

def search_pdf(request):
    if request.method == 'GET':
        return render(request, 'home/pdf/pdf_search.html', {})
    if request.method == 'POST':
        return HttpResponse('Something went wrong.')

# APIs
def create_diagnosis(request):
    if request.method == 'POST':
        diagnosis_form = DiagnosisForm(json.loads(request.body.decode('utf-8')))
        if diagnosis_form.is_valid():
            diagnosis = diagnosis_form.save()
            return JsonResponse({
                'id': diagnosis.id,
                'code': diagnosis.diagnosis_code,
                'description': diagnosis.diagnosis_description
            })
        else:
            return JsonResponse(diagnosis_form.errors.as_json(), safe=False)
        
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
 
def create_attached_file(request):
    if request.method == 'POST':
        attached_file_form = AttachedFileForm(request.POST, request.FILES)
        if attached_file_form.is_valid():
            attached_file = attached_file_form.save()
            return JsonResponse({
                'id': attached_file.id,
                'name': attached_file.name,
                'file': str(attached_file.file),
                'created_at': localtime(attached_file.created_at).date(),
                'patient': attached_file.patient.cedula
            })
        else:
            return JsonResponse({'error': attached_file_form.errors.as_json()})
       
def get_patient_list(request):
    data = [
        {
            'cedula': patient.cedula,
            'nombre': patient.nombre,
            'apellidos': patient.apellidos,
            'telefono': patient.telefono,
            'updated_at': localtime(patient.updated_at).strftime('%I:%M %p - %d/%m/%Y')
        }
    for patient in list(Patient.objects.all().order_by('-updated_at'))]
    return JsonResponse(data, safe=False)   

@login_required
def delete_patient(request, id):
    patient =  Patient.objects.get(pk=id)
    patient.delete()
    # messages.success(request, 'Se eliminó el paciente.')
    return HttpResponse('Paciente eliminado')

def get_diagnosis_list(request):
    return JsonResponse(
        [{
            'id': diagnosis.id,
            'code': diagnosis.diagnosis_code,
            'description': diagnosis.diagnosis_description
        } for diagnosis in Diagnosis.objects.filter(is_active=True)],
        safe=False
    )

def get_test_list(request):
    return JsonResponse(
        [{
            'id': test.id,
            'name': test.test_name,
            'description': test.test_description,
            'category': test.category.category_name,
            'subcategory': test.subcategory,
            'result_type': test.result_type
        } for test in Test.objects.all()],
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
        
        diagnosis = Diagnosis.objects.create(
            diagnosis_code=code, 
            diagnosis_description=description, 
            is_active=True
        )

        diagnosis.save()
        
    data = [
        {
            'code': diagnosis.diagnosis_code,
            'description': diagnosis.diagnosis_description
        }
    for diagnosis in list(Diagnosis.objects.all())]
    return JsonResponse(data, safe=False)
   
def test(request):
    return render(request, 'accounts/login2.html', {})  



from xhtml2pdf import pisa             # import python module

# Define your data
source_html = "<html><body><p>To PDF or not to PDF</p></body></html>"
output_filename = "test.pdf"

# Utility function
def convert_html_to_pdf(source_html, output_filename):
    # open output file for writing (truncated binary)
    result_file = open(output_filename, "w+b")

    # convert HTML to PDF
    pisa_status = pisa.CreatePDF(
        source_html,                # the HTML to convert
        dest=result_file)           # file handle to recieve result

    # close output file
    result_file.close()                 # close output file

    # return False on success and True on errors
    return pisa_status.err

# # Main program
# if __name__ == "__main__":
#     pisa.showLogging()
#     convert_html_to_pdf(source_html, output_filename)

from django.conf import settings
from django.template.loader import get_template
from django.contrib.staticfiles import finders

def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    result = finders.find(uri)
    if result:
        if not isinstance(result, (list, tuple)):
            result = [result]
        result = list(os.path.realpath(path) for path in result)
        path=result[0]
    else:
        sUrl = settings.STATIC_URL        # Typically /static/
        sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL         # Typically /media/
        mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception(
            'media URI must start with %s or %s' % (sUrl, mUrl)
        )
    return path

def render_pdf_view(request):
    if request.method == 'GET':
        return render(request, 'home/pdf/pdf_search.html', {})
    
    if request.method == 'POST':
        cedula = request.POST.get('patient_id')
        try:
            patient = Patient.objects.get(cedula=cedula)
            print('*'*20)
            print(dir(patient))
            # for attr in dir(patient):
            #     print(attr, ' / ', getattr(patient, attr))
            template_path = 'home/pdf/clinical_history.html'
            context = {'myvar': 'this is your template context', 'name': 'Mateo'}
            # Create a Django response object, and specify content_type as pdf
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            # find the template and render it.
            template = get_template(template_path)
            html = template.render(context)

            # create a pdf
            pisa_status = pisa.CreatePDF(
            html, dest=response, link_callback=link_callback)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse('Error al crear archivo PDF.')
            return response
        except:
            messages.warning(request, f'No encontramos un registro para {cedula}')
            return redirect('home:pdf')