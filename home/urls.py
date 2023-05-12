from django.urls import path, re_path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.index, name='home'),
    path('formulario', views.form_view, name="form"),
    path('example', views.example, name='example'),
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]