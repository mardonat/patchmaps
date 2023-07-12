## About The Project
### Creating patch structures

For the generation of application maps in agriculture, rectangular polygons are often used to distinguish subareas on the field. So far, these are always generated in north-south direction by conventional farm management softwares. However, the direction of travel on a field is very often different from the north-south orientation.
With this module, patch structures are generated parallel to the working direction. It is possible to define the maximum working width, as well as the maximum size of the polygons in the unit meter. If no tramline is provided, patch structures are created in the north-south direction.

### Link to academic paper

 This Project is part of our academic paper:
 
 ```
Donat, M., et al. (2022). "Patch cropping-a new methodological approach to determine new field arrangements
that increase the multifunctionality of agricultural landscapes." 
Computers and Electronics in Agriculture 197: 106894.
 ```
 [DOI:10.1016/j.compag.2022.106894](https://doi.org/10.1016/j.compag.2022.106894)
## Installation

You can install via pip:

```
pip install git+https://github.com/mardonat/patchmaps.git
```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started


Import the modul:
```
from patchmaps import patchmaps
```

Import the data using Geopandas
```
[1] line = gpd.read_file('line.shp')
[2] line= line.to_crs('epsg:4326')
[3] gdf = gpd.read_file('poly.shp')
[4] gdf= poly.to_crs('epsg:4326')
```
Type(poly) has to be a shapely.geometry.polygon.Polygon:
```
[1] poly=poly.iloc[0].geometry
[2] print(type(poly)==shapely.geometry.polygon.Polygon)
[3] True
```

And then create patchmaps with and without a trameline. Working_width is the maximum working width you use (e.g 36m). Patchmaps will have a edge length of the working width. With the parameter factor you can increase the patch size by a multiple of your working width. If you use a working width of 36 m and a factor of 1, patches will have a edge length of 36m. If you use working width of 36 m and factor 2, patches will have a edge length of 72m (36m*2m). 
```
patchmaps.get_structure(poly=poly,tramline=line, working_width=36,factor=2)
```

In this picture you can see the field polygon, the tramline and the generated patchstructure (parallel to tramline). By setting a working width of 36 m and the factor 2, rectangular patches with a total edge length of 72 m are generated.

<img src="https://github.com/mardonat/patchmaps/blob/main/tutorials/images/field_with_runline.PNG" width="900" height="700">


In this picture you can see the field polygon and the generated patchstructure (north-south orientation). By setting a working width of 36 m and the factor 2, rectangular patches with a total edge length of 72 m are generated.

<img src="https://github.com/mardonat/patchmaps/blob/main/tutorials/images/field_wo_runline.PNG" width="700" height="600">


<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Test data

Test data can be found in the [tutorial folder](https://github.com/mardonat/patchmaps/tree/main/tutorials). Different fields and tramlines are provided in different countries around the world to test the creation of patchmaps.


## License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Marco Donat -  marco.donat@zalf.de

Project Link: [https://github.com/mardonat/patchmaps.git](https://github.com/mardonat/patchmaps.git)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

