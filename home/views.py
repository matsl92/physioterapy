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
    Test,
    Category
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
        } for test in Test.objects.all().order_by('category', 'subcategory', 'test_name')],
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
            print(patient.patientdiagnosis_set.all())
            print('*'*20)
            print(dir(patient))
            # for attr in dir(patient):
            #     print(attr, ' / ', getattr(patient, attr))
            template_path = 'home/pdf/clinical_history.html'
            context = {
                'myvar': 'this is your template context', 
                'name': 'Mateo',
                'patient': patient
            }
            # Create a Django response object, and specify content_type as pdf
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="historia_clinica.pdf"'
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
        
def populate_test_table(request):
    
    text = """HOMBRO: 
    Articulación glenohumeral:
    -	Inspección- palpación: (descripción de la prueba) campo de texto
    -	Movimiento activo-pasivo: (descripción de la prueba) campo de texto. 
    Movilidad:
    -	Signo de Ludington: ambos brazos hacia la nuca. +Limitación o compensaciones para lograr el movimiento  (descripción de la prueba) // campo de opción + o - 
    -	Prueba de Apley: Intentar tocarse el borde interescapular. +Dolor con limitación del movimiento. (descripción de la prueba) // Campo de opción + o -
    Arcos de movilidad articular:
    -	Abducción: 180° (descripción de la prueba) / campo de texto
    -	Aducción: 30° (descripción de la prueba) / campo de texto
    -	Flexión: 180° (descripción de la prueba) / campo de texto
    -	Extensión: 60° (descripción de la prueba) / campo de texto
    -	RE: 90° (descripción de la prueba) / campo de texto
    -	RI: 70° (descripción de la prueba) / campo de texto
    Bursitis:
    -	Signo de bursitis subacromial: palpar la zona subacromial latero ventral, realizar extensión el brazo. +dolor localizado. (descripción de la prueba) campo + o -
    -	Signo de Dawbarn: Abducción del brazo simultaneo a la palpación del espacio subacromial hasta 90°. +dolor durante la abducción. (descripción de la prueba) campo + o -
    -	Prueba de Abott-sauders: abducción de 120' y con RE, baja lentamente. Guía el mvto del brazo del paciente y con la otra mano palpa la corredera bicipital. +Crujido (descripción de la prueba) campo +o -
    Luxación acromioclavicular: 
    -	Signo de la tecla de piano: (descripción de la prueba) campo + o- 
    -	Signo de aprehensión: anterior: sedente, abd 90° con flexión de codo, RE simultaneo con empuje anterior de la cabeza humeral. +Miedo o resistencia a que se realice //posterior: sedente o supino, abd de 90° con flexión de codo, RE simultaneo con empuje posteroinferior de la cabeza humeral. +Miedo o resistencia a que se realice. (descripción de la prueba) campo + o -.
    Inestabilidad del hombro:
    -	Inestabilidad inferior del hombro: Desde sedente tracciona hacia inferior. +surco entre acromion y cabeza humeral. (descripción de la prueba) campo + o -
    -	Cajón anterior y posterior: Sedente, fija escapula y desliza la cabeza humeral hacia anterior o posterior, comparativo para determinar diferencia significativa. (descripción de la prueba) campo + o -
    Pinzamiento subacromial: 
    -	Arco doloroso del hombro: +pinzamiento cuando refiere dolor entre los 70°-120° (descripción de la prueba) campo + o -
    -	Test de neer (pinzamiento supraespinoso): sedente, fija escapula, eleva pasivo el brazo desde RI y pronación hacia flexión máxima. +El paciente indica o refleja dolor (descripción de la prueba) campo + o -
    -	Test de Hawkins pinzamiento supraespinoso y bíceps con ligamento coracoacromial): sedente, elevar el brazo a 90° de flexión de hombro y codo flexionado a 90°, se realiza RI. +Dolor o molestia al realizarle la RI. (descripción de la prueba) campo + o -
    Desgarros del labrum glenoideo: 
    -	Test de O´Brien: bípedo, flexión de hombro 90° con codo extendido, aducir horizontal 10°-15° con RI, fuerza hacia abajo desde el antebrazo, regresar el brazo a posición inicial y en supinación aplicar fuerza de nuevo. +Dolor o clic en el hombro con la primera fuerza, y disminuye o es nulo en la segunda.  (descripción de la prueba) campo + o -
    Patología muscular o tendinosa: 
    -	Test de Speed (tendinopatía del bíceps o luxación del tendón al paso por la corredera): sedente, con codo extendido intenta llevar el hombro a flexión con antebrazo en supinación, se resiste la flexión de hombro, se palpa la articulación del hombro. (descripción de la prueba) campo + o -
    -	Test de Yergason (lesión tendinosa de la porción larga del bíceps-incompetencia del ligamento humeral transverso): sedente, flexión de codo a 90°, indicar al paciente que lleve la mano a supinación y flexione el codo mientras resisto el movimiento. (descripción de la prueba) campo + o -
    -	Prueba de abott-saunders (lesión tendón del bíceps, signo de subluxación): abducción de 120' y con RE, baja lentamente. Guía el mvto del brazo del paciente y con la otra mano palpa la corredera bicipital. + dolor en la corredera bicipital o un crujido articular audible o palpable. (descripción de la prueba) campo + o -
    -	Prueba del ligamento transversal del humero: abd 90' y RI, codo en extensión. se realiza RE del brazo palpando la corredera bicipital. +Chasquido o dolor tendón del bíceps. (descripción de la prueba) campo + o -
    -	Test de Jobe (tendinopatía o desgarro del supraespinoso-compromiso nervio supraescapular): sedente, abd pasiva de 90° con RI, mantener la posición, observar si la mano cae. Si sostiene la mano se aplica fuerza hacia abajo, +deja bajar el brazo y manifiesta dolor o debilidad en la región del supraespinoso. (descripción de la prueba) campo + o -
    -	Test de Gerber (debilidad o ruptura del subescapular): bípedo, dorso de la mano sobre región lumbar, FT fija zona escapular contralateral y se le pide empuje desde la palma de la mano. +Molestia, dolor o debilidad al empujar. (descripción de la prueba) campo + o -
    -	Prueba del musculo infraespinoso: sedente, Los brazos del paciente deben estar relajados y en posición anatómica; la articulación del codo se encuentra flexionada 90'. Ft coloca la palma de sus manos sobre el dorso de las del paciente. Resistencia a la RE. +Aparición de dolor o debilidad durante la RE. (descripción de la prueba) campo + o –
    -	Prueba del musculo redondo: bípedo, Ft detrás del paciente. + El músculo redondo mayor produce una rotación interna del brazo. Si existe una contractura muscular, el brazo afectado se mantendrá en rotación interna y la palma de las manos mirará hacia atrás. (descripción de la prueba) campo + o -
    Síndrome del opérculo torácico:
    -	Test de Wright: sedente tomar el pulso radial, llevar el hombro hacia abducción máxima con rotación externa +parestesia o se disminuye o desaparece el pulso. (descripción de la prueba) campo + o -
    -	Maniobra de Adson: sedente, tomar el pulso radial, rotación de la cabeza para el lado examinado.  FT (extensión, RE-HOMBRO) mientras el paciente lleva la cabeza a extensión, toma y mantiene una inspiración profunda. +Desaparece el pulso y aparece sintomatología. (descripción de la prueba) campo + o -
    -	Prueba de flexión horizontal de Thompson y Kopell: bípedo, desde abd 90' realiza flexión horizontal máxima. +dolor sobre el margen superior de la escápula con irradiación a la parte superior del brazo. (descripción de la prueba) campo + o -
    Articulación acromioclavicular:
    -	Arco doloroso: Abducción entre 140°-180° + Dolor (descripción de la prueba) campo + o -
    -	Prueba de aducción horizontal forzada: +Dolor en la articulación acromioclavicular. (descripción de la prueba) campo + o -
    -	Prueba de desplazamiento horizontal de la clavícula: sedente, movimiento en todas las direcciones. + Movilidad clavicular aumentada con dolor o sin él indica inestabilidad de la articulación acromioclavicular. (descripción de la prueba) campo + o -
    CODO:
    Rangos de movilidad articular: 
    -	Flexión: 150° (descripción de la prueba) / campo de texto
    -	Extensión: -5°-0° (descripción de la prueba) / campo de texto
    -	Pronación: 80° (descripción de la prueba) / campo de texto
    -	Supinación: 80° (descripción de la prueba) / campo de texto
    -	Prueba de hiperflexión: sedente, FT sujeta la muñeca+ flexión max de codo, observar limitación del mvto y localización del dolor. +Aumento o disminución de la movilidad articular y aparición del dolor. (descripción de la prueba) campo + o -
    -	Prueba de esfuerzo en supinación:  Sedente, FT toma con una mano antebrazo del paciente y con la otra sostiene el codo por la región medial, efectúa un movimiento brusco de supinación (se evalúa integridad de la articulación) +Dolor o limitación del movimiento (descripción de la prueba) campo + o -
    Pruebas de estabilidad:
    -	Bostezo lateral (estabilidad de ligamentos colaterales laterales): Sedente, brazo en extensión. FT estabiliza en región medial y con la otra realiza esfuerzo en varo. +Dolor (evalúa bilateral) (descripción de la prueba) campo + o -
    -	Bostezo medial (estabilidad de ligamentos colaterales mediales): Sedente brazo en extensión. FT estabiliza en región lateral y con la otra realiza esfuerzo en valgo. +Dolor o movilidad alterada contralateral. (descripción de la prueba) campo + o -
    -	Test de estrés en valgo: sedente, codo entre 70° y 90° con antebrazo supinado, con el pulgar debajo del antebrazo realizar estrés en valgo, llevándolo a extensión +Dolor región medial del codo. (descripción de la prueba) campo + o -
    Pruebas de epicondilitis:
    -	Prueba de la silla (epicondilitis lateral): con el brazo en extensión y antebrazo en pronación, se pide al paciente que levante una silla. +Aparición o aumento de dolor en epicóndilo lateral y en musculatura extensora del antebrazo. (descripción de la prueba) campo + o -
    -	Prueba de Thomson (epicondilitis lateral): extensión de muñeca con resistencia. (descripción de la prueba)
    -	Test de Cozen (test de hiperextensión contra resistencia): Sedente, estabiliza el codo, empuña la mano en pronación y se resiste la extensión de muñeca activa. +Dolor en epicóndilo lateral. (descripción de la prueba) campo + o -
    -	Test de Mill: Sedente, Ft palpa el epicóndilo y lleva pasivamente el antebrazo a pronación con flexión de muñeca máxima, luego extiende el codo. +Dolor epicóndilo o compresión del nervio radial. (descripción de la prueba) campo + o -
    -	Test de Maudsley: Sedente, Ft resiste la extensión activa del tercer dedo +Dolor epicóndilo lateral. (descripción de la prueba) campo + o -
    -	Test de Cozen invertida (epicondilitis medial): Sedente, estabiliza el codo, empuña en supinación, y el FT resiste la flexión de codo +Dolor en epicóndilo medial. (descripción de la prueba) campo + o -
    MUÑECA:
    -	Evaluación fibrocartílago triangular: codo a 90° con antebrazo supinado, FT coloca las manos sobre las del paciente y se le pide que intente elevarlas contra resistencia +Dolor sobre la zona. (descripción de la prueba) campo + o –
    -	Test de finkelstein (tenosinovitis de Quervain)
    -	Test de phalen (síndrome túnel del carpo): juntar las manos por el dorso de ellas llevándolas a hiperflexión con descenso de los codos (mantener 30s a un minuto) +Sintomatología en el recorrido del nervio medial. (descripción de la prueba) campo + o -
    -	Test de phalen invertido (Túnel del carpo): juntar las palmas de las manos llevando las muñecas a hiperextensión acompañada de elevación de los codos (mantener 30s a un minuto). (descripción de la prueba) campo + o -
    -	Signo de tinel (túnel del carpo): mano en supinación con apoyo se golpea con el martillo o se hace presión sobre el túnel +Dolor y parestesia en el recorrido del mediano. (descripción de la prueba) campo + o -
    -	Test de froment: pedirle al paciente que sujete una tarjeta con el índice y el pulgar, indicarle que no la deje retirar. evaluar bilateralmente +Flexión de la interfalángica del pulgar/parálisis del nervio cubital. (descripción de la prueba) campo + o -
    -	Test de ochsner (lesión del nervio mediano): pedir al paciente que entrelace las manos +incapacidad para flexionar los dedos 2-3. (descripción de la prueba) campo + o -
    -	Prueba de la O: realice oposición con el índice y pulgar dejando los otros tres dedos en extensión y abducción. Evalúa los tres nervios de la mano 1. Extensión de muñeca y dedos (N radial) 2. Abducción de los dedos (N cubital) 3. Pinza (N mediano). (descripción de la prueba) campo + o -
    COLUMNA:
    Pruebas torácicas: 
    -	Dedo-piso: Rodillas en extensión, flexión de columna hacia dedos de los pies, observar recorrido del movimiento. (descripción de la prueba) campo + o -
    -	Signo de OTT: El paciente se encuentra en bipedestación. Es necesario marcar la apófisis espinosa de la vértebra C7 y un punto situado 30 cm más abajo. En flexión la distancia aumenta 2-4 cm. (descripción de la prueba) campo + o -
    -	Signo de schober: Bípedo. marca sobre apófisis espinosa de la vértebra S1 y 10 cm más arriba. Pte realiza flexión de tronco. La distancia entre las dos marcas cutáneas se amplía hasta 15 cm; y en extensión se acorta hasta 8 y 9 cm. (descripción de la prueba) campo + o -
    -	Prueba del pliegue cutáneo de kibler: Decúbito prono con brazos paralelos al tronco. Tomar un pliegue cutáneo que se desplaza desde la lumbar a la zona escapular. (descripción de la prueba) campo + o -
    Pruebas columna cervical:
    -	Palpación: campo de texto
    -	Trígono suboccipital: campo de texto 
    -	Músculos palpables: por posterior (descripción de la prueba) campo de texto
    -	Por anterior: (descripción de la prueba) campo de texto 
    -	Test de Decklein: Integridad de la arteria vertebral. Rotación con extensión de columna cervical, 20 segundos. Comparación bilateral. + movimientos oculares, reflejos vágales. (descripción de la prueba) campo + o -
    -	Test del enchufe: (Estabilidad lig. Cruciforme) sedente, flexión de cuello, fijación de la cabeza con la mano contraria y contra el pecho del ft, presión sobre C1 (Atlas). + normal sensación de juego articular. **Lig. Fijo: sin mvto. **Lig. Laxo o lesionado: mvto, sensación inestable. (descripción de la prueba) campo + o -
    -	Sharp purser test: (Estabilidad lig. Cruciforme) sedente, flexión pasiva de cuello, fijación de la cabeza con mano contraria, presión sobre C2 (Axis). +disminución de la sintomatología. (descripción de la prueba) campo + o -
    -	Test de ligamentos alares: Mano del ft en U, flexión de cuello pasiva, con la otra mano realiza inclinación suboccipital. +normal Juego articular. (descripción de la prueba) campo + o -
    Movilidad: 
    -	Prueba de rotación cervical: Supino, ft fija desde el cráneo, realiza flexión y rotación cervical. +Limitación del movimiento por posteriorización de c1 sobre c2. (descripción de la prueba) campo + o -
    -	Prueba de rotación cervical: Sedente, flexión pasiva de cuello, realizar rotación hacia la derecha y luego hacia la izquierda. *La limitación con presencia de dolor = disfunción segmentaria. (descripción de la prueba) campo + o -
    Radiculopatía cervical:
    -	Test de spurling Sedente: columna recta, inclinación pasiva de la cabeza hacia lado no afectado y aplicar compresión, luego inclinar al lado con sintomatología y aplicar compresión. +Dolor o sintomatología con irradiación del lado comprometido. (descripción de la prueba) campo + o -
    -	Test de distracción cervical: sedente, pte relajado, mano debajo de la mandíbula y la otra abajo del occipital, realizar ligera tracción ascendente. +Alivio o disminución de síntomas radiculares. (descripción de la prueba) campo + o -
    Test de fuerza:
    -	musculatura suboccipital: (músculos profundos del cuello) en patrón disfuncional. Se pide al paciente flexión suboccipital, flexión cervical, sostener. +fasciculaciones. (descripción de la prueba) campo + o -
    -	Test de guillet: Bípedo, manos apoyadas en la a pared, palpar cresta iliaca y surco sacro, pedir flexión de cadera, observar el movimiento del iliaco ipsilateral y sacro contralateral (+Si hay dolor o no desciende la EIPS contralateral). (descripción de la prueba) campo + o -
    -	Test de gaemslen (Disfunción sacroilíaca): Decúbito supino en camilla, flexión de cadera y la otra se extiende al máximo por fuera de la camilla con leve abducción +Si hay dolor en la región posterior. (descripción de la prueba) campo + o -
    -	Test de faber: Decúbito supino en camilla, fijar cadera contralateral. La pierna a evaluare se lleva desde flexión, abducción y rotación externa hacia extensión. +Para osteoartritis (dolor de cadera ipsilateral) +Para disfunción sacroilíaca (dolor contralateral o posterior a nivel del sacro). (descripción de la prueba) campo + o -
    -	Test de yeoman: Pte en prono, una mano fija en el reborde glúteo y se hace extensión de cadera pasiva. +Dolor en la ASI (ligamentos) +Dolor lumbar (compromiso lumbar) Si hay parestesias en la cara anterior del cuádriceps se está realizando estiramiento del nervio femoral. (descripción de la prueba) campo + o -
    -	Test de excursión del movimiento: decúbito prono, fijar pisiforme sobre un surco del sacro y poner la otra mano encima y aplicar presión inferior (se realiza en ambos surcos). +Dolor y sensación de muelle. (descripción de la prueba) campo + o -
    -	Test de compresión lateral: decúbito lateral. Se aplica presión en dirección al suelo desde el ilion +Dolor en el sacro o en las nalgas. (descripción de la prueba) campo + o -
    -	Compresión femoral: decúbito supino, flexionar la cadera del lado afectado en 90° con flexión de rodilla. Ft con una mano sobre el sacro y con la otra sostiene la rodilla afectada, aduce levemente la cadera y ejerce fuerza hacia inferior. +Dolor en el lado ipsilateral a la rodilla flexionada. (descripción de la prueba) campo + o -
    -	Test de distracción pélvica: Decúbito supino. El ft ejerce presión en ambas EIAS en dirección dorsolateral +Si produce dolor. (descripción de la prueba) campo + o -
    -	**Diagnostico diferencial (dolor sacroilíaco y lumbar): Flexión de tronco, si hay dolor se realizar la prueba con bloqueo de la articulación sacroilíaca (+Sacroilíaco: si con la art bloqueada el dolor mejora) (+Lumbar: Si con la art bloqueada el dolor empeora). (descripción de la prueba) campo + o -
    -	Long sitting test (rotación anterior o posterior del ilion): decúbito supino, alinear pies desde maléolos internos y se observa pierna acortada. Se le pide a la persona que se siente (Rotación posterior del ilion: la pierna corta se alarga) (rotación anterior del ilion: la pierna larga se hace más larga). (descripción de la prueba) campo + o -
    Articulación coxofemoral:
    -	Medida real y aparente: Real (EIAS y maléolo interno) aparente (ombligo, maléolo interno). (descripción de la prueba) Cuadro de texto
    -	Test del piriforme (síndrome del piramidal): decúbito lateral con lado a evaluar supra lateral al borde de la camilla o decúbito supino, flexión de rodilla a 90°, descender la rodilla en dirección del piso o en dirección al muslo, la otra mano fija la cadera (+dolor en región glútea con irradiación ciática). (descripción de la prueba) campo + o -
    -	Signo de Trendelenburg: bípedo, realizar apoyo con una pierna y luego con la otra. Observar el movimiento de la pelvis, si la pelvis libre subo el signo es – (+Pelvis del pie sin apoyo cae, indica debilidad de glúteo medio). (descripción de la prueba) campo + o -
    ARTICULACIÓN DE LA RODILLA: 
    -	Bostezo medial y lateral (lesión de ligamento colateral medial o lateral): supino o sedente, flexión de rodilla entre 30° y 60°. estabilizando en rodilla y con la otra mano se aplica tensión en valgo o varo (+Movimiento significativo y dolor en cara medial o lateral) Grados de bostezo: Leve (<5mm), moderado (5 a 10mm), severo (>10mm). (descripción de la prueba) campo + o – y cuadro de texto
    -	Test de Lachman (Lesión LCA): supino, rodilla en flexión de 10° a 30°, una mano en porción distal del fémur, la otra en la proximal de la tibia. La mano superior fija haciendo fuerza hacia craneal, la inferior tracciona hacia anterior la tibia (+Movimiento anterior de la tibia *Puede acompañarse de dolor). (descripción de la prueba) campo + o -
    -	Cajón anterior y posterior (Lesión LCA, LCP): supino, flexión de rodilla a 90°. Ft fija en la parte distal del pie con su cuerpo, las dos manos sujetan la parte proximal de la tibia, empujar hacia atrás, luego tracción hacia adelante (+Desplazamiento anterior o posterior *Se puede acompañar de dolor). (descripción de la prueba) campo + o -
    -	Test de Apley (Lesión de ligamentos o capsula articular/Lesión meniscal): prono con rodilla en flexión de 90°, fijar el fémur distal con una mano, la otra mano a nivel distal de la pierna realiza tracción con movimientos rotacionales. (+distracción, dolor o aumento del mvto) (+Luego realizar el mismo procedimiento aplicando compresión/Dolor y bloqueo o crepitacionesLesión meniscal). (descripción de la prueba) campo + o -
    -	Test de McMurray (Lesión de menisco medial o lateral): decúbito supino, llevar pierna a completa flexión, una mano fija y palpa a nivel de la línea interarticular de la rodilla, la otra distal en el talón, aplica rotación tibial externa y lleva extensión la rodilla con estrés en varo (+Dolor, crepito audible o palpable Menisco medial), realizar el mismo procedimiento pero ahora la mano distal genera rotación tibial interna y lleva a extensión la rodilla con estrés en valgo (+Dolor, crepito Menisco lateral). (descripción de la prueba) campo + o -
    -	Test de Thessaly: Bípedo, apoyado en un pie. Ft da soporte, paciente rota su rodilla y cuerpo interna y externamente 3 veces, manteniendo la rodilla a 5 y a 20° de flexión (+Dolor, molestia en línea interarticular, crépitos o bloqueo). (descripción de la prueba) campo + o -
    -	Signo de ficat (desgaste del cartílago patela): decúbito supino, semiflexión de 10° de rodilla, movilizar la rótula contra la superficie articular del fémur (+crepito o dolor al realizar la movilización). (descripción de la prueba) campo + o -
    -	Aprehensión de rótula: Llevar hacia lateral la rótula (pierna extendida y relajada) (+Miedo o temor del paciente a que se luxe la rótula). (descripción de la prueba) campo + o -
    -	Test de Thompson (ruptura del tendón de Aquiles): decúbito prono con tobillos por fuera de la camilla, el Ft aprieta los gemelos (+No hay plantiflexión). (descripción de la prueba) campo + o -"""

    categories = []
    category = []
    subcategory = []
    exceptions = []
    category_name = ''
    subcategory_name = 'Ninguna'
    structured_data = {'categories': categories}

    text_lines = text.splitlines()
    [text_lines.remove(line) for line in text_lines if len(line) == 0]

    for line in text_lines:
        if line.isupper():
            if text_lines.index(line) > 0:
                category.append({subcategory_name: subcategory})
                categories.append({category_name: category})
                subcategory =[]
                category = []
                subcategory_name = 'Ninguna'
            category_name = line.strip().strip(':')
                
        else:
            if [*line.strip()][-1] == ':':
                if len(subcategory) > 0:
                    category.append({subcategory_name: subcategory})
                    subcategory = []
                subcategory_name = line.strip().strip(':')
            else:
                try:
                    test_name, tail = line.split(':', 1)
                    test_description, test_result_type = tail.split('(descripción de la prueba)')
                    subcategory.append([test_name, test_description, test_result_type])
                except Exception as e:
                    exceptions.append((e, line))
        if text_lines.index(line) == len(text_lines) - 1:
            category.append({subcategory_name: subcategory})
            categories.append({category_name: category})
                         
    for category in structured_data['categories']:
        for category_name, subcategories in category.items():
            name = category_name.strip()
            new_category = Category.objects.create(category_name=name)
            new_category.save()
            
            for subcategory in subcategories:
                for sub_name, tests in subcategory.items():
                    subcategory_name = sub_name.strip()
                    for test in tests:
                        if 'text' in test[2].strip().lower() or test[2].strip().lower() == '':
                            result_type = 'text'
                        else:
                            result_type = 'bool'
                            
                        new_test = Test.objects.create(
                            test_name = test[0].strip('-').strip().strip('-'),
                            test_description = test[1].strip().capitalize(),
                            category = new_category,
                            subcategory = subcategory_name,
                            result_type = result_type
                        )
                        new_test.save()
                        print(new_test)
    
    return JsonResponse(structured_data)
