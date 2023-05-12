from django.urls import path, re_path
from . import views

app_name = 'home'
urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    
    # Test page
    path('example', views.example, name='example'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]