import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','xander.settings')

import django
django.setup()
from pathlib import Path
from django.contrib.gis.utils import LayerMapping
from lakes.models import Lake, Contour
from django.contrib.gis.db.models import Union

base_dir = Path('.') / 'backend' / 'lakes' / 'data'

def run():
    print(f'{base_dir}')
    perimeter_load()
    contour_load()

def perimeter_load(verbose=True):
    #Load Lake Perimeter Data from shapefiles
    for path in base_dir.rglob('*_bdy_py_tm.shp'):
        lm = LayerMapping(Lake, str(path), lake_mapping)
        lm.save(strict=True, verbose=verbose)
        #Lakes with names longer than 20 characters have clipped names in shapefile
        #Replace clipped name with full name from directory name
        lake_name = path.parent.name
        if len(lake_name) > 20:
            try:
                lake = Lake.objects.get(name=lake_name[:20])
                lake.name = lake_name
                lake.save()
            except Lake.DoesNotExist:
                print(f'{lake_name} does not exist')

    #merge and remove lakes from lake chains that were saved as multiple
    #lake instances of the same name
    merge_chains()

    #Special case where McLeod lake data mislabeled Little McLeod Lake
    try:
        mcleod = Lake.objects.get(name="Little McLeod Lake")
        mcleod.name = "McLeod Lake"
        mcleod.save()
    except:
        print('Could not updat Little McLeod Lake to McLeod Lake')



def merge_chains():
        for lake in Lake.objects.all():
            chain_lakes = Lake.objects.filter(name=lake.name)
            if chain_lakes.count() > 1:
                chain_perimeter = chain_lakes.aggregate(Union('perimeter'))
                lake.perimeter = chain_perimeter['perimeter__union']
                print('Saving ' + lake.name + ' chain')
                lake.save()
                for chain_lake in chain_lakes:
                    if not chain_lake.id == lake.id:
                        print('Deleting redundant ' + chain_lake.name)
                        chain_lake.delete()

def contour_load(verbose=True):
    #Load contour data from shapefiles and associate with Lake instances
    for path in base_dir.rglob('*_bcon_ln_tm.shp'):
            lake_name = path.parent.name
            try:
                lake = Lake.objects.get(name=lake_name)
                lm = CustomLayerMapping(Contour, str(path), contour_mapping, custom={'lake':lake})
                print(str(lm))
                lm.save(strict=True, verbose=verbose)

            except Lake.DoesNotExist:
                print(f'{lake_name} does not exist')
            except Lake.MultipleObjectsReturned:
                print(f'More than on {lake_name} record exists')



class CustomLayerMapping(LayerMapping):
    def __init__(self, *args, **kwargs):
        self.custom = kwargs.pop('custom', {})
        super(CustomLayerMapping, self).__init__(*args, **kwargs)

    def feature_kwargs(self, feature):
        kwargs = super(CustomLayerMapping, self).feature_kwargs(feature)
        kwargs.update(self.custom)
        return kwargs

lake_mapping = {
    'name': 'DESCRIPTIO',
    'perimeter': 'MULTIPOLYGON',
}

contour_mapping = {
    'contour': 'CONTOUR',
    'cont_id': 'ID',
    'calc_dep_m': 'CALC_DEP_M',
    'geom': 'MULTILINESTRING',
}

if __name__ == "__main__":
    run()
