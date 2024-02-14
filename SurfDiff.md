# Calculate difference between point clouds representing two surfaces: a Tkinter Graphical User Interface Python code

Gonçalo Benitez Cunha<sup>1</sup>

<sup>1</sup>The University of Edinburgh, Scotland, United Kingdom

Corresponding author: Gonçalo Cunha ([g.cunha@ed.ac.uk](g.cunha@ed.ac.uk))


## 1. Summary

In academic research, as well as in many other industrial applications, there is the need for calculating the distance between points. This is normally a trivial exercise for point-to-point calculation. However, it complicates when the inputs are point clouds instead of single points and even further when these points are not aligned in the dimension of interest, hence a simple arithmetic or trigonometric calculation is not possible. This work elaborates on an approach used to calculate the distance between two point clouds applied to a real-life research application: Calculating the aperture and permeability fields between two surfaces of a rock fracture for Finite Element Method (FEM) numerical modelling.
This calculation is facilitated by a Python-based Graphical User Interface (GUI) which maps the calculated aperture distribution onto a mesh intended for FEM numerical modelling.
Open fractures in rocks facilitate the flow of fluids compared to the porous rock body [REFERENCES], especially in rocks with relatively impermeable rocks. Each fracture face roughness distribution contributes to the distribution of space between the two faces, or aperture of the fracture. The aperture distribution of a fracture is one of the main drivers for permeability of fluids through that fracture.
Fluid flow numerical simulations through fractures rely on representations of fracture aperture fields. Building the models for performing these simulations generally require upscaling of the fracture of aperture field or, as in (McDermott, et al., 2015), the usage of a specific resolution. Particularly when upscaling, averaging is used, which neglects the spatial continuity of the data.
In this paper, we introduce the method of upscaling a Freiberg gneiss’ single rough fracture aperture field using its spatial continuity through a kriging algorithm. The method is then tested by comparing the two methods (arithmetic averaging and kriging) in two different sized meshes in a finite element method (FEM) coupled hydro-mechanical model.
The objective of this study was to utilise a spatial description technique such as the variogram analysis to inform a kriging algorithm in order to better predict the upscaled value of the elements in coupled THMC processes numerical models. In order to assess if this technique was suitable, a comparison was made between fine and coarse models with aperture averaging and kriging using the spatial continuity of the aperture field.


## 2. Statement of need

The reality.


## 3. Methodology

In this section I describe the approach for calculating the difference between two surfaces composed of cloud points which is subsequently mapped onto a mesh of quadrilateral elements, using arithmetic averaging or kriging.
Both the red and blue surfaces in Figure 1 are gridded from individual point clouds using PyVista’s (Sullivan & Kaszynski, 2019)  package’s 2D Delaunay triangulation method. Each high or low in these surfaces corresponds to a point from the input point cloud. The surfaces correspond to two topographical surfaces represented with 10x vertical exaggeration. PyVista does have the option to measure this space normally to the surface’s cells, but not vertically. Therefore, the code hereby presentedcomputes the space between the two surfaces measured vertically along the z-axis at the resolution of the point clouds.
![Figure 1 - Top (red) and bottom (blue) surfaces gridded from points clouds using PyVista’s 2D Delaunay triangulation (Sullivan & Kaszynski, 2019). Five (5)a times vertical exaggeration.](https://github.com/benitez9rh/tkintersurfdiff/blob/main/GWTopBottomVExag10.png)
*Top (red) and bottom (blue) surfaces gridded from points clouds using PyVista’s 2D Delaunay triangulation (Sullivan & Kaszynski, 2019). Five (5)a times vertical exaggeration.*

Due to the fact that the point clouds could be in an unordered/unstructured state and that the two point clouds might (most likely in fact) not share the same XY locations, in which case a simple z-difference would suffice, new points at the same XY locations at the level of the second surface must be created. To accomplish this, one of the surfaces is gridded using a Delaunay triangulation which in effect interpolates 3 points in a continuum. Then, each point of the second cloup point is projected towards the gridded surface and the intersection of that line with the gridded surface creates the point needed at the same XY location. After, a simple z-difference can be calculated. This exercise is illustrated in Figure 2 below. The bottom surface’s points are then projected up towards the gridedd top surface to calculate the intersection points making the z-difference calculation possible. Note that the projections are done in both directions in case the bottom surface has points crossing the gridded top surface, as in the case on the left, rendering a negative space. This is accounted for in the code.
![Figure 2 - Representation of the difference calculation between surfaces. The bottom surface (not gridded) points’ (blue) are projected vertically along the z-axis until they cross the top surface (grided). The difference between the bottom surface’s points (blue) and the intersection points (purple) is calculated. The projections are done in both directions in case the gridded surface is below, which renders a negative distance (case on the left).](https://github.com/benitez9rh/tkintersurfdiff/blob/main/ApertureCalculation.png)
*Representation of the difference calculation between surfaces. The bottom surface (not gridded) points’ (blue) are projected vertically along the z-axis until they cross the top surface (grided). The difference between the bottom surface’s points (blue) and the intersection points (purple) is calculated. The projections are done in both directions in case the gridded surface is below, which renders a negative distance (case on the left).*


### 3.1 Data

The data required needs to be in a format that is readable by thePython Pandas package, such as tab delimited .txt or .csv files, and they must contain the required XYZ spatial information.
Below an example of the format required:

```
Index	X	Y	Z
0	-43.78	12.89	52.3
1	102.56	-28.6	10.51
...
N	Xn	Yn	Zn
```

The output is a file of the same format (tab delimited) with .txt extension containing the exact same XY locations as the bottom surface in the first two columns as well as the differences in the third column.
