# python
import os
from itertools import chain
# django
from django.utils.deconstruct import deconstructible
from django.utils.text import slugify


def get_related(obj):
    """ Gets related objects from a given object. """

    projects    = obj.related_projects.filter(published=True)
    resources   = obj.related_resources.filter(published=True)
    connections = obj.related_connections.filter(published=True)
    related     = list(chain(projects, resources, connections))

    return related

@deconstructible
class RenameImage(object):
    """ An util object to rename images paths when uploading
        It's encapsulated in an object and uses @deconstructible
        to avoid migration problem because of the serialization
        of the object.
        @see https://stackoverflow.com/questions/25767787/django-cannot-create-migrations-for-imagefield-with-dynamic-upload-to-value#25768034 """

    def __init__(self, path):
        self.path = path

    def __call__(self, instance, filename):
        """ This method has to include instance and filename as parameters
            to be used by django to rename path.
            @see https://docs.djangoproject.com/en/1.11/ref/models/fields/#django.db.models.FileField.upload_to """

        type_path    = slugify(instance.content_type.name)
        slug         = getattr(instance.source_content, 'slug', None)
        content_path = slug if slug else slugify(instance.source_content.name)
        filename = slugify(instance.caption) + "." + filename.split('.')[1]

        # return the whole path to the file
        return os.path.join(self.path, type_path, content_path, filename)

@deconstructible
class RenameFile(object):
    """ An util object to rename files paths when uploading
        It's encapsulated in an object and uses @deconstructible
        to avoid migration problem because of the serialization
        of the object.
        @see https://stackoverflow.com/questions/25767787/django-cannot-create-migrations-for-imagefield-with-dynamic-upload-to-value#25768034 """

    def __init__(self, path):
        self.path = path

    def __call__(self, instance, filename):
        """ This method has to include instance and filename as parameters
            to be used by django to rename path.
            @see https://docs.djangoproject.com/en/1.11/ref/models/fields/#django.db.models.FileField.upload_to """

        type_path    = slugify(instance.content_type.name)
        content_path = instance.source_content.slug
        filename = slugify(instance.name) + "." + filename.split('.')[1]

        # return the whole path to the file
        return os.path.join(self.path, type_path, content_path, filename)
