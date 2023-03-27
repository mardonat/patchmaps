#!/usr/bin/env python
# coding: utf-8


import geopandas as gpd
import numpy as np
from itertools import product
from shapely.geometry.polygon import Polygon
from pyproj import CRS
from pyproj.aoi import AreaOfInterest
from pyproj.database import query_utm_crs_info


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
    
    spur=spur.to_crs('{}'.format(EPSG))
    grenzen=grenzen.to_crs('{}'.format(EPSG))
        
    ##get the right dimension for layout
    x_diff=grenzen.bounds.iloc[0][2]-grenzen.bounds.iloc[0][0]
    y_diff=grenzen.bounds.iloc[0][3]-grenzen.bounds.iloc[0][1]
    
    dimension=x_diff/edge_length,y_diff/edge_length
    dimension_a=(int(dimension[0]) + (dimension[0] % 5 > 0))*2
    dimension_b=(int(dimension[1]) + (dimension[1] % 5 > 0))*2
    
    p0 = spur["geometry"][0].coords[0] 
    p1 = spur["geometry"][0].coords[1] 
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
    
    patches_within = gpd.sjoin(data,grenzen)
    
    patches_within=patches_within.to_crs('epsg:4326')
    
    return patches_within

