from django.contrib.gis import admin
from django.contrib import admin as regAdmin
from .models import Lake,Contour

class ContourInLine(admin.TabularInline):
    model = Contour

@admin.register(Lake)
class LakeAdmin(admin.OSMGeoAdmin):
    search_fields = ['name',]
    inlines = [ContourInLine,]
