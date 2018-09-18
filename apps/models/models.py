# django
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify
from django.utils.timezone import now
from django.urls import reverse
# contrib
from ckeditor_uploader.fields import RichTextUploadingField
from djgeojson.fields import PointField
from adminsortable.models import SortableMixin
from colorfield.fields import ColorField
# project
from .categories import FORMATS
from . import validators, utils
from django.conf import settings

validate_image_size = validators.ImageSizeValidator({ 'min_width' : 480, 'min_height' : 480, 'max_width' : 1920, 'max_height' : 1280 })
validate_image_type = validators.ImageTypeValidator(["jpeg", "png"])
validate_file_type  = validators.FileTypeValidator()
images_path         = utils.RenameImage("images/")
files_path          = utils.RenameFile("files/")

""" Generic models """


class Translatable(models.Model):

    def t(self, field_name, lang):
        """ Returns the translated value of the given field, with a fallback to default language. """
        translated = False
        source     = getattr(self, field_name)
        if lang != settings.LANGUAGE_CODE:
            translated = getattr(self, '%s_%s' % ( field_name, lang))
        return translated if translated else source if source else None

    class Meta:
        abstract = True

class Video(SortableMixin):
    """ Images """

    source_url     = models.CharField(_('Video'), max_length=200, blank=True, null=True,
                                       help_text=_('Inserta la url de un video de Youtube o Vimeo'))
    caption        = models.CharField(_('Pie de video opcional'), max_length=200, blank=True, null=True)
    caption_en     = models.CharField(_('Pie EN'), max_length=200, blank=True, null=True)
    caption_ca     = models.CharField(_('Pie CA'), max_length=200, blank=True, null=True)
    not_caption    = models.BooleanField(_('No mostrar pie de video'), default=True, help_text=_("No mostrar el pie de video en las galerías"))
    content_type   = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id      = models.PositiveIntegerField()
    source_content = GenericForeignKey('content_type', 'object_id')
    order          = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        """String representation of this model objects."""

        return self.source_content.name if self.source_content else "Video %s" % self.id

class Image(SortableMixin):
    """ Images """

    image_file     = models.ImageField(_('Archivo de imagen'), blank=False,
                                       validators=[validate_image_size, validate_image_type],
                                       upload_to=images_path)
    caption        = models.CharField(_('Texto alternativo/Pie de foto'), max_length=200, blank=False, null=True)
    caption_en     = models.CharField(_('Texto/Pie EN'), max_length=200, blank=True, null=True)
    caption_ca     = models.CharField(_('Texto/Pie CA'), max_length=200, blank=True, null=True)
    content_type   = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id      = models.PositiveIntegerField()
    source_content = GenericForeignKey('content_type', 'object_id')
    order          = models.PositiveIntegerField(default=0, editable=False, db_index=True)
    not_caption    = models.BooleanField(_('No mostrar pie de foto'), default=True, help_text=_("No mostrar el pie de foto en las galerías"))
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

    name            = models.CharField(_('Nombre del archivo'), max_length=200, blank=False, null=True)
    name_en         = models.CharField(_('Nombre EN'), max_length=200, blank=True, null=True)
    name_ca         = models.CharField(_('Nombre CA'), max_length=200, blank=True, null=True)
    attachment_file = models.FileField(_('Archivo adjunto'), blank=False,
                                        validators=[validate_file_type],
                                        upload_to=files_path)
    caption         = models.CharField(_('Descripción opcional'), max_length=200, blank=True, null=True)
    caption_en      = models.CharField(_('Descripción EN'), max_length=200, blank=True, null=True)
    caption_ca      = models.CharField(_('Descripción CA'), max_length=200, blank=True, null=True)
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
    caption        = models.CharField(_('Texto del enlace'), max_length=200, blank=True)
    caption_en     = models.CharField(_('Texto EN'), max_length=200, blank=True)
    caption_ca     = models.CharField(_('Texto CA'), max_length=200, blank=True)
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

    name    = models.CharField(_('Tag'), blank=False, max_length=128)
    name_en = models.CharField(_('Tag EN'), blank=True, max_length=128)
    name_ca = models.CharField(_('Tag CA'), blank=True, max_length=128)
    body    = models.TextField(_('Descripción opcional'), max_length=200, blank=True)
    body_en = models.TextField(_('Descripción EN'), max_length=200, blank=True)
    body_ca = models.TextField(_('Descripción CA'), max_length=200, blank=True)
    slug    = models.SlugField(editable=False, blank=True)

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

