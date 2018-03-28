# django
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline, GenericTabularInline
from django.db.models import TextField, ImageField
from django.forms import Textarea
from django.urls import reverse
from django.utils.html import format_html
# contrib
from leaflet.admin import LeafletGeoAdmin
from imagekit import ImageSpec
from imagekit.admin import AdminThumbnail
from imagekit.processors import ResizeToFill
from imagekit.cachefiles import ImageCacheFile
from adminsortable.admin import NonSortableParentAdmin, SortableGenericStackedInline, SortableGenericTabularInline, SortableAdmin
# app
from . import models
from apps.utils import widgets


# Project admin

def publish(modeladmin, request, queryset):
    queryset.update(published=True)

publish.short_description = "Publica los elementos seleccionados"

def unpublish(modeladmin, request, queryset):
    queryset.update(published=False)

unpublish.short_description = "Despublica los elementos seleccionados"

def feature(modeladmin, request, queryset):
    queryset.update(featured=True)

feature.short_description = "Promociona los elementos seleccionados"

def unfeature(modeladmin, request, queryset):
    queryset.update(featured=False)

unfeature.short_description = "Retira la promoción de los elementos seleccionados"

# Thumbnail generator for admin views
# @see https://github.com/matthewwithanm/django-imagekit#user-content-admin

class AdminThumbnailSpec(ImageSpec):
    processors = [ResizeToFill(100, 100)]
    format = 'JPEG'
    options = {'quality': 90 }

def cached_admin_thumb(instance):
    try:
        image  = instance.images.first()
        cached = ImageCacheFile(AdminThumbnailSpec(image.image_file))
    except:
        cached  = ImageCacheFile(AdminThumbnailSpec(instance.image))

    cached.generate()
    return cached

class ImageInline(SortableGenericTabularInline):
    model  = models.Image
    extra  = 0
    fields = (
        ( 'image_file', 'alt_text' ),
    )

    formfield_overrides = {
        ImageField: {
            'widget': widgets.AdminImageWidget
        }
    }

class LinkInline(SortableGenericTabularInline):
    model = models.Link
    fields = (
        ( 'url', 'title' ),
    )
    extra = 0

class ProjectAdmin(NonSortableParentAdmin, LeafletGeoAdmin):
    model        = models.Project
    ordering     = ('name',)
    thumb        = AdminThumbnail(image_field=cached_admin_thumb)
    list_filter  = ('published', 'featured')
    list_display = ('thumb', 'linked_name', 'summary', 'start_date', 'published', 'featured')
    inlines      = [ ImageInline, LinkInline ]
    actions      = [publish, unpublish, unfeature, feature]
    fields       = (('name', 'published', 'featured'), ('category', 'start_date', 'end_date'), ('summary', 'body'), 'geolocation', ('promoter', 'author_text', 'gratitude_text'), 'tags')

    def linked_name(self, obj):
        url = reverse("admin:%s_%s_change" % (obj._meta.app_label, obj._meta.model_name), args=(obj.id,))
        return format_html("<a href='" + url + "'>" + obj.name + "</a>")

    linked_name.short_description = 'Nombre del proyecto'
    thumb.short_description       = 'Imagen'

admin.site.register(models.Project, ProjectAdmin)


class TeamMemberAdmin(admin.ModelAdmin):
    model        = models.TeamMember
    ordering     = ('name',)
    thumb        = AdminThumbnail(image_field=cached_admin_thumb)
    list_filter  = ('published', 'featured')
    list_display = ('thumb', 'linked_name', 'surname', 'published', 'featured')
    actions      = [publish, unpublish, unfeature, feature]
    fields       = (('name', 'surname'), 'summary', 'image', ('published', 'featured'))

    def linked_name(self, obj):
        url = reverse("admin:%s_%s_change" % (obj._meta.app_label, obj._meta.model_name), args=(obj.id,))
        return format_html("<a href='" + url + "'>" + obj.name + "</a>")

    linked_name.short_description = 'Nombre'
    thumb.short_description       = 'Imagen'

admin.site.register(models.TeamMember, TeamMemberAdmin)


class ConnectionAdmin(LeafletGeoAdmin):
    model        = models.Project
    ordering     = ('name',)
    thumb        = AdminThumbnail(image_field=cached_admin_thumb)
    list_display = ('thumb', 'name', 'start_date', 'published', 'featured')
    list_filter  = ('published', 'featured')
    inlines      = [ ImageInline, LinkInline ]
    actions      = [publish, unpublish, unfeature, feature]
    fields       = (('name', 'published', 'featured'), ('category', 'start_date', 'end_date'), 'description', 'agents', 'geolocation', 'tags')

admin.site.register(models.Connection, ConnectionAdmin)


class ResourceAdmin(admin.ModelAdmin):
    model        = models.Resource
    ordering     = ('name',)
    thumb        = AdminThumbnail(image_field=cached_admin_thumb)
    list_display = ('thumb', 'linked_name', 'published', 'featured')
    list_filter  = ('published', 'featured')
    fields       = (('name', 'category'), 'image', 'description', ('promoter', 'author_text', 'gratitude_text'), 'license', 'tags', ('published', 'featured'))
    actions      = [publish, unpublish, unfeature, feature]
    inlines      = [ ImageInline, LinkInline ]

    def linked_name(self, obj):
        url = reverse("admin:%s_%s_change" % (obj._meta.app_label, obj._meta.model_name), args=(obj.id,))
        return format_html("<a href='" + url + "'>" + obj.name + "</a>")

    linked_name.short_description = 'Nombre'
    thumb.short_description       = 'Imagen'

admin.site.register(models.Resource, ResourceAdmin)


admin.site.register(models.Tag)
admin.site.register(models.ProjectCategory)
admin.site.register(models.ConnectionCategory)
admin.site.register(models.ResourceCategory)
