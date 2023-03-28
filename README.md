# Creating patch structures oriented parallel to the permanent traffic line

For the production of application maps in agriculture, rectangular polygons are often used to distinguish subareas on the field. So far, these are always generated in north-south direction by conventional farm management systems. However, the direction of travel on a field is very often different from the north-south direction.
With this module, patch structures are generated parallel to the working direction. It is possible to define the maximum working width, as well as the maximum size of the polygons in the unit meter. 


Instalation

pip install git+https://github.com/mardonat/patchmaps.git


Use

##import modul
from patchmaps import patchmaps

##import data
line = gpd.read_file('line.shp')
line= line.to_crs('epsg:4326')
poly = gpd.read_file('poly.shp')
poly= poly.to_crs('epsg:4326')

##create patchmaps
patchmaps.get_structure(poly=poly,tramline=line, working_width=36,factor=2)
