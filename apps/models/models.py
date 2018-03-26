# django #
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify
# contrib
from ckeditor_uploader.fields import RichTextUploadingField
from djgeojson.fields import PointField
# project
from .categories import FORMATS

""" Generic models """

class Image(models.Model):
    """ Images """

    image_file     = models.ImageField(_('Archivo de imagen'), blank=False)
    alt_text       = models.CharField(_('Alternative text'), max_length=200, blank=True)
    content_type   = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id      = models.PositiveIntegerField()
    source_content = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        """String representation of this model objects."""

        return self.image_file.name

class Attachment(models.Model):
    """ Attachments """

    attachment_file = models.ImageField(_('Attachment file'), blank=False)
    content_type    = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id       = models.PositiveIntegerField()
    source_content  = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        """String representation of this model objects."""

        return self.attachment_file.filename


class Link(models.Model):
    """ Attachment """

    url            = models.URLField(_('URL of the link'), blank=False)
    title          = models.CharField(_('Title of the link'), max_length=200, blank=True)
    content_type   = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id      = models.PositiveIntegerField()
    source_content = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        """String representation of this model objects."""

        return self.url

class Project(models.Model):
    """ Projects """

    name           = models.CharField(_('Nombre del proyecto'), max_length=200, blank=False, null=True)
    slug           = models.SlugField(editable=False, blank=True)
    start_date     = models.DateField(_('Fecha de comienzo'), blank=True, null=True)
    end_date       = models.DateField(_('Fecha de finalización'), blank=True, null=True)
    geolocation    = PointField(_('Geolocalización'), blank=True)
    project_format = models.CharField(_('Formato'), max_length=2, choices=FORMATS)
    promoter       = models.TextField(_('Promotor'), blank=True, null=True)
    author_text    = models.TextField(_('Autor'), blank=True, null=True)
    gratitude_text = models.TextField(_('Texto de agradecimientos'), blank=True, null=True)
    main_image     = models.ImageField(_('Imagen principal'), blank=True)
    summary        = models.TextField(_('Resumen'), blank=True, null=True)
    body           = RichTextUploadingField(_('Texto'), blank=True, null=True)

    def __str__(self):
        """String representation of this model objects."""

        return self.name

    def save(self, *args, **kwargs):
        """Populate automatically 'slug' field"""
        if not self.slug:
            self.slug = slugify(self.name)

        super(Project, self).save(*args, **kwargs)


class TeamMember(models.Model):

    name    = models.CharField(_('Nombre'), max_length=200, blank=False, null=True)
    surname = models.CharField(_('Apellidos'), max_length=200, blank=True, null=True)
    summary = models.TextField(_('Resumen'), blank=True, null=True)
    image   = models.ImageField(_('Imagen principal'), blank=True)

    def fullname(self):
        """Returns fullname of the person"""

        return "%s %s" % self.name, self.surname

    def __str__(self):
        """String representation of this model objects."""

        return self.fullname

    def save(self, *args, **kwargs):
        """Populate automatically 'slug' field"""
        if not self.slug:
            self.slug = slugify(self.fullname)

        super(TeamMember, self).save(*args, **kwargs)
