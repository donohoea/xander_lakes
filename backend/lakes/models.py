from django.contrib.gis.db import models


class Lake(models.Model):
    name = models.CharField(max_length=50)
    perimeter = models.MultiPolygonField(srid=4326)

    class Meta():
        ordering = ['name']

    def __str__(self):
        return self.name


class Contour(models.Model):
    contour = models.FloatField()
    cont_id = models.IntegerField()
    calc_dep_m = models.FloatField()
    geom = models.MultiLineStringField(srid=4326)
    lake = models.ForeignKey(Lake,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.lake.name}: {self.calc_dep_m}m"
