## About The Project
### Creating patch structures

For the production of application maps in agriculture, rectangular polygons are often used to distinguish subareas on the field. So far, these are always generated in north-south direction by conventional farm management softwares. However, the direction of travel on a field is very often different from the north-south orientation.
With this module, patch structures are generated parallel to the working direction. It is possible to define the maximum working width, as well as the maximum size of the polygons in the unit meter. If no tramline is provided, patch structures are created in the north-south direction.

### Link to academic papers
 This Project is part of our academic paper:
 
 ```
Donat, M., et al. (2022). "Patch cropping-a new methodological approach to determine new field arrangements
##that increase the multifunctionality of agricultural landscapes." Computers and Electronics in Agriculture 197: 106894.
 ```
 [https://doi.org/10.1016/j.compag.2022.106894](https://doi.org/10.1016/j.compag.2022.106894)
## Installation

You can install via pip:

```
$ pip install git+https://github.com/mardonat/patchmaps.git
```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started


Import the modul:
```
from patchmaps import patchmaps
```

Import the data using Geopandas
```
line = gpd.read_file('line.shp')
line= line.to_crs('epsg:4326')
poly = gpd.read_file('poly.shp')
poly= poly.to_crs('epsg:4326')
```

And then create patchmaps with and without a trameline:
```
patchmaps.get_structure(poly=poly,tramline=line, working_width=36,factor=2)
```

In this picture you can see the field polygon, the tramline and the generated patchstructure (parallel to tramline). By setting a working width of 36 m and the factor 2, rectangular patches with a total edge length of 72 m are generated.

<img src="https://github.com/mardonat/patchmaps/blob/main/tutorials/images/field_with_runline.PNG" width="900" height="700">


In this picture you can see the field polygon and the generated patchstructure (north-south orientation). By setting a working width of 36 m and the factor 2, rectangular patches with a total edge length of 72 m are generated.

<img src="https://github.com/mardonat/patchmaps/blob/main/tutorials/images/field_wo_runline.PNG" width="700" height="600">


<p align="right">(<a href="#readme-top">back to top</a>)</p>

## License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Marco Donat -  marco.donat@zalf.de

Project Link: [https://github.com/mardonat/patchmaps.git](https://github.com/mardonat/patchmaps.git)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
