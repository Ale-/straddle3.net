# django
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline, GenericTabularInline
from django.db.models import TextField, ImageField
from django.forms import Textarea, ModelForm
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

def generic_cached_admin_thumb(instance):
    image = instance.images.first()
    if image:
        cached = ImageCacheFile(AdminThumbnailSpec(image.image_file))
        cached.generate()
        return cached
    return None

def cached_admin_thumb(instance):
    cached = ImageCacheFile(AdminThumbnailSpec(instance.image))
    if cached:
        cached.generate()
        return cached
    return None

admin.site.register(models.Image)

class ImageInline(SortableGenericStackedInline):
    model  = models.Image
    extra  = 0
    fields = ('image_file', ('caption', 'not_caption', 'views_featured'), ('caption_en', 'caption_ca'))

    formfield_overrides = {
        ImageField: {
            'widget': widgets.AdminImageWidget
        }
    }
    classes = ['collapse']

class VideoInline(SortableGenericStackedInline):
    model  = models.Video
    extra  = 0
    fields = ( 'source_url', 'caption', ('caption_en', 'caption_ca'))
    classes = ['collapse']

class AttachmentInline(SortableGenericStackedInline):
    model  = models.Attachment
    extra  = 0
    fields = ('attachment_file', ('name', 'name_en', 'name_ca'), ('caption', 'caption_en', 'caption_ca'))
    classes = ['collapse']

class LinkInline(SortableGenericStackedInline):
    model = models.Link
    extra = 0
    fields = ( ('url', 'caption'), ('caption_en', 'caption_ca'))
    classes = ['collapse']

class ProjectAdmin(NonSortableParentAdmin, LeafletGeoAdmin):
    model             = models.Project
    ordering          = ('name',)
    thumb             = AdminThumbnail(image_field=generic_cached_admin_thumb)
    list_filter       = ('published', 'featured')
    list_display      = ('thumb', 'linked_name', 'summary', 'start_date', 'published', 'featured')
    actions           = [ publish, unpublish, unfeature, feature ]
    fieldsets = (
        (None, {
            'fields': (
                ('name', 'subtitle'),
                ('category', 'published', 'featured'),
                ('start_date', 'end_date'),
                ('summary', 'not_summary', 'body'),
                'geolocation',
                ('promoter', 'author_text', 'gratitude_text'),
                'tags', 'related_projects'
            ),
        }),
        ('Traducción al inglés', {
            'classes' : ('collapse',),
            'fields'  : (
                ('name_en', 'subtitle_en'),
                ('summary_en', 'body_en'),
                ('promoter_en', 'author_text_en', 'gratitude_text_en'),
            ),
        }),
        ('Traducción al catalán', {
            'classes' : ('collapse',),
            'fields'  : (
                ('name_ca', 'subtitle_ca'),
                ('summary_ca', 'body_ca'),
                ('promoter_ca', 'author_text_ca', 'gratitude_text_ca'),
            ),
        })
    )
    inlines           = [ ImageInline, LinkInline, AttachmentInline, VideoInline ]
    filter_horizontal = ('tags','related_projects')

    class Media:
        js = ['/static/straddle3/js/featured-image.js',]

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


class ConnectionAdmin(NonSortableParentAdmin, LeafletGeoAdmin):
    model             = models.Project
    ordering          = ('name',)
    thumb             = AdminThumbnail(image_field=generic_cached_admin_thumb)
    list_display      = ('thumb', 'linked_name', 'start_date', 'published', 'featured')
    list_filter       = ('published', 'featured')
    inlines           = [ ImageInline, LinkInline ]
    actions           = [ publish, unpublish, unfeature, feature ]

    fieldsets = (
        (None, {
            'fields': (
                ('name', 'subtitle'),
                'body', 'agents'
            ),
        }),
        ('Traducción al inglés', {
            'classes' : ('collapse',),
            'fields'  : (
                ('name_en', 'subtitle_en'),
                'body_en', 'agents_en'
            ),
        }),
        ('Traducción al catalán', {
            'classes' : ('collapse',),
            'fields'  : (
                ('name_ca', 'subtitle_ca'),
                'body_ca', 'agents_ca'
            ),
        })
    )
    filter_horizontal = ('tags',)

    class Media:
        js = ['/static/straddle3/js/featured-image.js',]

    def linked_name(self, obj):
        url = reverse("admin:%s_%s_change" % (obj._meta.app_label, obj._meta.model_name), args=(obj.id,))
        return format_html("<a href='" + url + "'>" + obj.name + "</a>")