class ProjectCategory(Translatable):

    name    = models.CharField(_('Nombre de la categoría'), max_length=128, blank=False)
    name_en = models.CharField(_('Nombre EN'), blank=True, max_length=128)
    name_ca = models.CharField(_('Nombre CA'), blank=True, max_length=128)
    color   = ColorField(_('Color de la categoría'), blank=True)
    body    = models.TextField(_('Descripción opcional'), max_length=200, blank=True)
    body_en = models.TextField(_('Descripción EN'), max_length=200, blank=True)
    body_ca = models.TextField(_('Descripción CA'), max_length=200, blank=True)
    slug    = models.SlugField(editable=False, blank=True)

    class Meta:
        verbose_name        = _('tipo de proyecto')
        verbose_name_plural = _('tipos de proyecto')

    def __str__(self):
        """String representation of this model objects."""
        return self.name

    def save(self, *args, **kwargs):
        """Populate automatically 'slug' field"""
        if not self.slug:
            self.slug = slugify(self.name)
        super(ProjectCategory, self).save(*args, **kwargs)

class Project(Translatable):
    """ Projects """

    name             = models.CharField(_('Nombre del proyecto'), max_length=200, blank=False, null=True)
    subtitle         = models.CharField(_('Subtítulo'), max_length=200, blank=True, null=True)
    summary          = models.TextField(_('Resumen'), blank=True, null=True)
    body             = RichTextUploadingField(_('Texto'), blank=True, null=True)
    slug             = models.SlugField(editable=False, blank=True)
    start_date       = models.DateField(_('Fecha de comienzo'), blank=True, null=True, help_text=_("Puedes usar el formato dd/mm/yyyy"))
    end_date         = models.DateField(_('Fecha de finalización'), blank=True, null=True, help_text=_("Puedes usar el formato dd/mm/yyyy"))
    geolocation      = PointField(_('Geolocalización'), blank=True)
    category         = models.ManyToManyField(ProjectCategory, verbose_name=_('Formato'), related_name='project', blank=True)
    promoter         = models.TextField(_('Promotor'), blank=True, null=True)
    author_text      = models.TextField(_('Créditos'), blank=True, null=True)
    gratitude_text   = models.TextField(_('Agradecimientos'), blank=True, null=True)
    images           = GenericRelation(Image)
    tags             = models.ManyToManyField(Tag, verbose_name=_('Tags'), blank=True)
    published        = models.BooleanField(_('Publicado'), default=False, help_text=_("Indica si este contenido es visible públicamente"))
    featured         = models.BooleanField(_('Destacado'), default=False, help_text=_("Indica si este contenido es destacado y ha de tener mayor visibilidad"))
    links            = GenericRelation(Link)
    videos           = GenericRelation(Video)
    attachments      = GenericRelation(Attachment)
    related_projects    = models.ManyToManyField('self', blank=True, verbose_name=_('Proyectos relacionados'), help_text=_("Selecciona los proyectos relacionados"))
    related_connections = models.ManyToManyField('models.Connection', blank=True, verbose_name=_('Conexiones relacionadas'), help_text=_("Selecciona los conexiones relacionados"))
    related_resources   = models.ManyToManyField('models.Resource', blank=True, verbose_name=_('Recursos relacionados'), help_text=_("Selecciona los recursos relacionados"))

    # en
    name_en           = models.CharField(_('Nombre del proyecto'), max_length=200, blank=True, null=True)
    subtitle_en       = models.CharField(_('Subtítulo'), max_length=200, blank=True, null=True)
    summary_en        = models.TextField(_('Resumen'), blank=True, null=True)
    body_en           = RichTextUploadingField(_('Texto'), blank=True, null=True)
    promoter_en       = models.TextField(_('Promotor'), blank=True, null=True)
    author_text_en    = models.TextField(_('Autor'), blank=True, null=True)
    gratitude_text_en = models.TextField(_('Texto de agradecimientos'), blank=True, null=True)

    # ca
    name_ca           = models.CharField(_('Nombre del proyecto'), max_length=200, blank=True, null=True)
    subtitle_ca       = models.CharField(_('Subtítulo'), max_length=200, blank=True, null=True)
    summary_ca        = models.TextField(_('Resumen'), blank=True, null=True)
    body_ca           = RichTextUploadingField(_('Texto'), blank=True, null=True)
    promoter_ca       = models.TextField(_('Promotor'), blank=True, null=True)
    author_text_ca    = models.TextField(_('Autor'), blank=True, null=True)
    gratitude_text_ca = models.TextField(_('Texto de agradecimientos'), blank=True, null=True)

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

    @property
    def related(self):
        return utils.get_related(self)

    def save(self, *args, **kwargs):
        """Populate automatically 'slug' field"""
        if not self.slug:
            self.slug = slugify(self.name)

        super(Project, self).save(*args, **kwargs)

