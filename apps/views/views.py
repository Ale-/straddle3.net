# python
import json
from itertools import chain
# django
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from django.http import Http404, HttpResponse
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
# project
from apps.models import models
from django.conf import settings

class FrontView(View):
    """ Frontpage """

    def get(self, request, *args, **kwargs):
        """ Handle GET requests. """

        # featured elements
        frontpage = models.Block.objects.filter(label="Inicio").first()

        # images for the front navigation block
        random_resource   = models.Resource.objects.filter(images__isnull=False).order_by('?').first()
        random_project    = models.Project.objects.filter(images__isnull=False).order_by('?').first()
        random_connection = models.Connection.objects.filter(images__isnull=False).order_by('?').first()

        return render(request, 'pages/front.html', locals())

class MapView(View):
    """ View to render content in a map """

    def get(self, request, *args, **kwargs):
        projects    = models.Project.objects.all()
        project_categories = models.ProjectCategory.objects.filter(project__isnull=False, project__published=True).distinct().order_by('name')
        project_categories = sorted(project_categories, key = lambda i: getattr(i, 'name'))
        connections = models.Connection.objects.all()
        connection_categories = models.ConnectionCategory.objects.filter(connection__isnull=False, connection__published=True).distinct().order_by('name')
        connection_categories = sorted(connection_categories, key = lambda i: getattr(i, 'name'))
        markers     = list(projects) + list(connections)
        return render(request, 'pages/map.html', {
            'markers'               : markers,
            'connection_categories' : connection_categories,
            'project_categories'    : project_categories,
        })

# Dataset fake API for testing D3 widgets
def MapApi(request):
    markers = []
    lang = request.LANGUAGE_CODE
    projects    = models.Project.objects.filter(geolocation__isnull=False)
    for project in projects:
        img        = project.featured_image
        category = project.category.first()
        markers.append({
            'name'       : project.t('name', lang),
            'subtitle'   : project.t('subtitle', lang),
            'url'        : project.get_absolute_url(),
            'pos'        : project.geolocation,
            'cat'        : category.t('name', lang) if category else None,
            'col'        : category.color if category else None,
            'img'        : img.image_file.url if img else None,
        })
    connections = models.Connection.objects.filter(geolocation__isnull=False)
    for connection in connections:
        img      = connection.featured_image
        category = connection.category
        markers.append({
            'name'       : connection.t('name', lang),
            'subtitle'   : connection.t('subtitle', lang),
            'url'        : connection.get_absolute_url(),
            'pos'        : connection.geolocation,
            'cat'        : category.t('name', lang) if category else None,
            'col'        : category.color if category else None,
            'img'        : img.image_file.url if img else None,
        })

    return HttpResponse(json.dumps(markers), content_type="application/json")


class ProjectView(DetailView):
    """ View to display single projects """

    model = models.Project

    def get_context_data(self, **kwargs):
        context = super(ProjectView, self).get_context_data(**kwargs)
        name = context['object'].name

        return context

class ProjectList(ListView):
    """ View to display a list of projects """

    model = models.Project
    ordering = ['-start_date', 'name']

    def get_queryset(self):
        """ Sets the queryset used in the view. """
        self.category = self.kwargs.get('category_slug', None)
        if self.category:
            if self.category == 'otros':
                return self.model.objects.exclude(
                    category__slug__in=['espacio-publico','equipamientos','vivienda']
                )
            return self.model.objects.filter(category__slug=self.category)
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        """ Sets the context data of the view. """
        context    = super(ProjectList, self).get_context_data(**kwargs)
        lang       = self.request.LANGUAGE_CODE
        categories = models.ProjectCategory.objects.filter(project__isnull=False, project__published=True)
        context['categories'] = list(set([ cat.t('name', lang) for cat in categories ]))
        context['categories'].sort()
        if self.category:
            if self.category == 'otros':
                context['category'] = 'otros'
            else:
                try:
                    category = categories.get(slug=self.category)
                    context['category'] = category.t('name', lang)
                except Exception as e:
                    pass
        return context

class ConnectionView(DetailView):
    """ View to display single connections """

    model = models.Connection

    def get_context_data(self, **kwargs):
        context = super(ConnectionView, self).get_context_data(**kwargs)
        name    = context['object'].name
        return context

