# django
from django.utils.html import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.widgets import AdminFileWidget
from django.template.loader import render_to_string

class AdminImageWidget(AdminFileWidget):
    def render(self, name, value, attrs=None):
        parent_widget = super(AdminImageWidget, self).render(name, value, attrs)
        print(value.__class__)
        c = {
            'parent_widget': parent_widget,
            'url'          : value.url,
        } if value and 'url' in value else {
            'parent_widget': parent_widget,
            'url'          : None,
        }
        return render_to_string("admin-image-widget.html", c)