class ConnectionCategory(Translatable):

    name    = models.CharField(_('Nombre de la categoría'),  max_length=128, blank=False)
    name_en = models.CharField(_('Nombre EN'),  max_length=128, blank=True)
    name_ca = models.CharField(_('Nombre CA'),  max_length=128, blank=True)
    body    = models.TextField(_('Descripción opcional'), max_length=200, blank=True)
    body_en = models.TextField(_('Descripción EN'), max_length=200, blank=True)
    body_ca = models.TextField(_('Descripción CA'), max_length=200, blank=True)
    color   = ColorField(_('Color de la categoría'), blank=True)
    slug    = models.SlugField(editable=False, blank=True)

    class Meta:
        verbose_name = _('tipo de conexión')
        verbose_name_plural = _('tipos de conexión')

    def __str__(self):
        """String representation of this model objects."""
        return self.name

    def save(self, *args, **kwargs):
        """Populate automatically 'slug' field"""
        if not self.slug:
            self.slug = slugify(self.name)
        super(ConnectionCategory, self).save(*args, **kwargs)


class Connection(Translatable):

    name        = models.CharField(_('Nombre'), max_length=200, blank=False, null=True)
    subtitle    = models.CharField(_('Subtítulo'), max_length=200, blank=True, null=True)
    slug        = models.SlugField(editable=False)
    category    = models.ForeignKey(ConnectionCategory, verbose_name=_('Tipo'), related_name='connection', blank=True, null=True, on_delete=models.SET_NULL)
    geolocation = PointField(_('Geolocalización'), blank=True)
    start_date  = models.DateField(_('Fecha de comienzo'), blank=True, null=True, help_text=_("Puedes usar el formato dd/mm/yyyy"))
    end_date    = models.DateField(_('Fecha de finalización'), blank=True, null=True, help_text=_("Puedes usar el formato dd/mm/yyyy"))
    body        = RichTextUploadingField(_('Descripción'), blank=True, null=True)
    agents      = models.TextField(_('Agentes'), blank=True, null=True)
    tags        = models.ManyToManyField(Tag, verbose_name=_('Tags'), blank=True)
    images      = GenericRelation(Image)
    videos      = GenericRelation(Video)
    published   = models.BooleanField(_('Publicado'), default=False, help_text="Indica si este contenido es visible públicamente")
    featured    = models.BooleanField(_('Destacado'), default=False, help_text="Indica si este contenido es destacado y ha de tener mayor visibilidad")
    links       = GenericRelation(Link)
    attachments = GenericRelation(Attachment)
    related_projects    = models.ManyToManyField('models.Project', blank=True, verbose_name=_('Proyectos relacionados'), help_text=_("Selecciona los proyectos relacionados"))
    related_connections = models.ManyToManyField('self', blank=True, verbose_name=_('Conexiones relacionadas'), help_text=_("Selecciona los conexiones relacionados"))
    related_resources   = models.ManyToManyField('models.Resource', blank=True, verbose_name=_('Recursos relacionados'), help_text=_("Selecciona los recursos relacionados"))

    # en
    name_en        = models.CharField(_('Nombre'), max_length=200, blank=True, null=True)
    subtitle_en    = models.CharField(_('Subtítulo'), max_length=200, blank=True, null=True)
    body_en        = RichTextUploadingField(_('Descripción'), blank=True, null=True)
    agents_en     = models.TextField(_('Agentes'), blank=True, null=True)

    # ca
    name_ca        = models.CharField(_('Nombre'), max_length=200, blank=True, null=True)
    subtitle_ca    = models.CharField(_('Subtítulo'), max_length=200, blank=True, null=True)
    body_ca        = RichTextUploadingField(_('Descripción'), blank=True, null=True)
    agents_ca     = models.TextField(_('Agentes'), blank=True, null=True)

    class Meta:
        verbose_name = _('conexión')
        verbose_name_plural = _('conexiones')

    def get_absolute_url(self):
        return reverse('connection', args=[self.slug])

    def __str__(self):
        """String representation of this model objects."""

        return self.name

    @property
    def related(self):
        return utils.get_related(self)

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

        super(Connection, self).save(*args, **kwargs)


