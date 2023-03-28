#!/usr/bin/env python
# coding: utf-8



import geopandas as gpd
import numpy as np
from itertools import product
from shapely.geometry.polygon import Polygon
#import matplotlib.pyplot as plt

from pyproj import CRS
from pyproj.aoi import AreaOfInterest
from pyproj.database import query_utm_crs_info


def get_structure(poly, working_width=36,factor=2,tramline= None):

    edge_length=working_width*factor
    
    if factor % 2 == 0:
        parallel_shift=4 
    else:
        parallel_shift=2
    
        
    ##convert to epsg 4326
    poly= poly.to_crs('epsg:4326')
    
    ##find correct EPSG for calculation in meter
    utm_crs_list = query_utm_crs_info(datum_name="WGS 84",area_of_interest=AreaOfInterest(
                west_lon_degree=poly.bounds.values[0][0],
                south_lat_degree=poly.bounds.values[0][1],
                east_lon_degree=poly.bounds.values[0][2],
                north_lat_degree=poly.bounds.values[0][3]))
    
    
    EPSG = CRS.from_epsg(utm_crs_list[0].code)
    
    
    poly=poly.to_crs('{}'.format(EPSG))
    
    
    if tramline is None:
        p0=poly.bounds.values[0][0],poly.bounds.values[0][1]
        p1=poly.bounds.values[0][0],poly.bounds.values[0][1]+10
    else:
        tramline=tramline.to_crs('{}'.format(EPSG))
        p0 = tramline["geometry"][0].coords[0] # First coordinate of permanent traffic lane 
        p1 = tramline["geometry"][0].coords[1]
        
    
    ##get the right dimension for layout
    x_diff=poly.bounds.iloc[0][2]-poly.bounds.iloc[0][0]
    y_diff=poly.bounds.iloc[0][3]-poly.bounds.iloc[0][1]
    
    dimension=x_diff/edge_length,y_diff/edge_length
    dimension_a=(int(dimension[0]) + (dimension[0] % 5 > 0))*2#upround
    dimension_b=(int(dimension[1]) + (dimension[1] % 5 > 0))*2
    
    # Second coordinate of permanent traffic lane 
    dif = np.array(p0) - np.array(p1)  
    l = np.linalg.norm( dif)           
    ndif = dif / l                    
    q1 = ndif * edge_length              
    q2 = np.array((q1[1],-q1[0]))      

    polies = []
    so =np.array( p0 - q2/parallel_shift)                         
    for i,j in product(range(-dimension_a,dimension_a),range(-dimension_b,dimension_b)):  
        
        s = so + i * q1 + j * q2 
        p=Polygon([ s ,s+q2, s+(q1+q2), s+q1])
        polies +=[p]
    data = gpd.GeoDataFrame({'geometry':polies})
    data.crs = '{}'.format(EPSG)
    
    patches_within = gpd.sjoin(data,poly)
    
    patches_within=patches_within.to_crs('epsg:4326')
    
    return patches_within

