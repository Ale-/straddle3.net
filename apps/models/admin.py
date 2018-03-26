# django
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline, GenericTabularInline
from django.db.models import TextField
from django.forms import Textarea
# contrib
from leaflet.admin import LeafletGeoAdmin
# app
from . import models

class ImageInline(GenericTabularInline):
    model = models.Image
    extra = 1
    fields = (
        ( 'image_file', 'alt_text' ),
    )

class LinkInline(GenericTabularInline):
    model = models.Link
    fields = (
        ( 'url', 'title' ),
    )
    extra = 1

class ProjectAdmin(LeafletGeoAdmin):
    model    = models.Project
    ordering = ('start_date',)
    list_display  = ('name', 'start_date', 'end_date')
    inlines      = [ LinkInline, ImageInline ]

admin.site.register(models.Project, ProjectAdmin)

admin.site.register(models.TeamMember)
