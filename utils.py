import string
from unidecode import unidecode
from shapely.geometry import shape

def str_wo_space(x):
    return  unidecode(x.translate(str.maketrans('', '', string.punctuation)).replace(' ', '-'))

from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="geoapiExercises")

def localisation(geometry):
    centroid = shape(geometry).centroid 
    Latitude = str(centroid.y)
    Longitude = str(centroid.x)
    location = geolocator.reverse(Latitude+","+Longitude)
    dict_loc = location.raw['address']
    keys = [x for x in ['country_code', 'state', 'county', 'city'] if x in dict_loc.keys()]
    name = '-'.join([ str_wo_space(dict_loc[key]) for key in keys])
    return name, Latitude, Longitude

from OSMPythonTools.nominatim import Nominatim
from shapely import wkt
from rasterio.warp import transform_geom
from shapely.geometry import shape

def get_polygon(name, epsg):
    finder = Nominatim()
    spatial_entity = finder.query(name, wkt=True)
    pol = wkt.loads(spatial_entity.wkt())
    pol_ = shape(transform_geom('EPSG:4326', epsg, pol))
    return pol_, spatial_entity

from shapely.geometry import Point
import random
random.seed()

def get_bounding_box(row, gdf):
    aoi = Point(row.geometry.centroid.x, row.geometry.centroid.y).buffer(4750, cap_style=3)
    neighbors = gdf.clip(aoi)
    neighbors = neighbors.append(row)

    return neighbors, aoi

def get_random_bounding_box(gdf, gdf_ref):
    random_row = random.choice(gdf_ref.index.tolist())
    row = gdf_ref.loc[[random_row]]
    return get_bounding_box(row, gdf)

def compute_IoU(bounds1, bounds2):
    if bounds1.intersects(bounds2):
        IoU = bounds1.intersection(bounds2).area / bounds1.union(bounds2).area
    else: 
        IoU = 0
        
    return IoU