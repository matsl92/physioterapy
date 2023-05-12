from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template import loader
from django import template
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import PatientForm

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

def form_view(request):
    form = PatientForm()
    context = {'segment': 'form', 'form': form}
    return render(request, 'home/form.html', context)