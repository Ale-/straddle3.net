# django
from django import template
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
# project
from django.conf import settings

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

@register.inclusion_tag('field.html')
def field(obj=None, field_name=None, value_html_wrapper='div', label=False, label_html_wrapper='label', field_label=None, container='full'):
    try:
        model_name = obj.__class__.__name__.lower()
        field_value = getattr(obj, field_name)
    except:
        return Exception("You need to pass a valid object or field name to field_simple tag")
    if not field_label:
        field_label = obj._meta.get_field(field_name).verbose_name
    return {
        'model_name'         : model_name,
        'field_name'         : field_name,
        'label'              : label,
        'field_label'        : field_label,
        'field_value'        : field_value,
        'value_html_wrapper' : value_html_wrapper,
        'label_html_wrapper' : label_html_wrapper,
        'container_name'     : model_name + "-" + container,
    }

@register.inclusion_tag('fake-breadcrumb.html')
def fake_breadcrumb(text=_("Volver a la página anterior")):
    return { 'text' : text }
