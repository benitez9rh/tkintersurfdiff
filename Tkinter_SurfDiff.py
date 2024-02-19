# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 11:46:02 2023
@author: s2132627
"""


"""
This script takes two .csv or .txt tab-delimited files of points clouds (with spatial XY information) and calculates the vertical (along the z-axis) space between the two. 
It does this by gridding the top surface first to create and interpolating continuum between points. The point cloud corresponding from the bottom surface is then projected towards the top surface and intesection points with the grid are created.
The differences are theen calculated.
Note the point clouds' points don't need toe share the same exact XY locations but the clouds need to be above/below each othert in order to have intersections with the projection lines.

Below is an example of the .csv file format required.

x	y	aperture	avg	var	std
-22.5	-32.5	0.49977896	0.515901725	0.005059804	0.071132302
-22.5	-31.5	0.48803121	0.508111098	0.004592228	0.067765978         
...     ...     ...         ...         ...         ...

"""
import os
import pathlib
import sys
from tkinter import *               #Import everything from Tkinter
from tkinter import ttk
import tkinter.messagebox           #Import messagebox method
from tkinter import filedialog
from time import time, ctime
import time
import pandas as pd
from numpy import *
import numpy as np
from ast import literal_eval
from scipy.spatial import KDTree
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib import cm
import csv
from sklearn.metrics import r2_score
import pyvista as pv
from pyvista import examples

'''User Defined Global Variables'''
output_extension = ".txt"
xdens = 0.5 # density of 0.1 causes error: MemoryError: Unable to allocate 64.9 GiB for an array with shape (952300, 9152) and data type float64
ydens = 0.5
zexag = 0 # vertical exageration (%)
auto_centre = True
save = True

"""System Variables"""
cmap = plt.cm.plasma                    # color map
extension_xyz = ".xyz"
extension_csv = ".csv"
extension_png = ".png"
extension_txt = ".txt"

'''Tkinter Variables'''
root = Tk()
BROWSE_frame = LabelFrame(root, text = "Browse Frame")
BROWSE_frame.grid(row = 1, column = 1, columnspan = 3, sticky = EW, pady = 10, padx = 10)
CSV_frame1 = LabelFrame(root, highlightbackground="black", highlightthickness=1)
CSV_frame1.grid(row = 3, column = 1, pady = 20, padx = 10)
CSV_frame2 = LabelFrame(root, highlightbackground="black", highlightthickness=1)
CSV_frame2.grid(row = 3, column = 2, pady = 20, padx = 10)

'''Methods'''
def simplest_type(s): # ast 's literal_eval converts numericals to their appropriate type. Say you have "2" and "3.14" strings, they will be converted to int and float respectively. The issue is that it breaks when it sees an actual string, thus this simplest_type function. # From https://stackoverflow.com/questions/60213604/automatically-convert-string-to-appropriate-type
    try:
        return literal_eval(s)
    except:
        return s
class MidpointNormalize(colors.Normalize):
	"""
	Normalise the colorbar so that diverging bars work there way either side from a prescribed midpoint value)
	e.g. im=ax1.imshow(array, norm=MidpointNormalize(midpoint=0.,vmin=-100, vmax=100))
    # set the colormap and centre the colorbar. Thanks to http://chris35wills.github.io/matplotlib_diverging_colorbar/
	"""
	def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
		self.midpoint = midpoint
		colors.Normalize.__init__(self, vmin, vmax, clip)
	def __call__(self, value, clip=None):
		# I'm ignoring masked values and all kinds of edge cases to make a
		# simple example...
		x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
		return np.ma.masked_array(np.interp(value, x, y), np.isnan(value))

'''Tkinter Methods'''
def description():
    tkinter.messagebox.showinfo(title = "Description", message = " Simply use the 'Browse' button to browse to the input .CSV files containing the spatial information of the point clouds.\n\n Then click 'Create difference .txt file', or alternatively 'File' > 'Create difference .txt file' and a new file will be created in the same directory with the difference between the surfaces. \
                                                                 \n\nOnce both files are browsed, the contents can be visualised in the corresponding visualisation windows. \
                                                                     \n\nFor each of the .csv files type the row corresponding to the header, the rows to ignore (separated by commas) and the columns to read corresponding to the X,Y and Z spatial information.")
def browseCSV2():
    root.CSVinputfilepath2 = filedialog.askopenfilename(initialdir="C://Desktop/", title = "Select a file", filetypes = ((".csv files","*.csv"), (".txt files", "*.txt"), ("All files", "*.*") ))
    CSV_Text2.delete(0.0, END)
    CSV_Text2.insert(0.0, root.CSVinputfilepath2)
    CSVinputfilename2 = root.CSVinputfilepath2[root.CSVinputfilepath2.rfind("/")+1:]
    pathCSV2 = root.CSVinputfilepath2[:root.CSVinputfilepath2.rfind("/")+1]
    CSVinput_extension2 = root.CSVinputfilepath2[root.CSVinputfilepath2.rfind("."):]
    try:
        f = open(root.CSVinputfilepath2, 'r')
    except:
        tkinter.messagebox.showerror(title = "Error", message = "File not found or path is incorrect")
    finally:
        input_CSVfile2 = open(root.CSVinputfilepath2, 'r')
        # read the content of the file line by line 
        CSVdata_input2 = input_CSVfile2.readlines()
        #Submit input file's contents(.CSV) onto the respective text box for review by the user
        CSV_file_Text2.delete(0.0, END)
        CSV_file_Text2.insert(0.0, CSVdata_input2)
def browseCSV1():
    root.CSVinputfilepath1 = filedialog.askopenfilename(initialdir="C://Desktop/", title = "Select a file", filetypes = ((".csv files","*.csv"), (".txt files", "*.txt"), ("All files", "*.*") ))
    CSV_Text1.delete(0.0, END)
    CSV_Text1.insert(0.0, root.CSVinputfilepath1)
    CSVinputfilename1 = root.CSVinputfilepath1[root.CSVinputfilepath1.rfind("/")+1:]
    pathCSV1 = root.CSVinputfilepath1[:root.CSVinputfilepath1.rfind("/")+1]
    CSVinput_extension1 = root.CSVinputfilepath1[root.CSVinputfilepath1.rfind("."):]
    try:
        f = open(root.CSVinputfilepath1, 'r')
    except:
        tkinter.messagebox.showerror(title = "Error", message = "File not found or path is incorrect")
    finally:
        input_CSVfile1 = open(root.CSVinputfilepath1, 'r')
        # read the content of the file line by line 
        CSVdata_input1 = input_CSVfile1.readlines()
        #Submit input file's contents(.CSV) onto the respective text box for review by the user
        CSV_file_Text1.delete(0.0, END)
        CSV_file_Text1.insert(0.0, CSVdata_input1)

def createDifference():
    
    CSVinputfilename1 = root.CSVinputfilepath1[root.CSVinputfilepath1.rfind("/")+1:root.CSVinputfilepath1.rfind(".")]
    pathCSV1 = root.CSVinputfilepath1[:root.CSVinputfilepath1.rfind("/")+1]
    CSVinput_extension1 = root.CSVinputfilepath1[root.CSVinputfilepath1.rfind("."):]
    savewd = pathCSV1
    
    CSVinputfilename2 = root.CSVinputfilepath2[root.CSVinputfilepath2.rfind("/")+1:root.CSVinputfilepath2.rfind(".")]
    pathCSV2 = root.CSVinputfilepath2[:root.CSVinputfilepath2.rfind("/")+1]
    CSVinput_extension2 = root.CSVinputfilepath2[root.CSVinputfilepath2.rfind("."):]
    
    try:
        # path = root.inputfilepath[:root.inputfilepath.rfind("/")+1]
        header1 = int(header_Entry1.get())
        readcols1 = [int(i) for i in readcols_Entry1.get().split(",")]
        skiprows1 = [i for i in skiprows_Entry1.get().split(",")]
        header2 = int(header_Entry2.get())
        readcols2 = [int(i) for i in readcols_Entry2.get().split(",")]
        skiprows2 = [i for i in skiprows_Entry2.get().split(",")]
        fringe_aperture = simplest_type(fringeaperture_Entry.get())
        '''Global Variables'''
        
        if "" in skiprows1:
            df1 = pd.read_csv(pathCSV1 + CSVinputfilename1 + CSVinput_extension1, usecols = readcols1, header = header1)
        else:
            skiprows = [simplest_type(i) for i in skiprows]
            df1 = pd.read_csv(pathCSV1 + CSVinputfilename1 + CSVinput_extension1, usecols = readcols1, header = header1, skiprows = skiprows1)           #  
        if "" in skiprows2:
            df2 = pd.read_csv(pathCSV2 + CSVinputfilename2 + CSVinput_extension2, usecols = readcols2, header = header2)
        else:
            skiprows = [simplest_type(i) for i in skiprows]
            df2 = pd.read_csv(pathCSV2 + CSVinputfilename2 + CSVinput_extension2, usecols = readcols2, header = header2, skiprows = skiprows2)
    except:
        tkinter.messagebox.showerror(title = "Error", message = "There was an error reading the input file.\nThe most likely reason is that the file does not conform with the required format.\n\nMake sure the file has only 3 columns (x, y and aperture, respectively) and a header on row 1.")
    finally:
        if "" in skiprows1:
            df1 = pd.read_csv(pathCSV1 + CSVinputfilename1 + CSVinput_extension1, usecols = readcols1, header = header1)
        else:
            skiprows = [int(i) for i in skiprows]
            df1 = pd.read_csv(pathCSV1 + CSVinputfilename1 + CSVinput_extension1, usecols = readcols1, header = header1, skiprows = skiprows1)
        if "" in skiprows2:
            df2 = pd.read_csv(pathCSV2 + CSVinputfilename2 + CSVinput_extension2, usecols = readcols2, header = header2)
        else:
            skiprows = [int(i) for i in skiprows]
            df2 = pd.read_csv(pathCSV2 + CSVinputfilename2 + CSVinput_extension2, usecols = readcols2, header = header2, skiprows = skiprows2)
        
        dfcolnames1 = df1.columns
        xcol1, ycol1, vcol1 = dfcolnames1
        dfcolnames2 = df2.columns
        xcol2, ycol2, vcol2 = dfcolnames2
        stats=df1.describe().transpose(); xmin1 = stats['min'][xcol1]; xmax1 = stats['max'][xcol1]; ymin1 = stats['min'][ycol1]; ymax1 = stats['max'][ycol1];
        vmin1 = stats['min'][vcol1]; vmax1 = stats['max'][vcol1]; # nvmin = stats['min']['N'+vcol]; nvmax = stats['max']['N'+vcol]
        stats=df2.describe().transpose(); xmin2 = stats['min'][xcol2]; xmax2 = stats['max'][xcol2]; ymin2 = stats['min'][ycol2]; ymax2 = stats['max'][ycol2];
        vmin2 = stats['min'][vcol2]; vmax2 = stats['max'][vcol2]; # nvmin = stats['min']['N'+vcol]; nvmax = stats['max']['N'+vcol]
        df1 = df1[[xcol1, ycol1, vcol1]] # Filter DataFrame to only the necessary columns
        df2 = df2[[xcol2, ycol2,vcol2]] # Filter DataFrame to only the necessary columns

        if auto_centre == True:
            df1_xctr = df1['x'].mean()                  # Translating s1 upscaled points to XY area of s2 by finding s2 centre of gravity and add/subtract centre of gravity XY coordinates to the s1 upscaled points
            df1_yctr = df1['y'].mean()
            df2_xctr = df2['x'].mean()            # Translating s1 upscaled points to XY area of s2 by finding s2 centre of gravity and add/subtract centre of gravity XY coordinates to the s1 upscaled points
            df2_yctr = df2['y'].mean()
            ctr_xdiff = (df1_xctr - df2_xctr )
            ctr_ydiff = (df1_yctr - df2_yctr )  
            df2['x'] = df2['x'] + ctr_xdiff
            df2['y'] = df2['y'] + ctr_ydiff
        
        gridx = np.arange(xmin1, xmax1, xdens)
        gridy = np.arange(ymax1, ymin1, -1*ydens)
        arr1 = df1.to_numpy(); #arr1 = arr1[:,1:] # gets rid of first column
        arr2 = df2.to_numpy(); # arr2  = arr2[:,1:] # gets rid of first column
        arr1 = arr1[~np.isnan(arr1).any(axis=1)]   # Removes all rows with NaNs but keeps the shape of the initial array https://stackoverflow.com/questions/11620914/how-do-i-remove-nan-values-from-a-numpy-array
        arr2 = arr2[~np.isnan(arr2).any(axis=1)]
        
        """ Creating the PolyData """
        df1cloud = pv.PolyData(arr1)
        df2cloud = pv.PolyData(arr2)
        
        """ Create triangulated surfaces """
        Surf_1 = df1cloud.delaunay_2d()
        Surf_2 = df2cloud.delaunay_2d()
        
        diff = np.zeros(Surf_2.n_points)
        Surf_2_verticals = np.zeros((Surf_2.n_points,3))
        Surf_1_verticals = np.zeros((Surf_2.n_points,3))
        for i in range(Surf_2.n_points):
            if i%10_000 ==0:                                  # Track the progress
                print('Surf_2.n_points loop: ' + str(i) + "/" + str(Surf_2.n_points) + ' ' + ctime())
            p = Surf_2.points[i]
            intersect, cell = Surf_1.ray_trace(p , [p[0],p[1], 9999], first_point=True)
            if intersect.size != 0:
                if intersect.size == 3:
                    intersectz = intersect[2]
                    pz = p[2]
                dist = np.sqrt(np.sum((intersectz - pz) ** 2))
                Surf_1_verticals[i] = intersect
                Surf_2_verticals[i] = p
            else:
                intersect, cell = Surf_1.ray_trace(p , [p[0],p[1], -9999], first_point=True)
                if intersect.size != 0:
                    if intersect.size == 3:
                        intersectz = intersect[2]
                        pz = p[2]
                    dist = np.sqrt(np.sum((intersectz - pz) ** 2))
                    Surf_1_verticals[i] = intersect
                    Surf_2_verticals[i] = p
                elif intersect.size == 0:
                    dist = np.nan
                    Surf_1_verticals[i] = np.nan
                    Surf_2_verticals[i] = np.nan
            diff[i] = dist
        
        x = Surf_2.points[:,0].T; x = x[~np.isnan(diff)]        # Remove indexes where diff contains NaNs, i.e., all non-intersections
        y = Surf_2.points[:,1].T; y = y[~np.isnan(diff)]        # Remove indexes where diff contains NaNs, i.e., all non-intersections
        Surf_1_verticals = Surf_1_verticals[~np.isnan(diff)]    # Remove indexes where diff contains NaNs, i.e., all non-intersections
        Surf_2_verticals = Surf_2_verticals[~np.isnan(diff)]    # Remove indexes where diff contains NaNs, i.e., all non-intersections
        diff = diff[~np.isnan(diff)]                            # Remove indexes containing NaNs, i.e., all non-intersections
    
        r2 = 1 - np.sum(diff) / np.sum(np.array([(i-Surf_1_verticals[:,2].mean())**2 for i in Surf_1_verticals[:,2]]) ) # r2 = 1 - ( SSres / SStotal):           SumSquares of residuals = sum of (observed - predicted)**2.        SumSquares total = sum of (observed - observed mean)**2.
        
        DiffMap = pd.DataFrame(np.vstack((np.array(x).flatten(), np.array(y).flatten(), diff)).transpose(), columns = [xcol1, ycol1, "DiffMap"]).drop_duplicates()
        if save == True:
            DiffMap.to_csv(f"{savewd}{CSVinputfilename1}_vs_{CSVinputfilename2}_DiffMap{extension_csv}")
            
        """ Difference Map """
        if amin(DiffMap['DiffMap'])<0:
            cmap = plt.cm.seismic                    # color map
            plt.scatter(DiffMap['x'], DiffMap['y'], c=DiffMap['DiffMap'], cmap=cmap, norm=MidpointNormalize(midpoint=0,vmin=amin(DiffMap['DiffMap']), vmax=amax(DiffMap['DiffMap'])), marker = ".", alpha=1) #alpha is transparency
        else:
            cmap = plt.cm.plasma                    # color map
            plt.scatter(DiffMap['x'], DiffMap['y'], c=DiffMap['DiffMap'], cmap=cmap, marker = ".", alpha=1) #alpha is transparency
        plt.annotate(f'r^2 = {r2:.4f}', (float(x.min()-10), float(y.min())-40), annotation_clip = False)
        plt.colorbar(mappable = None, label = 'DiffMap', orientation="vertical", ticks=np.linspace(amin(DiffMap['DiffMap']), amax(DiffMap['DiffMap']), 10))                                                                                                                                                                         #contour map, colour bar and colourbar label???
        plt.xlabel(r'$X$', fontsize=15)
        plt.ylabel(r'$Y$', fontsize=15)
        plt.title(f'{CSVinputfilename1}_vs_{CSVinputfilename2}_DiffMap')
        # plt.title(f'{inputfilename2}\nvs Blind Prediction {vcol}_ORIGvsORIG-r:({s2xr}, {s2yr}, {s2zr})_ErrorMap')
        plt.tight_layout()
        if save == True:
            plt.savefig(f'{savewd}{CSVinputfilename1}_vs_{CSVinputfilename2}_DiffMap{extension_png}', dpi=1000, bbox_inches = 'tight')
            # plt.savefig(f'{savewd}{inputfilename2}vs BPred {vcol}_ORIGvsORIG-r({s2xr}, {s2yr}, {s2zr})-offset({x1off}, {y1off}, {z1off})_ErrorMap{extension_png}', bbox_inches = 'tight')
        plt.show()
        
        plt.hist(DiffMap['DiffMap'], bins=np.linspace(DiffMap['DiffMap'].min(), DiffMap['DiffMap'].max(), 1000))
        plt.xlabel(f"Difference", fontsize=15)
        plt.ylabel(f'Frequency', fontsize=15)
        plt.title(f'DiffMap Histogram')       
        plt.annotate( r"$\mu$" + f": {DiffMap['DiffMap'].mean():.3f}\n" + r"$\sigma:$" + f" {DiffMap['DiffMap'].std():.3f}\n",(0.85,0.8), xycoords='axes fraction')
        if save == True:
            plt.savefig(f'{savewd}{CSVinputfilename1}_DiffMapHist{extension_png}', dpi=1000, bbox_inches = 'tight')
            # plt.savefig(f'{savewd}{inputfilename2}vs BPred {vcol}_ORIGvsORIG-r({s2xr}, {s2yr}, {s2zr})-offset({x1off}, {y1off}, {z1off})_ErrorMap{extension_png}', bbox_inches = 'tight')
        plt.show()
        df = DiffMap.astype({xcol1: np.float32, ycol1: np.float32, "DiffMap": np.float32})

'''Labels'''
#Create labels
CSV_Label1 = Label(BROWSE_frame, text = "Top Surface .CSV file", pady = 5)
CSV_Label2 = Label(BROWSE_frame, text = "Bottom Surface .CSV file", pady = 5)
header_Label1 = Label(BROWSE_frame, text = "Top Surface .CSV Header row:", pady = 5)
readcols_Label1 = Label(BROWSE_frame, text = "Top Surface .CSV Columns to read (separete by comma):", pady = 5)
skiprows_Label1 = Label(BROWSE_frame, text = "Top Surface .CSV Rows to skip (separete by comma):\nLeave blank if no rows to skip.", pady = 5)
header_Label2 = Label(BROWSE_frame, text = "Bottom Surface .CSV Header row:", pady = 5)
readcols_Label2 = Label(BROWSE_frame, text = "Bottom Surface .CSV Columns to read (separete by comma):", pady = 5)
skiprows_Label2 = Label(BROWSE_frame, text = "Bottom Surface .CSV Rows to skip (separete by comma):\nLeave blank if no rows to skip.", pady = 5)
csv_file_label1 = Label(CSV_frame1, text = "Top Surface .CSV file content", pady = 5)
csv_file_label2 = Label(CSV_frame2, text = "Bottom Surface .CSV file content", pady = 5)


'''Text boxes and scrolls'''
#Create scrollbars
CSVscroll1 = Scrollbar(CSV_frame1)
CSVscroll2 = Scrollbar(CSV_frame2)
#Create text boxes
CSV_Text1 = Text(BROWSE_frame, width = 60, height=2, state=NORMAL)
CSV_Text2 = Text(BROWSE_frame, width = 60, height=2, state=NORMAL)
header_Entry1 = Entry(BROWSE_frame, width = 10, state=NORMAL); header_Entry1.insert(-1, "0")
readcols_Entry1 = Entry(BROWSE_frame, width = 10, state=NORMAL); readcols_Entry1.insert(-1, "1,2,3")
skiprows_Entry1 = Entry(BROWSE_frame, width = 10, state=NORMAL); skiprows_Entry1.insert(-1, "")
header_Entry2 = Entry(BROWSE_frame, width = 10, state=NORMAL); header_Entry2.insert(-1, "0")
readcols_Entry2 = Entry(BROWSE_frame, width = 10, state=NORMAL); readcols_Entry2.insert(-1, "1,2,3")
skiprows_Entry2 = Entry(BROWSE_frame, width = 10, state=NORMAL); skiprows_Entry2.insert(-1, "")
CSV_file_Text1 = Text(CSV_frame1, height=20, state=NORMAL, yscrollcommand = CSVscroll1.set)
CSV_file_Text2 = Text(CSV_frame2, height=20, state=NORMAL, yscrollcommand = CSVscroll2.set)
#Configure scrollbar
CSVscroll1.config(command=CSV_file_Text1.yview)
CSVscroll2.config(command=CSV_file_Text2.yview)

'''Buttons'''
BrowseCSVButt1 = Button(BROWSE_frame, text="Browse Top Surface .CSV file", fg="black", font=("Ariel", 9, "bold"), command=browseCSV1)
BrowseCSVButt2 = Button(BROWSE_frame, text="Browse Bottom Surface.CSV file", fg="black", font=("Ariel", 9, "bold"), command=browseCSV2)
FormatButt= Button(BROWSE_frame, text="Create difference .txt file", fg="black", font=("Ariel", 9, "bold"), command=createDifference)

'''Allocate widgets'''
# BROWSE_frame
BrowseCSVButt1.grid(row = 0, column = 2, sticky = W)
BrowseCSVButt2.grid(row = 1, column = 2, sticky = W)
header_Label1.grid(row = 2, column = 0, sticky = W)
header_Entry1.grid(row = 2, column = 1, sticky = W)
readcols_Label1.grid(row = 3, column = 0, sticky = W)
readcols_Entry1.grid(row = 3, column = 1, sticky = W)
skiprows_Label1.grid(row = 4, column = 0, sticky = W)
skiprows_Entry1.grid(row = 4, column = 1, sticky = W)
header_Label2.grid(row = 2, column = 2, sticky = W)
header_Entry2.grid(row = 2, column = 3, sticky = W)
readcols_Label2.grid(row = 3, column = 2, sticky = W)
readcols_Entry2.grid(row = 3, column = 3, sticky = W)
skiprows_Label2.grid(row = 4, column = 2, sticky = W)
skiprows_Entry2.grid(row = 4, column = 3, sticky = W)
FormatButt.grid(row = 0, column = 6, sticky = W)
#CSV_frame
CSV_Label1.grid(row = 0, column = 0, sticky = W)
CSV_Text1.grid(row = 0, column = 1, sticky = W)
csv_file_label1.grid(row = 1, column = 1, sticky = W)
CSV_file_Text1.grid(row = 2, column = 1)
CSVscroll1.grid(row = 1, column = 3, rowspan = 3, sticky = NS)
CSV_Label2.grid(row = 1, column = 0, sticky = W)
CSV_Text2.grid(row = 1, column = 1, sticky = W)
csv_file_label2.grid(row = 2, column = 1, sticky = W)
CSV_file_Text2.grid(row = 3, column = 1)
CSVscroll2.grid(row = 1, column = 3, rowspan = 3, sticky = NS)

'''Menu bar'''
menubar = Menu(root)
root.config(menu = menubar)
file_menu = Menu(menubar)
menubar.add_cascade(label = "File", menu = file_menu)
file_menu.add_command(label = "Create difference .txt file", command = createDifference)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
options_menu = Menu(menubar)
menubar.add_cascade(label = "Options", menu = options_menu)
options_menu.add_command(label = "Description", command = description)

'''Prompt on open'''
#Uncomment below if you wish the description() function (info box explaining how the app works) to be prompted at app opening
#description()

'''Add Window title, geometry and create Window's main loop'''
root.title("Tkinter - CSV surface difference calculator")
root.geometry("2000x800")
root.mainloop()