admin.site.register(models.Connection, ConnectionAdmin)

class ResourceAdmin(NonSortableParentAdmin):
    model             = models.Resource
    ordering          = ('name',)
    thumb             = AdminThumbnail(image_field=generic_cached_admin_thumb)
    list_display      = ('thumb', 'linked_name', 'published', 'featured')
    list_filter       = ('published', 'featured')
    fieldsets = (
        (None, {
            'fields': (
                ('name', 'subtitle'),
                'summary', 'body',
                ('promoter', 'author_text', 'gratitude_text'),
                'license',
            ),
        }),
        ('Traducción al inglés', {
            'classes' : ('collapse',),
            'fields'  : (
                ('name_en', 'subtitle_en'),
                'summary_en', 'body_en',
                ('promoter_en', 'author_text_en', 'gratitude_text_en'),
                'license_en',
            ),
        }),
        ('Traducción al catalán', {
            'classes' : ('collapse',),
            'fields'  : (
                ('name_ca', 'subtitle_ca'),
                'summary_ca', 'body_ca',
                ('promoter_ca', 'author_text_ca', 'gratitude_text_ca'),
                'license_ca',
            ),
        })
    )
    actions           = [publish, unpublish, unfeature, feature]
    inlines           = [ ImageInline, LinkInline, AttachmentInline, VideoInline ]
    filter_horizontal = ('tags',)

    class Media:
        js = ['/static/straddle3/js/featured-image.js',]

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

class BlockAdminForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(BlockAdminForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs = { 'readonly' : True, 'classes' : 'disabled' }

class BlockAdmin(NonSortableParentAdmin):

    form = BlockAdminForm
    inlines = [ ImageInline, AttachmentInline, VideoInline ]
    fieldsets = (
        (None, {
            'fields'  : ('label', 'name', 'body'),
        }),
        ('Traducción al inglés', {
            'classes' : ('collapse',),
            'fields'  : ('name_en', 'body_en'),
        }),
        ('Traducción al catalán', {
            'classes' : ('collapse',),
            'fields'  : ('name_ca', 'body_ca'),
        })
    )

admin.site.register(models.Block, BlockAdmin)

class PostAdmin(NonSortableParentAdmin, LeafletGeoAdmin):
    model             = models.Post
    ordering          = ('name',)
    thumb             = AdminThumbnail(image_field=generic_cached_admin_thumb)
    list_display      = ('thumb', 'linked_name', 'date', 'published', )
    list_filter       = ('published',)
    inlines           = [ ImageInline, LinkInline ]
    actions           = [publish, unpublish, unfeature, feature]
    filter_horizontal = ('tags',)

    fieldsets = (
        (None, {
            'fields': (('name', 'published', 'date'), 'summary', 'body', 'tags'),
        }),
        ('Traducción al inglés', {
            'classes' : ('collapse',),
            'fields'  : ('name_en', 'summary_en', 'body_en'),
        }),
        ('Traducción al catalán', {
            'classes' : ('collapse',),
            'fields'  : ('name_ca', 'summary_ca', 'body_ca'),
        })
    )

    class Media:
        js = ['/static/straddle3/js/featured-image.js',]

    def linked_name(self, obj):
        url = reverse("admin:%s_%s_change" % (obj._meta.app_label, obj._meta.model_name), args=(obj.id,))
        return format_html("<a href='" + url + "'>" + obj.name + "</a>")

admin.site.register(models.Post, PostAdmin)
