from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from home.views import pages

application_paths = [
    path('admin/', admin.site.urls),
    path('', include('authentication.urls')),
    path('', include('home.urls')), 
]

media_paths = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

any_other_path = [
    # Matches any html file
    re_path(r'^.*\.*', pages, name='pages'),
]

urlpatterns = application_paths + media_paths + any_other_path

