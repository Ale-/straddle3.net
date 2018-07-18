# django
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify
from django.urls import reverse
# contrib
from ckeditor_uploader.fields import RichTextUploadingField
from djgeojson.fields import PointField
from adminsortable.models import SortableMixin
from colorfield.fields import ColorField
# project
from .categories import FORMATS
from . import validators, utils

validate_image_size = validators.ImageSizeValidator({ 'min_width' : 480, 'min_height' : 480, 'max_width' : 1920, 'max_height' : 1280 })
validate_image_type = validators.ImageTypeValidator(["jpeg", "png"])
validate_file_type  = validators.FileTypeValidator()
images_path         = utils.RenameImage("images/")
files_path          = utils.RenameFile("files/")

""" Generic models """

class Video(SortableMixin):
    """ Images """

    source_url     = models.CharField(_('Video'), max_length=200, blank=True, null=True,
                                       help_text=_('Inserta la url de un video de Youtube o Vimeo'))
    caption        = models.TextField(_('Caption opcional'), max_length=200, blank=False)
    content_type   = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id      = models.PositiveIntegerField()
    source_content = GenericForeignKey('content_type', 'object_id')
    order          = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        """String representation of this model objects."""

        return self.caption[:100] + "..."

class Image(SortableMixin):
    """ Images """

    image_file     = models.ImageField(_('Archivo de imagen'), blank=False,
                                       validators=[validate_image_size, validate_image_type],
                                       upload_to=images_path)
    alt_text       = models.CharField(_('Texto alternativo'), max_length=200, blank=False)
    content_type   = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id      = models.PositiveIntegerField()
    source_content = GenericForeignKey('content_type', 'object_id')
    order          = models.PositiveIntegerField(default=0, editable=False, db_index=True)
    not_caption    = models.BooleanField(_('No mostrar pie de foto'), default=False, help_text=_("Marca la casilla para no mostrar el pie de foto en las galerías"))
    views_featured = models.BooleanField(_('Destacada'), default=False, help_text=_("La imagen destacada será la que se muestre en las vistas"))

    class Meta:
        verbose_name = _('imagen')
        verbose_name_plural = _('imágenes')
        ordering = ['order']

    def __str__(self):
        """String representation of this model objects."""

        return self.image_file.name

class Attachment(SortableMixin):
    """ Attachments """

    name            = models.CharField(_('Nombre descriptivo del archivo'), max_length=200, blank=False, null=True)
    attachment_file = models.FileField(_('Archivo adjunto'), blank=False,
                                        validators=[validate_file_type],
                                        upload_to=files_path)
    content_type    = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id       = models.PositiveIntegerField()
    source_content  = GenericForeignKey('content_type', 'object_id')
    order          = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    class Meta:
        verbose_name = _('adjunto')
        verbose_name_plural = _('adjuntos')
        ordering = ['order']

    def __str__(self):
        """String representation of this model objects."""

        return self.attachment_file.name


class Link(SortableMixin):
    """ Attachment """

    url            = models.URLField(_('URL del enlace'), blank=False)
    title          = models.CharField(_('Título del enlace'), max_length=200, blank=True)
    content_type   = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id      = models.PositiveIntegerField()
    source_content = GenericForeignKey('content_type', 'object_id')
    order          = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    class Meta:
        verbose_name        = _('enlace')
        verbose_name_plural = _('enlaces')
        ordering            = ['order']

    def __str__(self):
        """String representation of this model objects."""

        return self.url

class Tag(models.Model):

    name        = models.CharField(_('Nombre de la etiqueta'), blank=False, max_length=128)
    description = models.TextField(_('Descripción opcional'), max_length=200, blank=True)
    slug        = models.SlugField(editable=False, blank=True)

    class Meta:
        verbose_name = _('tag')
        verbose_name_plural = _('tags')

    def __str__(self):
        """String representation of this model objects."""

        return self.name

    def save(self, *args, **kwargs):
        """Populate automatically 'slug' field"""
        if not self.slug:
            self.slug = slugify(self.name)

        super(Tag, self).save(*args, **kwargs)

