from django.urls import path
from .views import HomePageView, LeafletView, lakes_view, contours_view

app_name = 'lakes'

urlpatterns = [
    path('',HomePageView.as_view(), name='home'),
    path('leaflet/', LeafletView.as_view(), name='leaflet'),
    path('lakes/', lakes_view, name='lakes'),
    path('contours/<int:lake_id>/', contours_view, name='contours'),
]
