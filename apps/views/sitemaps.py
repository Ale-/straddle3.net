# django
from django.contrib.sitemaps import Sitemap
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
# project
from apps.models import models

class StaticSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return ['front', 'what', 'who', 'team', 'archive', 'open_fridays', 'repository', 'cv', 'bibliography', 'press', 'videos' ]

    def location(self, item):
        return reverse(item)


class DynamicSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return self.model.objects.filter(published=True)

    def lastmod(self, obj):
        ct = ContentType.objects.get(model=self.modelname)
        log = LogEntry.objects.all().filter(
            content_type=ct,
            object_id=obj.id).order_by('action_time').first()
        return log.action_time

class ProjectSitemap(DynamicSitemap):
    model     = models.Project
    modelname = "project"

class ConnectionSitemap(DynamicSitemap):
    model     = models.Connection
    modelname = "connection"

class ResourceSitemap(DynamicSitemap):
    model     = models.Resource
    modelname = "resource"

class BlogSitemap(DynamicSitemap):
    model     = models.Post
    modelname = "post"