class ProjectCategory(models.Model):

    name        = models.CharField(_('Nombre de la categoría'), max_length=128, blank=False)
    color       = ColorField(_('Color de la categoría'), blank=True)
    description = models.TextField(_('Descripción opcional'), max_length=200, blank=True)

    class Meta:
        verbose_name = _('tipo de proyecto')
        verbose_name_plural = _('tipos de proyecto')

    def __str__(self):
        """String representation of this model objects."""

        return self.name

class Project(models.Model):
    """ Projects """

    name           = models.CharField(_('Nombre del proyecto'), max_length=200, blank=False, null=True)
    summary        = models.TextField(_('Resumen'), blank=True, null=True)
    body           = RichTextUploadingField(_('Texto'), blank=True, null=True)
    slug           = models.SlugField(editable=False, blank=True)
    start_date     = models.DateField(_('Fecha de comienzo'), blank=True, null=True, help_text=_("Puedes usar el formato dd/mm/yyyy"))
    end_date       = models.DateField(_('Fecha de finalización'), blank=True, null=True, help_text=_("Puedes usar el formato dd/mm/yyyy"))
    geolocation    = PointField(_('Geolocalización'), blank=True)
    category       = models.ForeignKey(ProjectCategory, verbose_name=_('Formato'), blank=True, null=True, on_delete=models.SET_NULL)
    promoter       = models.TextField(_('Promotor'), blank=True, null=True)
    author_text    = models.TextField(_('Autor'), blank=True, null=True)
    gratitude_text = models.TextField(_('Texto de agradecimientos'), blank=True, null=True)
    images         = GenericRelation(Image)
    tags           = models.ManyToManyField(Tag, verbose_name=_('Tags'), blank=True)
    published      = models.BooleanField(_('Publicado'), default=False, help_text=_("Indica si este contenido es visible públicamente"))
    featured       = models.BooleanField(_('Destacado'), default=False, help_text=_("Indica si este contenido es destacado y ha de tener mayor visibilidad"))
    links          = GenericRelation(Link)
    videos         = GenericRelation(Video)
    not_summary    = models.BooleanField(_('No mostrar resumen'), default=False, help_text=_("Marca para no mostrar el resumen en las vistas completas"))

    class Meta:
        verbose_name = _('Proyecto')
        verbose_name_plural = _('Proyectos / Trabajos')

    def __str__(self):
        """String representation of this model objects."""

        return self.name

    def get_absolute_url(self):
        return reverse('project', args=[self.slug])

    @property
    def featured_image(self):
        """ Returns featured image from the set """

        featured = self.images.filter(views_featured=True)
        if not featured:
            return self.images.first()
        return featured.first()

    def save(self, *args, **kwargs):
        """Populate automatically 'slug' field"""
        if not self.slug:
            self.slug = slugify(self.name)

        super(Project, self).save(*args, **kwargs)


class ConnectionCategory(models.Model):

    name        = models.CharField(_('Nombre de la categoría'),  max_length=128, blank=False)
    description = models.TextField(_('Descripción opcional'), max_length=200, blank=True)
    color       = ColorField(_('Color de la categoría'), blank=True)

    class Meta:
        verbose_name = _('tipo de conexión')
        verbose_name_plural = _('tipos de conexión')

    def __str__(self):
        """String representation of this model objects."""

        return self.name


class Connection(models.Model):

    name        = models.CharField(_('Nombre'), max_length=200, blank=False, null=True)
    slug        = models.SlugField(editable=False)
    category    = models.ForeignKey(ConnectionCategory, verbose_name=_('Tipo'), blank=True, null=True, on_delete=models.SET_NULL)
    geolocation = PointField(_('Geolocalización'), blank=True)
    start_date  = models.DateField(_('Fecha de comienzo'), blank=True, null=True, help_text=_("Puedes usar el formato dd/mm/yyyy"))
    end_date    = models.DateField(_('Fecha de finalización'), blank=True, null=True, help_text=_("Puedes usar el formato dd/mm/yyyy"))
    description = RichTextUploadingField(_('Descripción'), blank=True, null=True)
    agents      = models.TextField(_('Agentes'), blank=True, null=True)
    tags        = models.ManyToManyField(Tag, verbose_name=_('Tags'), blank=True)
    images      = GenericRelation(Image)
    videos      = GenericRelation(Video)
    published   = models.BooleanField(_('Publicado'), default=False, help_text="Indica si este contenido es visible públicamente")
    featured    = models.BooleanField(_('Destacado'), default=False, help_text="Indica si este contenido es destacado y ha de tener mayor visibilidad")
    links       = GenericRelation(Link)


    class Meta:
        verbose_name = _('conexión')
        verbose_name_plural = _('conexiones')

    def get_absolute_url(self):
        return reverse('connection', args=[self.slug])

    def __str__(self):
        """String representation of this model objects."""

        return self.name

    def save(self, *args, **kwargs):
        """Populate automatically 'slug' field"""
        if not self.slug:
            self.slug = slugify(self.name)

        super(Connection, self).save(*args, **kwargs)


