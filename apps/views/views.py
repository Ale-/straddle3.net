# python
import json
from itertools import chain
# django
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from django.http import Http404, HttpResponse
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
        connections = models.Connection.objects.all()
        markers     = list(projects) + list(connections)

        return render(request, 'pages/map.html', { 'markers' : markers })

# Dataset fake API for testing D3 widgets
def MapApi(request):
    markers = []
    lang = request.LANGUAGE_CODE
    projects    = models.Project.objects.filter(geolocation__isnull=False)
    for project in projects:
        img      = project.featured_image
        category = project.category
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
        context['previous_project'] = models.Project.objects.filter(name__lt=name).order_by('-name').first()
        context['next_project'] = models.Project.objects.filter(name__gt=name).order_by('name').first()

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
        context = super(ProjectList, self).get_context_data(**kwargs)
        if self.category:
            if self.category == 'otros':
                context['category'] = 'otros'
            else:
                category = models.ProjectCategory.objects.filter(slug=self.category).first()
                if category:
                    translated = False
                    if self.request.LANGUAGE_CODE != settings.LANGUAGE_CODE:
                        translated = getattr(category, 'name_%s' % self.request.LANGUAGE_CODE)
                    context['category'] = translated if translated else getattr(category, 'name')
        return context

class ConnectionView(DetailView):
    """ View to display single connections """

    model = models.Connection

    def get_context_data(self, **kwargs):
        context = super(ConnectionView, self).get_context_data(**kwargs)
        name    = context['object'].name
        context['previous_connection'] = models.Connection.objects.filter(name__lt=name).order_by('name').first()
        context['next_connection']     = models.Connection.objects.filter(name__gt=name).order_by('name').first()
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
        category = models.ConnectionCategory.objects.filter(slug=self.category).first()
        if category:
            translated = False
            if self.request.LANGUAGE_CODE != settings.LANGUAGE_CODE:
                translated = getattr(category, 'name_%s' % self.request.LANGUAGE_CODE)
            context['category'] = translated if translated else getattr(category, 'name')
        return context

class TeamList(ListView):
    """ View to display a list of team members """

    model = models.TeamMember
    ordering = ['surname']

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
        category = models.ResourceCategory.objects.filter(slug=self.category).first()
        if category:
            translated = False
            if self.request.LANGUAGE_CODE != settings.LANGUAGE_CODE:
                translated = getattr(category, 'name_%s' % self.request.LANGUAGE_CODE)
            context['category'] = translated if translated else getattr(category, 'name')
        return context

class ResourceView(DetailView):
    """ View to display single resources """

    model = models.Resource

    def get_context_data(self, **kwargs):
        context = super(ResourceView, self).get_context_data(**kwargs)
        name = context['object'].name
        context['previous_resource'] = models.Resource.objects.filter(name__lt=name).order_by('name').first()
        context['next_resource'] = models.Resource.objects.filter(name__gt=name).order_by('name').first()
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
