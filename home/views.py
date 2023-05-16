from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template import loader
from django import template
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .forms import PatientForm, DiagnosticForm, EvolutionForm, TestForm, PatientTestForm
from .models import Paciente, Evolucion
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
        patient_form = PatientForm()
        diagnostic_form = DiagnosticForm()
        evolution_form = EvolutionForm()
        patient_test_form = PatientTestForm()
        context = {
            'segment': 'form', 
            'patient_form': patient_form, 
            'diagnostic_form': diagnostic_form,
            'evolution_form': evolution_form,
            'patient_test_form': patient_test_form,
            'evolution_records': None,
            'js_variables': {'diagnostic_form': diagnostic_form}
        }
        return render(request, 'home/form.html', context)
    if request.method == 'POST':
        patient_form = PatientForm(request.POST, request.FILES)
        if patient_form.is_valid():
            patient = patient_form.save()
            
            evolution_form = EvolutionForm({**request.POST.dict(), **{'paciente': patient}})
            if evolution_form.is_valid():
                evolution_form.save()
                return HttpResponse('Forms were saved.')
            else:
                return HttpResponse([
                    evolution_form.errors.as_json()
                ])
        else:
            return HttpResponse([
                patient_form.errors.as_json()
            ])
    
    
def update_patient(request, id):
    patient = Paciente.objects.get(pk=id)
    evolution_records = Evolucion.objects.filter(paciente__pk=id)
    if request.method == 'GET': 
        patient_form = PatientForm(instance=patient)
        evolution_form = EvolutionForm()
        context = {
            'segment': 'form',
            'patient_tests': '', 
            'form': patient_form, 
            'evolution_form': evolution_form,
            'evolution_records': evolution_records
        }
        return render(request, 'home/form.html', context)
    
    if request.method == 'POST':
        patient_form = PatientForm(request.POST, request.FILES, instance=patient)
        if patient_form.is_valid():
            patient = patient_form.save()
            evolution_form = EvolutionForm({**request.POST.dict(), **{'paciente': patient}})
            if evolution_form.is_valid():
                evolution_form.save()
                return HttpResponse('Forms were saved.')
            else:
                return HttpResponse([
                    evolution_form.errors.as_json()
                ])
        else:
            return HttpResponse([
                patient_form.errors.as_json()
            ])
            
def patient_list(request):
    context = {
        'object_list': Paciente.objects.all(),
        'segment': 'patient_list'
    }
    return render(request, 'home/patient_list.html', context)

def create_diagnostic(request):
    if request.method == 'POST':
        print(request.POST)
        print(request.body)
        print(json.loads(request.body.decode('utf-8')))
        diagnostic_form = DiagnosticForm(json.loads(request.body.decode('utf-8')))
        if diagnostic_form.is_valid():
            diagnostic = diagnostic_form.save()
            return JsonResponse({
                'id': diagnostic.id,
                'code': diagnostic.code,
                'description': diagnostic.description,
                'created_at': diagnostic.id,
            })
        else:
            return JsonResponse(diagnostic_form.errors.as_json(), safe=False)