class TeamMember(models.Model):

    name       = models.CharField(_('Nombre'), max_length=200, blank=False, null=True)
    surname    = models.CharField(_('Apellidos'), max_length=200, blank=True, null=True)
    summary    = models.TextField(_('Resumen'), blank=True, null=True)
    summary_en = models.TextField(_('Resumen'), blank=True, null=True)
    summary_ca = models.TextField(_('Resumen'), blank=True, null=True)
    image      = models.ImageField(_('Imagen principal'), blank=True)
    published  = models.BooleanField(_('Publicado'), default=False, help_text="Indica si este contenido es visible públicamente")
    inactive   = models.BooleanField(_('Inactivo'), default=False, help_text="Indica si esta persona ya no participa actualmente en S3")

    class Meta:
        verbose_name = _('persona en Straddle3')
        verbose_name_plural = _('equipo Straddle3')

    @property
    def fullname(self):
        """Returns fullname of the person"""

        return "%s %s" % (self.name, self.surname if self.surname else '')

    def __str__(self):
        """String representation of this model objects."""

        return self.fullname


class ResourceCategory(Translatable):

    name    = models.CharField(_('Nombre de la categoría'), max_length=128, blank=False)
    name_en = models.CharField(_('Nombre EN'), max_length=128, blank=True)
    name_ca = models.CharField(_('Nombre CA'), max_length=128, blank=True)
    body    = models.TextField(_('Descripción opcional'), max_length=200, blank=True)
    body_en = models.TextField(_('Descripción EN'), max_length=200, blank=True)
    body_ca = models.TextField(_('Descripción CA'), max_length=200, blank=True)
    color   = ColorField(_('Color de la categoría'), blank=True)
    slug    = models.SlugField(editable=False, blank=True)

    class Meta:
        verbose_name = _('tipo de recurso')
        verbose_name_plural = _('tipos de recurso')

    def __str__(self):
        """String representation of this model objects."""

        return self.name

    def save(self, *args, **kwargs):
        """Populate automatically 'slug' field"""
        if not self.slug:
            self.slug = slugify(self.name)
        super(ResourceCategory, self).save(*args, **kwargs)


class Resource(models.Model):

    name           = models.CharField(_('Nombre'), max_length=200, blank=False, null=True)
    subtitle       = models.CharField(_('Subtítulo'), max_length=200, blank=True, null=True)
    slug           = models.SlugField(editable=False)
    category       = models.ForeignKey(ResourceCategory, verbose_name=_('Formato'), related_name='resource', blank=True, null=True, on_delete=models.SET_NULL)
    use_text       = models.TextField(_('Funciones básicas/posibles aplicaciones'), blank=True, null=True)
    author_text    = models.TextField(_('Créditos'), blank=True, null=True)
    promoter       = models.TextField(_('Promotor'), blank=True, null=True)
    gratitude_text = models.TextField(_('Agradecimientos'), blank=True, null=True)
    license        = models.TextField(_('Licencia'), blank=True, null=True)
    summary        = models.TextField(_('Resumen'), blank=True, null=True)
    body           = RichTextUploadingField(_('Descripción'), blank=True, null=True)
    tags           = models.ManyToManyField(Tag, verbose_name=_('Tags'), blank=True)
    published      = models.BooleanField(_('Publicado'), default=False, help_text="Indica si este contenido es visible públicamente")
    featured       = models.BooleanField(_('Destacado'), default=False, help_text="Indica si este contenido es destacado y ha de tener mayor visibilidad")
    images         = GenericRelation(Image)
    links          = GenericRelation(Link)
    videos         = GenericRelation(Video)
    attachments    = GenericRelation(Attachment)
    related_projects    = models.ManyToManyField('models.Project', blank=True, verbose_name=_('Proyectos relacionados'), help_text=_("Selecciona los proyectos relacionados"))
    related_connections = models.ManyToManyField('models.Connection', blank=True, verbose_name=_('Conexiones relacionadas'), help_text=_("Selecciona los conexiones relacionados"))
    related_resources   = models.ManyToManyField('self', blank=True, verbose_name=_('Recursos relacionados'), help_text=_("Selecciona los recursos relacionados"))

    # en
    name_en           = models.CharField(_('Nombre'), max_length=200, blank=True, null=True)
    subtitle_en       = models.CharField(_('Subtítulo'), max_length=200, blank=True, null=True)
    summary_en        = models.TextField(_('Resumen'), blank=True, null=True)
    body_en           = RichTextUploadingField(_('Descripción'), blank=True, null=True)
    use_text_en       = models.TextField(_('Funciones básicas/posibles aplicaciones'), blank=True, null=True)
    author_text_en    = models.TextField(_('Autor'), blank=True, null=True)
    promoter_en       = models.TextField(_('Promotor'), blank=True, null=True)
    gratitude_text_en = models.TextField(_('Texto de agradecimientos'), blank=True, null=True)
    license_en        = models.TextField(_('Licencia'), blank=True, null=True)

    # ca
    name_ca           = models.CharField(_('Nombre'), max_length=200, blank=True, null=True)
    subtitle_ca       = models.CharField(_('Subtítulo'), max_length=200, blank=True, null=True)
    body_ca           = RichTextUploadingField(_('Descripción'), blank=True, null=True)
    summary_ca        = models.TextField(_('Resumen'), blank=True, null=True)
    use_text_ca       = models.TextField(_('Funciones básicas/posibles aplicaciones'), blank=True, null=True)
    author_text_ca    = models.TextField(_('Autor'), blank=True, null=True)
    promoter_ca       = models.TextField(_('Promotor'), blank=True, null=True)
    gratitude_text_ca = models.TextField(_('Texto de agradecimientos'), blank=True, null=True)
    license_ca        = models.TextField(_('Licencia'), blank=True, null=True)


    class Meta:
        verbose_name = _('recurso')
        verbose_name_plural = _('recursos')

    def __str__(self):
        """String representation of this model objects."""

        return self.name

    def get_absolute_url(self):
        return reverse('resource', args=[self.slug])

    @property
    def related(self):
        return utils.get_related(self)

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

        super(Resource, self).save(*args, **kwargs)


