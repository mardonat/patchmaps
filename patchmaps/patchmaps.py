#!/usr/bin/env python
# coding: utf-8



import geopandas as gpd
import numpy as np
from itertools import product
from shapely.geometry.polygon import Polygon
from shapely.ops import transform

import pyproj
from pyproj import CRS
from pyproj.aoi import AreaOfInterest
from pyproj.database import query_utm_crs_info

import math

def get_structure(poly: Polygon, crs='epsg:4326', working_width=36, factor=2, tramline=None) -> gpd.GeoDataFrame:

    edge_length = working_width * factor
    if factor % 2 == 0:
        parallel_shift = 4
    else:
        parallel_shift = 2
   
    # input_crs = CRS.from_user_input(crs).name
    # find correct EPSG for calculation in meter
    utm_crs_list = query_utm_crs_info(datum_name="WGS 84", area_of_interest=AreaOfInterest(
        west_lon_degree=poly.bounds[0],
        south_lat_degree=poly.bounds[1],
        east_lon_degree=poly.bounds[2],
        north_lat_degree=poly.bounds[3]))
    utm = CRS.from_epsg(utm_crs_list[0].code)
    # to utm (meters) TODO verify this.
    project = pyproj.Transformer.from_crs(crs, utm, always_xy=True).transform
    poly = transform(project, poly)

    if tramline is None:
        p0 = poly.bounds[0], poly.bounds[1]
        p1 = poly.bounds[0], poly.bounds[1] + 10
    else:
        tramline = tramline.to_crs('{}'.format(utm))
        p0 = tramline["geometry"][0].coords[0]  # First coordinate of permanent traffic lane
        p1 = tramline["geometry"][0].coords[1]

    ##get the right dimension for layout
    x_diff = poly.bounds[2] - poly.bounds[0]
    y_diff = poly.bounds[3] - poly.bounds[1]

    dimension = x_diff / edge_length, y_diff / edge_length
    dimension_a = math.ceil((int(dimension[0]) + (dimension[0] % 5 > 0)) * 2)  # upround
    dimension_b = math.ceil((int(dimension[1]) + (dimension[1] % 5 > 0)) * 2)

    # Second coordinate of permanent traffic lane
    dif = np.array(p0) - np.array(p1)
    l = np.linalg.norm(dif)
    ndif = dif / l
    q1 = ndif * edge_length
    q2 = np.array((q1[1], -q1[0]))

    so = np.array(p0 - q2 / parallel_shift)
    def compute_poly(i, j):
        s = so + i * q1 + j * q2
        patch = Polygon([s, s + q2, s + (q1 + q2), s + q1])
        # if patch.intersection(poly):
        return patch
    polies = [compute_poly(i, j) for i, j in product(range(-dimension_a, dimension_a), range(-dimension_b, dimension_b))]
    data = gpd.GeoDataFrame({'geometry': polies})
    data.crs = '{}'.format(utm)

    # Alternatively use clip and clip to polygon
    patches_within = data.clip(poly, keep_geom_type=True)
    # patches_within = data[data.intersects(poly)]

    # transform back to original crs
    patches_within = patches_within.to_crs(crs)

    return patches_within