class ConnectionList(ListView):
    """ View to display a list of connections """

    model = models.Connection
    ordering = ['name']

    def get_queryset(self):
        """ Sets the queryset used in the view. """
        self.category = self.kwargs.get('category_slug', None)
        if self.category:
            return self.model.objects.filter(category__slug=self.category)
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        """ Sets the context data of the view. """
        context = super(ConnectionList, self).get_context_data(**kwargs)
        lang       = self.request.LANGUAGE_CODE
        categories = models.ConnectionCategory.objects.filter(connection__isnull=False, connection__published=True)
        context['categories'] = list(set([ cat.t('name', lang) for cat in categories ]))
        context['categories'].sort()
        if self.category:
            try:
                category = categories.get(slug=self.category)
                context['category'] = category.t('name', lang)
            except Exception as e:
                pass
        return context

class TeamList(ListView):
    """ View to display a list of team members """

    model = models.TeamMember
    ordering = ['inactive', '?']

class ResourceList(ListView):
    """ View to display a list of resources """

    model = models.Resource
    ordering = ['name']

    def get_queryset(self):
        """ Sets the queryset used in the view. """
        self.category = self.kwargs.get('category_slug', None)
        if self.category:
            return self.model.objects.filter(category__slug=self.category)
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        """ Sets the context data of the view. """
        context = super(ResourceList, self).get_context_data(**kwargs)
        lang       = self.request.LANGUAGE_CODE
        categories = models.ResourceCategory.objects.filter(resource__isnull=False, resource__published=True)
        context['categories'] = list(set([ cat.t('name', lang) for cat in categories ]))
        context['categories'].sort()
        if self.category:
            try:
                category = categories.filter(slug=self.category).first()
                context['category'] = category.t('name', lang)
            except Exception as e:
                pass

        return context

class ResourceView(DetailView):
    """ View to display single resources """

    model = models.Resource

    def get_context_data(self, **kwargs):
        context = super(ResourceView, self).get_context_data(**kwargs)
        name = context['object'].name
        return context

class TagView(DetailView):
    """ Display tagged content. """

    model = models.Tag

    def get_context_data(self, **kwargs):
        context                = super(TagView, self).get_context_data(**kwargs)
        projects               = models.Project.objects.filter(tags=self.object)
        connections            = models.Connection.objects.filter(tags=self.object)
        resources              = models.Resource.objects.filter(tags=self.object)
        context['object_list'] = list(chain(projects, connections, resources))
        return context

class Blog(ListView):
    """ Blog :) """

    model = models.Post
    ordering = ['-date']

class PostView(DetailView):
    """ Display blog posts. """

    model = models.Post

    def get_context_data(self, **kwargs):
        context = super(PostView, self).get_context_data(**kwargs)
        date = context['object'].date
        context['previous_post'] = models.Post.objects.filter(date__lt=date).order_by('date').first()
        context['next_post'] = models.Post.objects.filter(date__gt=date).order_by('date').first()
        return context

class SearchView(View):
    """ Search page """

    def get(self, request, *args, **kwargs):
        # Arguments and results of the query
        text        = request.GET.get('q', '')
        object_list = []
        lang        = request.LANGUAGE_CODE
        # Create the queryset
        if text:
            query     = Q()
            query_blo = Q()
            query_con = Q()
            query_def = Q()
            if lang == 'es':
                query_blo = query|Q(name__icontains=text)|Q(body__icontains=text)
                query_con = query_blo|Q(subtitle__icontains=text)
                query_def = query_con|Q(summary__icontains=text)
            elif lang == 'en':
                query_blo = query|Q(name_en__icontains=text)|Q(body_en__icontains=text)
                query_con = query_blo|Q(subtitle_en__icontains=text)
                query_def = query_con|Q(summary_en__icontains=text)
            else:
                query_blo = query|Q(name_ca__icontains=text)|Q(body_ca__icontains=text)
                query_con = query_blo|Q(subtitle_ca__icontains=text)
                query_def = query_con|Q(summary_ca__icontains=text)

            posts       = models.Post.objects.filter(query_blo)
            connections = models.Connection.objects.filter(query_con)
            projects    = models.Project.objects.filter(query_def)
            resources   = models.Resource.objects.filter(query_def)
            content     = chain(projects, connections, resources, posts)
            object_list = sorted(content, key = lambda i: getattr(i, 'name'))

        return render(request, 'models/search_list.html', {
            'object_list' : object_list,
            'text'        : text,
        })

class Videos(View):

    def get(self, request, *args, **kwargs):
        # videos connected to the block
        # videos attached to other objects
        models_with_video = ['Proyecto', 'conexión', 'recurso']
        types = ContentType.objects.all() #filter(name__in=models_with_video)
        for t in types:
            print(t.app_label)
        videos = models.Video.objects.filter(content_type__in=types)
        return render(request, 'pages/videos.html', {
            'videos' : videos,
        })