class Block(models.Model):

    label       = models.CharField(_('Etiqueta'), max_length=200,
                                   blank=True, null=True,)
    name        = models.CharField(_('Nombre'), max_length=200,
                                   blank=True, null=True,
                                   help_text=_('Introduce el título del bloque, si no quieres que el bloque tenga título deja este campo en blanco'))
    name_en     = models.CharField(_('Nombre'), max_length=200,
                                   blank=True, null=True,
                                   help_text=_('Introduce el título del bloque, si no quieres que el bloque tenga título deja este campo en blanco'))
    name_ca     = models.CharField(_('Nombre'), max_length=200,
                                   blank=True, null=True,
                                   help_text=_('Introduce el título del bloque, si no quieres que el bloque tenga título deja este campo en blanco'))
    body        = RichTextUploadingField(_('Texto'), blank=True, null=True)
    body_en     = RichTextUploadingField(_('Texto'), blank=True, null=True)
    body_ca     = RichTextUploadingField(_('Texto'), blank=True, null=True)
    images      = GenericRelation(Image)
    videos      = GenericRelation(Video)
    attachments = GenericRelation(Attachment)

    class Meta:
        verbose_name = _('bloque de texto')
        verbose_name_plural = _('bloques de texto')

    def __str__(self):
        """String representation of this model objects."""

        return self.label if self.label else self.name if self.name else self.pk


class Post(models.Model):

    name      = models.CharField(_('Nombre/título'), max_length=200, blank=False, null=True)
    slug      = models.SlugField(editable=False)
    published = models.BooleanField(_('Publicado'), default=True, help_text=_("Indica si este contenido es visible públicamente"))
    summary   = models.TextField(_('Resumen'), blank=True, null=True)
    date      = models.DateField(_('Fecha de publicación'), default=now, blank=True)
    body      = RichTextUploadingField(_('Cuerpo'), blank=True, null=True)
    tags      = models.ManyToManyField(Tag, verbose_name=_('Tags'), blank=True)
    images    = GenericRelation(Image)
    links     = GenericRelation(Link)
    videos    = GenericRelation(Video)

    # en
    name_en    = models.CharField(_('Nombre/título'), max_length=200, blank=True, null=True)
    summary_en = models.TextField(_('Resumen'), blank=True, null=True)
    body_en    = RichTextUploadingField(_('Cuerpo'), blank=True, null=True)

    # ca
    name_ca    = models.CharField(_('Nombre/título'), max_length=200, blank=True, null=True)
    summary_ca = models.TextField(_('Resumen'), blank=True, null=True)
    body_ca    = RichTextUploadingField(_('Cuerpo'), blank=True, null=True)

    def __str__(self):
        """String representation of this model objects."""
        return self.name

    def save(self, *args, **kwargs):
        """Populate automatically 'slug' field"""
        if not self.slug:
            self.slug = slugify(self.name)
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post', args=[self.slug])

    @property
    def featured_image(self):
        """ Returns featured image from the set """

        featured = self.images.filter(views_featured=True)
        if not featured:
            return self.images.first()
        return featured.first()
