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


class MapView(View):
    """ View to render content in a map """

    def get(self, request, *args, **kwargs):
        projects    = models.Project.objects.all()
        connections = models.Connection.objects.all()
        markers     = list(projects) + list(connections)
        print(markers)

        return render(request, 'pages/map.html', { 'markers' : markers })

# Dataset fake API for testing D3 widgets
def MapApi(request):
    markers = []
    projects    = models.Project.objects.filter(geolocation__isnull=False)
    for project in projects:
        img = project.images.first()
        start_date = project.start_date
        end_date   = project.end_date
        category   = project.category
        markers.append({
            'name'       : project.name,
            'url'        : project.get_absolute_url(),
            'pos'        : project.geolocation,
            'cat'        : category.name if category else None,
            'col'        : category.color if category else None,
            'img'        : img.image_file.url if img else None,
            'txt'        : project.summary if project.summary else None,
            'start_date' : start_date.strftime("%d %b %Y") if start_date else None,
            'end_date'   : end_date.strftime("%d %b %Y") if end_date else None,
        })
    connections = models.Connection.objects.filter(geolocation__isnull=False)
    for connection in connections:
        img = connection.images.first()
        start_date = connection.start_date
        end_date   = connection.end_date
        category   = connection.category
        markers.append({
            'name'       : connection.name,
            'url'        : connection.get_absolute_url(),
            'pos'        : connection.geolocation,
            'cat'        : category.name if category else None,
            'col'        : category.color if category else None,
            'img'        : img.image_file.url if img else None,
            'txt'        : connection.description if connection.description else None,
            'start_date' : start_date.strftime("%d %b %Y") if start_date else None,
            'end_date'   : end_date.strftime("%d %b %Y") if end_date else None,
        })

    return HttpResponse(json.dumps(markers), content_type="application/json")


class ProjectView(DetailView):
    """ View to display single projects """

    model = models.Project

class ProjectList(ListView):
    """ View to display a list of projects """

    model = models.Project
    ordering = ['-start_date', 'name']

class ConnectionView(DetailView):
    """ View to display single connections """

    model = models.Connection

class ConnectionList(ListView):
    """ View to display a list of connections """

    model = models.Connection
    ordering = ['name']

class TeamList(ListView):
    """ View to display a list of team members """

    model = models.TeamMember
    ordering = ['surname']

class ResourceList(ListView):
    """ View to display a list of resources """

    model = models.Resource
    ordering = ['name']

class ResourceView(DetailView):
    """ View to display single resources """

    model = models.Resource

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
