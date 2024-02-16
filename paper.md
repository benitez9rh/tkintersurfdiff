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

In academic research, as well as in many other industrial applications, there is the need for calculating the distance between points. This is normally a trivial exercise for point-to-point calculation. However, it complicates when the inputs are point clouds instead of single points and even further when these points are not aligned in the dimension of interest, hence a simple arithmetic or trigonometric calculation is not possible. This work elaborates on an approach used to calculate the distance between two point clouds applied to a real-life research application: Calculating the error or difference map between two point clouds representing two surfaces.
This calculation is facilitated by a Python-based Graphical User Interface (GUI). The GUI allows a user-friendly system navigation to browse the necessary input files. The code in the background calculates the error map on a point by point basis (from the bottom surface to the top surface grid) at the click of a button.
Open fractures in rocks facilitate the flow of fluids compared to the porous rock body [REFERENCES], especially in rocks with relatively impermeable rocks. Each fracture face roughness distribution contributes to the distribution of space between the two faces, or aperture of the fracture. The aperture distribution of a fracture is one of the main drivers for permeability of fluids through that fracture.
Fluid flow numerical simulations through fractures rely on representations of fracture aperture fields. Building the models for performing these simulations generally require upscaling of the fracture of aperture field or, as in (McDermott, et al., 2015), the usage of a specific resolution. Particularly when upscaling, averaging is used, which neglects the spatial continuity of the data.
In this paper, we introduce the method of upscaling a Freiberg gneiss’ single rough fracture aperture field using its spatial continuity through a kriging algorithm. The method is then tested by comparing the two methods (arithmetic averaging and kriging) in two different sized meshes in a finite element method (FEM) coupled hydro-mechanical model.
The objective of this study was to utilise a spatial description technique such as the variogram analysis to inform a kriging algorithm in order to better predict the upscaled value of the elements in coupled THMC processes numerical models. In order to assess if this technique was suitable, a comparison was made between fine and coarse models with aperture averaging and kriging using the spatial continuity of the aperture field.

![Error Calculation Method. \label{fig:TopBottomVExag10}](Figures/TopBottomVExag10.png)

\autoref{fig:TopBottomVExag10}

## 2. Statement of need

The reality.

