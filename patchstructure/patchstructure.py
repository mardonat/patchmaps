#!/usr/bin/env python
# coding: utf-8

# In[8]:


import geopandas as gpd
import numpy as np
from itertools import product
from shapely.geometry.polygon import Polygon
import matplotlib.pyplot as plt

from pyproj import CRS
from pyproj.aoi import AreaOfInterest
from pyproj.database import query_utm_crs_info


# print('hallo')


def get_patchstructure(spur, grenzen, working_width=36,factor=2):

    edge_length=working_width*factor
    
    if factor % 2 == 0:
        parallel_shift=4 
    else:
        parallel_shift=2
    
    ##find correct EPSG
    utm_crs_list = query_utm_crs_info(datum_name="WGS 84",area_of_interest=AreaOfInterest(
                west_lon_degree=grenzen.bounds.values[0][0],
                south_lat_degree=grenzen.bounds.values[0][1],
                east_lon_degree=grenzen.bounds.values[0][2],
                north_lat_degree=grenzen.bounds.values[0][3]))
    EPSG = CRS.from_epsg(utm_crs_list[0].code)
    print(EPSG)
    spur=spur.to_crs('{}'.format(EPSG))
    grenzen=grenzen.to_crs('{}'.format(EPSG))
        
    ##get the right dimension for layout
    x_diff=grenzen.bounds.iloc[0][2]-grenzen.bounds.iloc[0][0]
    y_diff=grenzen.bounds.iloc[0][3]-grenzen.bounds.iloc[0][1]
    
    dimension=x_diff/edge_length,y_diff/edge_length
    dimension_a=(int(dimension[0]) + (dimension[0] % 5 > 0))*2#upround
    dimension_b=(int(dimension[1]) + (dimension[1] % 5 > 0))*2
    
    p0 = spur["geometry"][0].coords[0] # First coordinate of permanent traffic lane 
    p1 = spur["geometry"][0].coords[1] # Second coordinate of permanent traffic lane 
    dif = np.array(p0) - np.array(p1)  # Differnez zwíschen den Startpunkten berechnen (Längen der Kanten eines Rechteckes)
    l = np.linalg.norm( dif)           # Länge der Leiutspur
    ndif = dif / l                     # Verhältnisse berechnen, für x m auf einer schrägen, muss q1[0] von y abgezogen werden und q1[1] von x
    q1 = ndif * edge_length                   # berechnen der konkreten werte "x" zur Erstellung eines Gitters für 72 m Patchlänge
    q2 = np.array((q1[1],-q1[0]))      # berechnen der konkreten werte "y" zur Erstellung eines Gitters für 72 m Patchlänge

    polies = []
    so =np.array( p0 - q2/parallel_shift)                         # parallel shift; /2 =Half; /4= quater
    for i,j in product(range(-dimension_a,dimension_a),range(-dimension_b,dimension_b)):  
        
        s = so + i * q1 + j * q2 
        p=Polygon([ s ,s+q2, s+(q1+q2), s+q1])
        polies +=[p]
    data = gpd.GeoDataFrame({'geometry':polies})
    data.crs = '{}'.format(EPSG)
    
    patches_within = gpd.sjoin(data,grenzen)
    
    patches_within=patches_within.to_crs('epsg:4326')
    
    return patches_within

