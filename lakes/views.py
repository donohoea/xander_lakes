import json
from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.serializers import serialize
from django.http import HttpResponse
from .models import Lake, Contour


class HomePageView(TemplateView):
    template_name = 'lakes/index.html'

class LakesView(TemplateView):
    template_name = 'lakes/lakes.html'


def lakes_geojson_view(request):
    lakes_as_geojson = serialize('geojson', Lake.objects.all(),
        geometry_field='perimeter', fields=('pk','name',))
    return HttpResponse(lakes_as_geojson)

def contours_geojson_view(request, lake_id):
    contours_as_geojson = serialize('geojson',
        Contour.objects.filter(lake=lake_id), geometry_field='geom',
        fields=('contour','calc_dep_m'));
    return HttpResponse(contours_as_geojson);
