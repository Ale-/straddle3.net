# python
import json
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
    projects    = models.Project.objects.all()
    for project in projects:
        img = project.images.first()
        start_date = project.start_date
        end_date   = project.end_date
        markers.append({
            'name'       : project.name,
            'slug'       : project.slug,
            'pos'        : project.geolocation,
            'cat'        : project.category.name,
            'col'        : project.category.color,
            'img'        : img.image_file.url if img else None,
            'start_date' : start_date.strftime("%d %b %Y") if start_date else None,
            'end_date'   : end_date.strftime("%d %b %Y") if end_date else None,
        })
    connections = models.Connection.objects.all()
    for connection in connections:
        img = connection.images.first()
        start_date = connection.start_date
        end_date   = connection.end_date
        markers.append({
            'name'       : connection.name,
            'slug'       : connection.slug,
            'pos'        : connection.geolocation,
            'cat'        : connection.category.name,
            'col'        : connection.category.color,
            'img'        : img.image_file.url if img else None,
            'start_date' : start_date.strftime("%d %b %Y") if start_date else None,
            'end_date'   : end_date.strftime("%d %b %Y") if end_date else None,
        })

    return HttpResponse(json.dumps(markers), content_type="application/json")
