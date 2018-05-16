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
    # API
    url(r'^api/map$', views.MapApi, name="map"),
]

urlpatterns += i18n_patterns(
    # Frontpage
    url(r'^$',  views.MapView.as_view(), name="front"),
    # CKEditor
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    # CKEditor
    url(r'^mapa$', views.MapView.as_view(), name="map"),
    # Project
    path('project/<slug:slug>', views.ProjectView.as_view(), name="project")

)

if settings.DEBUG == True:
   urlpatterns += static( settings.STATIC_URL, document_root = settings.STATIC_ROOT )
   urlpatterns += static( settings.MEDIA_URL,  document_root = settings.MEDIA_ROOT )
