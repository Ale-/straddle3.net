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
    path('proyectos', views.ProjectList.as_view(), name="projects"),
    # Project
    path('proyectos/<slug:slug>', views.ProjectView.as_view(), name="project"),
    # Projects
    path('proyectos/category/<slug:category_slug>', views.ProjectList.as_view(), name="projects_cat"),
    # Connections
    path('complicidades', views.ConnectionList.as_view(), name="connections"),
    # Projects
    path('complicidades/cat/<slug:category_slug>', views.ConnectionList.as_view(), name="connections_cat"),
    # Connection
    path('complicidades/<slug:slug>', views.ConnectionView.as_view(), name="connection"),
    # Resource
    path('recursos', views.ResourceList.as_view(), name="resources"),
    # Connection
    path('recursos/<slug:slug>', views.ResourceView.as_view(), name="resource"),
    # Resource
    path('recursos/cat/<slug:category_slug>', views.ResourceList.as_view(), name="resources_cat"),
    # Tag
    path('tag/<slug:slug>', views.TagView.as_view(), name="tag"),
    # Who
    path('quienes-somos', TemplateView.as_view(template_name="pages/who.html"), name="who"),
    # Who
    path('quienes-somos/equipo', views.TeamList.as_view(), name="team"),
    # What
    path('que-hacemos', TemplateView.as_view(template_name="pages/what.html"), name="what"),
    # Archivo
    path('archivo/', TemplateView.as_view(template_name="pages/archive.html"), name="archive"),
    # Open Fridays
    path('archivo/open-fridays', TemplateView.as_view(template_name="pages/open-fridays.html"), name="open_fridays"),
    # Repositorio webs
    path('archivo/repositorio-webs', TemplateView.as_view(template_name="pages/repositorio-webs.html"), name="repository"),
    # Curriculum
    path('archivo/curriculum', TemplateView.as_view(template_name="pages/curriculum.html"), name="cv"),
    # Bibliografía
    path('archivo/bibliografía', TemplateView.as_view(template_name="pages/bibliography.html"), name="bibliography"),
    # Hemeroteca
    path('archivo/hemeroteca', TemplateView.as_view(template_name="pages/press.html"), name="press"),
    # Videos
    path('archivo/videos', views.Videos.as_view(), name="videos"),
    # Blog
    path('actualidad', TemplateView.as_view(template_name="pages/whatsup.html"), name="whatsup"),
    # Blog
    path('actualidad/blog', views.Blog.as_view(), name="blog"),
    # Blog post
    path('actualidad/blog/<slug:slug>', views.PostView.as_view(), name="post"),
    # Search
    path('buscador', views.SearchView.as_view(), name="search"),

)

if settings.DEBUG == True:
   urlpatterns += static( settings.STATIC_URL, document_root = settings.STATIC_ROOT )
   urlpatterns += static( settings.MEDIA_URL,  document_root = settings.MEDIA_ROOT )
