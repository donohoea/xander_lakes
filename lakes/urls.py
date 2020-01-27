from django.urls import path
from .views import HomePageView, LakesView, lakes_geojson_view, contours_geojson_view

app_name = 'lakes'

urlpatterns = [
    path('',HomePageView.as_view(), name='home'),
    path('lakes/', LakesView.as_view(), name='lakes'),
    path('lakes/geojson', lakes_geojson_view, name='lakes'),
    path('contours/<int:lake_id>/geojson', contours_geojson_view, name='contours'),
]