class TeamMember(models.Model):

    name      = models.CharField(_('Nombre'), max_length=200, blank=False, null=True)
    surname   = models.CharField(_('Apellidos'), max_length=200, blank=True, null=True)
    summary   = models.TextField(_('Resumen'), blank=True, null=True)
    image     = models.ImageField(_('Imagen principal'), blank=True)
    published = models.BooleanField(_('Publicado'), default=False, help_text="Indica si este contenido es visible públicamente")
    featured  = models.BooleanField(_('Destacado'), default=False, help_text="Indica si este contenido es destacado y ha de tener mayor visibilidad")

    class Meta:
        verbose_name = _('persona en Straddle3')
        verbose_name_plural = _('equipo Straddle3')

    @property
    def fullname(self):
        """Returns fullname of the person"""

        return "%s %s" % (self.name, self.surname)

    def __str__(self):
        """String representation of this model objects."""

        return self.fullname


class ResourceCategory(models.Model):

    name        = models.CharField(_('Nombre de la categoría'), max_length=128, blank=False)
    description = models.TextField(_('Descripción opcional'), max_length=200, blank=True)
    color       = ColorField(_('Color de la categoría'), blank=True)

    class Meta:
        verbose_name = _('tipo de recurso')
        verbose_name_plural = _('tipos de recurso')

    def __str__(self):
        """String representation of this model objects."""

        return self.name


class Resource(models.Model):

    name           = models.CharField(_('Nombre'), max_length=200, blank=False, null=True)
    slug           = models.SlugField(editable=False)
    category       = models.ForeignKey(ResourceCategory, verbose_name=_('Formato'), blank=True, null=True, on_delete=models.SET_NULL)
    use_text       = models.TextField(_('Funciones básicas/posibles aplicaciones'), blank=True, null=True)
    author_text    = models.TextField(_('Autor'), blank=True, null=True)
    promoter       = models.TextField(_('Promotor'), blank=True, null=True)
    gratitude_text = models.TextField(_('Texto de agradecimientos'), blank=True, null=True)
    license        = models.TextField(_('Licencia'), blank=True, null=True)
    description    = RichTextUploadingField(_('Descripción'), blank=True, null=True)
    tags           = models.ManyToManyField(Tag, verbose_name=_('Tags'), blank=True)
    published      = models.BooleanField(_('Publicado'), default=False, help_text="Indica si este contenido es visible públicamente")
    featured       = models.BooleanField(_('Destacado'), default=False, help_text="Indica si este contenido es destacado y ha de tener mayor visibilidad")
    images         = GenericRelation(Image)
    links          = GenericRelation(Link)
    videos         = GenericRelation(Video)

    class Meta:
        verbose_name = _('recurso')
        verbose_name_plural = _('recursos')

    def __str__(self):
        """String representation of this model objects."""

        return self.name

    def get_absolute_url(self):
        return reverse('resource', args=[self.slug])

    def save(self, *args, **kwargs):
        """Populate automatically 'slug' field"""
        if not self.slug:
            self.slug = slugify(self.name)

        super(Resource, self).save(*args, **kwargs)


class Block(models.Model):

    name = models.CharField(_('Nombre'), max_length=200, blank=False, null=True)
    body = RichTextUploadingField(_('Texto'), blank=True, null=True)

    class Meta:
        verbose_name = _('bloque')
        verbose_name_plural = _('bloques')

    def __str__(self):
        """String representation of this model objects."""

        return self.name
