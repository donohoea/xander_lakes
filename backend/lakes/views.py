import requests
from django.conf import settings
from django.template import engines
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.core.serializers import serialize
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from .models import Lake, Contour


class HomePageView(TemplateView):
    template_name = 'lakes/index.html'

class LakesView(TemplateView):
    template_name = 'lakes/lakes.html'

catchall_prod = TemplateView.as_view(template_name='index.html')


@csrf_exempt
def catchall_dev(request, upstream='http://localhost:3000'):
    """
    Proxy HTTP requests to the frontend dev server in development.

    The implementation is very basic e.g. it doesn't handle HTTP headers.

    """
    upstream_url = upstream + request.path
    method = request.META['REQUEST_METHOD'].lower()
    response = getattr(requests, method)(upstream_url, stream=True)
    content_type = response.headers.get('Content-Type')

    if request.META.get('HTTP_UPGRADE', '').lower() == 'websocket':
        return HttpResponse(
            content="WebSocket connections aren't supported",
            status=501,
            reason="Not Implemented"
        )

    elif content_type == 'text/html; charset=UTF-8':
        return HttpResponse(
            content=engines['django'].from_string(response.text).render(),
            status=response.status_code,
            reason=response.reason,
        )

    else:
        return StreamingHttpResponse(
            streaming_content=response.iter_content(2 ** 12),
            content_type=content_type,
            status=response.status_code,
            reason=response.reason,
        )

catchall = catchall_dev if settings.DEBUG else catchall_prod

def lakes_geojson_view(request):
    redis_key = 'lakes'
    lakes_as_geojson = cache.get(redis_key)
    if not lakes_as_geojson:
        lakes_as_geojson = serialize('geojson', Lake.objects.all(),
            geometry_field='perimeter', fields=('pk','name',))
        cache.set(redis_key, lakes_as_geojson)
    return HttpResponse(lakes_as_geojson)

def contours_geojson_view(request, lake_id):
    redis_key = f'contours{lake_id}'
    contours_as_geojson = cache.get(redis_key)
    if not contours_as_geojson:
        contours_as_geojson = serialize('geojson',
            Contour.objects.filter(lake=lake_id), geometry_field='geom',
            fields=('contour','calc_dep_m'))
        cache.set(redis_key, contours_as_geojson)
    return HttpResponse(contours_as_geojson)

def lakes_list_view(request):
    lakes = Lake.objects.values_list('id', 'name')
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    lakes_alpha_lists = []
    for i in range(26):
        lakes_alpha_lists.append([])

    for lake in lakes:
        lakes_alpha_lists[alphabet.index(lake[1][0])].append(lake)

    paginated_lakes = []
    page = []
    firstLetter = 'A'

    for i, letter_list in enumerate(lakes_alpha_lists + []):
        if len(page) + len(letter_list) > 15:
            if firstLetter != alphabet[i-1]: label = f'{firstLetter}-{alphabet[i-1]}'
            else: label = f'{alphabet[i-1]}'
            paginated_lakes.append([page,label])
            firstLetter = alphabet[i]
            page = []
        elif i == 25:
            label = f'{firstLetter}-{alphabet[i]}'
            page += letter_list
            paginated_lakes.append([page,label])
        page += letter_list

    return JsonResponse(paginated_lakes, safe=False)
