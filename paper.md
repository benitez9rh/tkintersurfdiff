---
title: 'Calculate difference between point clouds representing two surfaces: a Tkinter Graphical User Interface Python code'

tags:
  - Python
  - Tkinter GUI
  - Geometry
  - Rock fractures
  - Surface difference
  - Error

authors:
 - name: Gonçalo Benitez Cunha
   orcid: 0009-0007-5441-3790
   affiliation: "1"
   
affiliations:
 - name: The University of Edinburgh, Edinburgh, Scotland, United Kingdom
   index: 1

date: 16 February 2024
bibliography: paper.bib

---

## Summary

In academic research, as well as in many other industrial applications, there is the need for calculating the distance between points. This is normally a trivial exercise for point-to-point calculation. In particular situations such as error maps however, the inputs are generally point clouds instead of single points. To complicate matters, often these points are not aligned in the dimension of interest, hence a simple arithmetic calculation is not possible. This work elaborates on an approach used to calculate the distance between two point clouds applied to a real-life research and industrial application: Calculating the error or difference map between two point clouds representing two surfaces. It further wraps it in a Graphical User Interface (GUI) to streamline the browsing process and the identification of  the input parameters for the user, hence eliminating thee need to code.

![Gridded Surfaces from point clouds.\label{fig:TopBottomVExag10}](Figures/TopBottomVExag10.png)


## Statement of need

Open fractures in rocks facilitate the flow of fluids compared to the porous rock body [@McDermott2015; @McCraw2016], especially in rocks with relatively impermeable rocks. Each fracture face roughness distribution contributes to the distribution of space between the two faces, or aperture of the fracture. The aperture distribution of a fracture is one of the main factors for permeability increase through that fracture. To calculate the aperture spatial distribution between two fracture surfaces, or likewise the error map between two surfaces, the vertical difference between these surfaces needs to be calculated. The input point clouds seldom have matching (x, y) coordinates which would allow simple point-to-point attribute difference (z-coordinate in this example). Therefore, gridding of the point clouds is necessary for interpolation between the input points allowing the calculation of intersection points at the (x, y, attribute) of one of the surfaces directly above or below the other.
PyVista's package [@SullivanKaszynski2019] allows for much of the modelling required in this exercise but only offers the projection of the normals of the gridded surface cells thus lacking the projection in the vertical direction.

In this paper, we introduce a Python code allowing for the calculation of two point clouds' difference in the vertical direction wrapped in a simple and easy-to-use tkinter [@Lundh1999] GUI, streamlining the experience of browsing the computer system for the input files and eliminating the need to code.


## Acknowledgements

This work was possible due to the sponsorship of Quintessa, the School of Geosciences at the The University of Edinburgh and Nuclear Waste Services, part of the Nuclear Decommissioning Authority in the United Kingdom. Acknowledgement must also be made to Dr. Roberto Rizzo for his guidance, support and motivation into publishing my code. 
Various other Python [@VanRossum1995] packages are used including Pandas [@McKinney2010], Numpy [@Harris2020], Scipy [@Virtanen2020], Scikit-Learn [@Pedregosa2011] and Matplotlib [@Hunter2007].
Other smaller and non-published code contributions used are cited and acknowledged accordingly as comments and/or links in the code.


## References

