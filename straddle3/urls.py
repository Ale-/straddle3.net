# django
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path
from django.conf.urls.i18n import i18n_patterns
from django.views.generic.base import TemplateView
from django.conf import settings
# apps
from apps.views import views

admin.site.site_header = settings.ADMIN_SITE_HEADER

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^i18n/',  include('django.conf.urls.i18n')),
    # API
    url(r'^api/map$', views.MapApi, name="map"),
]

urlpatterns += i18n_patterns(
    # Frontpage
    url(r'^$',  views.FrontView.as_view(), name="front"),
    # CKEditor
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    # Map
    url(r'^mapa$', views.MapView.as_view(), name="map"),
    # Projects
    path('projects', views.ProjectList.as_view(), name="projects"),
    # Projects
    path('projects/<slug:category_slug>', views.ProjectList.as_view(), name="projects"),
    # Project
    path('project/<slug:slug>', views.ProjectView.as_view(), name="project"),
    # Connections
    path('connections', views.ConnectionList.as_view(), name="connections"),
    # Projects
    path('connections/<slug:category_slug>', views.ConnectionList.as_view(), name="connections"),
    # Connection
    path('connection/<slug:slug>', views.ConnectionView.as_view(), name="connection"),
    # Resource
    path('resources', views.ResourceList.as_view(), name="resources"),
    # Resource
    path('resources/<slug:category_slug>', views.ResourceList.as_view(), name="resources"),
    # Connection
    path('resource/<slug:slug>', views.ResourceView.as_view(), name="resource"),
    # Tag
    path('tag/<slug:slug>', views.TagView.as_view(), name="tag"),
    # Who
    path('quienes-somos', views.TeamList.as_view(), name="who"),
    # What
    path('que-hacemos', TemplateView.as_view(template_name="pages/what.html"), name="what"),
    # Open Fridays
    path('archivo/open-fridays', TemplateView.as_view(template_name="pages/open-fridays.html"), name="open_fridays"),
    # Repositorio webs
    path('archivo/repositorio-webs', TemplateView.as_view(template_name="pages/repositorio-webs.html"), name="repository"),
    # Curriculum
    path('archivo/curriculum', TemplateView.as_view(template_name="pages/curriculum.html"), name="cv"),
    # Bibliografía
    path('archivo/bibliografía', TemplateView.as_view(template_name="pages/bibliografia.html"), name="bibliography"),

)

if settings.DEBUG == True:
   urlpatterns += static( settings.STATIC_URL, document_root = settings.STATIC_ROOT )
   urlpatterns += static( settings.MEDIA_URL,  document_root = settings.MEDIA_ROOT )
