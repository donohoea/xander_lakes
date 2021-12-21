from django.urls import path, re_path
from .views import HomePageView, LakesView, catchall, lakes_list_view, lakes_geojson_view, contours_geojson_view

app_name = 'lakes'

urlpatterns = [
    #path('',HomePageView.as_view(), name='home'),
    path('lakes/', LakesView.as_view(), name='lakes'),
    path('lakes/list', lakes_list_view, name='lakes_list'),
    path('lakes/geojson', lakes_geojson_view, name='lakes_geojson'),
    path('contours/<int:lake_id>/geojson', contours_geojson_view, name='contours'),
    re_path(r'', catchall),
]
