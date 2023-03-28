## About The Project
### Creating patch structures oriented parallel to the permanent traffic line

For the production of application maps in agriculture, rectangular polygons are often used to distinguish subareas on the field. So far, these are always generated in north-south direction by conventional farm management softwares. However, the direction of travel on a field is very often different from the north-south orientation.
With this module, patch structures are generated parallel to the working direction. It is possible to define the maximum working width, as well as the maximum size of the polygons in the unit meter. If no tramline is provided, patch structures are created in the north-south direction.

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


![alt text](https://github.com/mardonat/patchmaps/blob/main/tutorials/images/field_with_runline.PNG? | width=20)


<p align="right">(<a href="#readme-top">back to top</a>)</p>

## License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Marco Donat -  marco.donat@zalf.de

Project Link: [https://github.com/mardonat/patchmaps.git](https://github.com/mardonat/patchmaps.git)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
