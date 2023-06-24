from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, SignUpForm
from django.contrib import messages
from xhtml2pdf import pisa
from django.conf import settings
from django.template.loader import get_template
from django.contrib.staticfiles import finders
import os
from django.http import HttpResponse
from home.models import Patient

# Define your data
source_html = "<html><body><p>To PDF or not to PDF</p></body></html>"
output_filename = "historia_clinica.pdf"

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

def index(request):
    if request.method == 'GET':
        login_form = LoginForm(prefix='login')
    if request.method == 'POST':
        
        if request.POST.get('patient_id') != '' and request.POST.get('patient_id') != None:
            
            cedula = request.POST.get('patient_id')
            try:
                patient = Patient.objects.get(cedula=cedula)
                template_path = 'home/pdf/clinical_history.html'
                context = {
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
                return redirect('authentication:index')
            
            
        
        login_form = LoginForm(request.POST, prefix='login')
        if login_form.is_valid():
            username = login_form.cleaned_data.get("username")
            password = login_form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home:patients")
            else:
                messages.warning(request, 'Credenciales inválidas')
                return redirect('authentication:index')
        else:
            messages.warning(request, 'Error al validat los datos')
            return redirect('authentication:index')

    return render(request, "accounts/index.html", {"form": login_form})

def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home:patients")
            else:
                msg = 'Credenciales inválidas'
        else:
            msg = 'Error al validar los datos'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})

def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = 'User created - please <a href="/login">login</a>.'
            success = True

            return redirect("/login/")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})

def logout_view(request):
    logout(request)
    return redirect('authentication:index')