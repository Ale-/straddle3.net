# python
import os
# django
from django import template
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.utils.text import slugify
# project
from django.conf import settings
from apps.models import models

register = template.Library()

@register.simple_tag
def css(file):
    return  settings.STATIC_URL + settings.PROJECT_STATIC_FOLDER + '/css/' + file

@register.simple_tag
def js(file):
    return  settings.STATIC_URL + settings.PROJECT_STATIC_FOLDER + '/js/' + file

@register.simple_tag
def img(file):
    return  settings.STATIC_URL + settings.PROJECT_STATIC_FOLDER + '/img/' + file

@register.simple_tag
def field_verbose_name(obj, field_name):
    return obj._meta.get_field(field_name).verbose_name

@register.simple_tag()
def simple_field(obj, field_name, lang, safe=False):
    field = getattr(obj, field_name)
    if lang != settings.LANGUAGE_CODE:
        translation = getattr(obj, "%s_%s"%(field_name, lang))
        field = translation if translation else field
    return mark_safe(field) if safe else field

@register.simple_tag()
def trans_cat_slug(cat, lang):
    name = cat.t('name', lang)
    return slugify(name)

@register.inclusion_tag('field.html')
def field(obj=None, lang=settings.LANGUAGE_CODE, safe=False, field_name=None, value_html_wrapper='div', label=False, label_html_wrapper='label', field_label=None, container='full', icon=None):
    source = getattr(obj, field_name)
    model_name = obj.__class__.__name__.lower()
    field_value = simple_field(obj, field_name, lang, safe)
    if not field_label:
        field_label = obj._meta.get_field(field_name).verbose_name
    return {
        'model_name'         : model_name,
        'obj'                : obj,
        'field_name'         : field_name,
        'label'              : label,
        'field_label'        : field_label,
        'field_value'        : field_value,
        'value_html_wrapper' : value_html_wrapper,
        'label_html_wrapper' : label_html_wrapper,
        'container_name'     : model_name,
        'icon'               : icon,
    }

@register.inclusion_tag('fake-breadcrumb.html')
def fake_breadcrumb(text=_("Volver a la página anterior")):
    return { 'text' : text }

@register.filter
def verbose_name(obj):
    return obj._meta.verbose_name

@register.filter(name='remove_i18n_prefix')
def remove_i18n_prefix(value):
    if value.startswith('/en') or value.startswith('/es'):
        value = value[3::]
    return value

@register.simple_tag
def videoembed(src, w, h):
    uri           = src.split('://')[1]
    service       = uri.split('/')[0]
    common_attrs  = "frameborder='0' webkitallowfullscreen mozallowfullscreen allowfullscreen"
    resource      = ""
    if service == 'vimeo.com' or service == 'youtu.be':
        resource = "https://player.vimeo.com/video/%s" % uri.split('/')[1]
    elif service == 'www.youtube.com':
        if '?v=' in uri:
            resource = uri.split('?v=')[1]
        elif '&v=' in uri:
            resource = uri.split('&v=')[1]
        resource = "https://www.youtube.com/embed/%s" % resource
    elif service == 'youtu.be':
        resource = "https://www.youtube.com/embed/%s" % uri.split('/')[1]
    elif service == 'www.ccma.cat':
        resource = uri.split('/video/')[1]
        resource = "http://www.ccma.cat/video/embed/%s" % resource
    if resource is not "":
        print(resource)
        return mark_safe("<iframe src='%s' width='%s' height='%s' %s></iframe>" % ( resource, w, h, common_attrs ))
    return ''

@register.filter
def filesize(url):
    return os.path.getsize(settings.BASE_DIR + url)

@register.filter
def file_exists(path):
    return os.path.isfile("%s/%s" % ( settings.BASE_DIR, path))

@register.filter
def media_exists(path):
    return os.path.isfile("%s/%s" % ( settings.MEDIA_ROOT, path))

@register.filter
def mediafile(path):
    imagefile = open("%s/%s" % ( settings.MEDIA_ROOT, path), "rb")
    return imagefile

@register.inclusion_tag('text-block.html')
def text(label, staff=False, lang=settings.LANGUAGE_CODE):
    try:
        text = models.Block.objects.get(label=label)
    except:
        text = None
    return {
        'text'  : text,
        'staff' : staff,
        'lang'  : lang,
        'label' : label,
    }

@register.filter
def get_section(path):
    return path.split("/")[2]

@register.simple_tag
def t(obj, field, lang):
    return obj.t(field, lang)

@register.filter
def ends(text, suffix):
    print(text, suffix, text.endswith(suffix))
    return text.endswith(suffix)
