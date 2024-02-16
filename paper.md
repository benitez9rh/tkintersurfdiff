---
title: 'Calculate difference between point clouds representing two surfaces: a Tkinter Graphical User Interface Python code'
tags:
  - python
  - tkinter
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

## 1. Summary

In academic research, as well as in many other industrial applications, there is the need for calculating the distance between points. This is normally a trivial exercise for point-to-point calculation. In particular situations such as error maps however, the inputs are generally point clouds instead of single points. To complicate matters, often these points are not aligned in the dimension of interest, hence a simple arithmetic calculation is not possible. This work elaborates on an approach used to calculate the distance between two point clouds applied to a real-life research and industrial application: Calculating the error or difference map between two point clouds representing two surfaces.

![Gridded Surfaces from point clouds.\label{fig:TopBottomVExag10}](Figures/TopBottomVExag10.png)

\autoref{fig:TopBottomVExag10} * - Gridded Surfaces from point clouds.*

## 2. Statement of need

Open fractures in rocks facilitate the flow of fluids compared to the porous rock body [@McDermott2015; @McCraw2016], especially in rocks with relatively impermeable rocks. Each fracture face roughness distribution contributes to the distribution of space between the two faces, or aperture of the fracture. The aperture distribution of a fracture is one of the main factors for permeability increase through that fracture. To calculate the aperture spatial distribution between two fracture surfaces, or likewise the error map between two surfaces, the vertical difference between these surfaces needs to be calculates. The input point clouds seldom have matching (x, y) coordinates which would allow simple point-to-point attribute difference (z-coordinate in this example). Therefore, gridding of the point clouds is necessary for interpolation between the input points allowing the calculation of intersection points at the (x, y, attribute) of one of the surfaces directly above or below the other.
PyVista's package [@SullivanKaszynski2019] allows for much of the modelling required in this exercise but only offers the projection of the normals of the gridded surface cells thus lacking the projection in the vertical direction.

In this paper, we introduce a Python code allowing for the calculation of two point clouds' difference in the vertical direction wrapped in a simple and easy-to-use GUI, streamlining the experience of browsing the computer system for the input files and eliminating the need to code.


