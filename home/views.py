from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template import loader
from django import template
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.shortcuts import redirect
from .forms import PatientForm, DiagnosticForm, EvolutionForm, TestForm, PatientTestForm
from .models import Patient, Evolution, PatientTest
import json

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
        msg = ""
        errors = []
        if patient_form.is_valid():
            patient = patient_form.save()
            msg += "Patient form was saved."
            
            evolution_form = EvolutionForm({
                **request.POST.dict(),
                **{'patient': patient}
            })
            if evolution_form.is_valid():
                evolution_form.save()
                
            else:
                msg += "Evolution form wasn't saved."
                errors.append({'evolution_form': evolution_form.errors.as_json()})
            
            patient_test_form = PatientTestForm({
                **request.POST.dict(),
                **{'patient': patient}
            })
            if patient_test_form.is_valid():
                patient_test_form.save()
                
            else:
                msg += "Patient test form wasn't saved."
                errors.append({'patient_test_form': patient_test_form.errors.as_json()})
                
            # return JsonResponse([msg, errors], safe=False)
            return redirect('home:patient_list')
        
        else:
            msg += "Patient form was't saved."
            # return JsonResponse([msg, patient_form.errors.as_json()], safe=False)
            return redirect('home:patient_list')
            
       
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
        msg = ""
        errors = []
        if patient_form.is_valid():
            patient = patient_form.save()
            msg += "Patient form was saved."
            
            evolution_form = EvolutionForm({
                **request.POST.dict(),
                **{'patient': patient}
            })
            if evolution_form.is_valid():
                evolution_form.save()
                
            else:
                msg += "Evolution form wasn't saved."
                errors.append({'evolution_form': evolution_form.errors.as_json()})
            
            patient_test_form = PatientTestForm({
                **request.POST.dict(),
                **{'patient': patient}
            })
            if patient_test_form.is_valid():
                patient_test_form.save()
                
            else:
                msg += "Patient test form wasn't saved."
                errors.append({'patient_test_form': patient_test_form.errors.as_json()})
                
            # return JsonResponse([msg, errors], safe=False)
            return redirect('home:patient_list')
        
        else:
            msg += "Patient form was't saved."
            # return JsonResponse([msg, patient_form.errors.as_json()], safe=False)
            return redirect('home:patient_list')
        
        
        # patient_form = PatientForm(request.POST, request.FILES, instance=patient)
        # if patient_form.is_valid():
        #     patient = patient_form.save()
        #     evolution_form = EvolutionForm({**request.POST.dict(), **{'paciente': patient}})
        #     if evolution_form.is_valid():
        #         evolution_form.save()
        #         return HttpResponse('Forms were saved.')
        #     else:
        #         return HttpResponse([
        #             evolution_form.errors.as_json()
        #         ])
        # else:
        #     return HttpResponse([
        #         patient_form.errors.as_json()
        #     ])
            
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
                'diagnostic_code': diagnostic.diagnostic_code,
                'diagnostic_description': diagnostic.diagnostic_description,
                'is_active': diagnostic.is_active,
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
        
