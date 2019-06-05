# -*- coding: utf-8 -*-
#anaconda/python3.7
"""
Spyder Editor

Anaconda/python 3.7


This is a temporary script file.
"""

import numpy as np
import matplotlib.pyplot as plt
import functions as fct

#===================== data import ============================================

#file = 'hygdata_part1.txt'
file = 'hygdata_v3.txt'

Data = np.genfromtxt(file, delimiter = ',', 
                     usecols = (0, 7, 8, 9, 13, 14, 16, 17, 18, 19, 33), 
                     skip_header = 2, skip_footer = 1).T
"""
0 = id
1 = Right Ascension (RA)
2 = Declination (Dec)
3 = Distance
4 = Apparent Magnitude
5 = Absolute Magnitude
6 = Color Index
7 = x coordinate
8 = y coordinate
9 = z coordinate
10 = Luminosity
"""
distance = Data[3]
apparentMag = Data[4]
absoluteMag = Data[5]
ColorIndex = Data[6]
ID = Data[0]
Luminosity = Data[10]

absMag = fct.AbsMag(apparentMag, distance)

#========== Making the data useable ====================================
"""Here I calculate other values not available directly through the data but 
that needed to be derived from the data (like the radius). And filtering
out unusable data such as nan values."""

""" some color index data is not available and is in the array as nan. The 
following lines filter those out of the data."""
sel = ~np.isnan(ColorIndex)
ColorIndex = ColorIndex[sel]
absoluteMag = absoluteMag[sel]
Luminosity = Luminosity [sel]

Temperatures = fct.Temp(ColorIndex)
fct.Radius(Luminosity, Temperatures)

#========== Plotting an HR diagram =================================

fig, ax = plt.subplots(figsize=(8,10))

ax.set_xlim(-0.5, 2.5)
ax.set_ylim(20, -10)
ax.grid()
ax.set_title('H-R Diagram')

ax.title.set_fontsize(20)
ax.set_xlabel('Color index B-V')
ax.xaxis.label.set_fontsize(20)
ax.set_ylabel('Absolute magnitude')
ax.yaxis.label.set_fontsize(20)

ax.scatter(ColorIndex, absoluteMag,
           s=1, edgecolors='none', c='k')

ax.tick_params(axis='both', labelsize=14)
#====================================================================

#============= What's up with those -15 and brighter stars? ==================
"""
sel = np.logical_not(absMag >(-14))

brightBois = ID[sel]
"""

#======== Temperatures ==============================

fig, bx = plt.subplots(figsize=(8,10))

bx.set_xlim(15000, 1000)
bx.set_ylim(20, -10)
bx.grid()
bx.set_title('H-R Diagram')

bx.title.set_fontsize(20)
bx.set_xlabel('Temperature K')
bx.xaxis.label.set_fontsize(20)
bx.set_ylabel('Absolute magnitude')
bx.yaxis.label.set_fontsize(20)

bx.scatter(Temperatures, absoluteMag,
           s=1, edgecolors='none', c='k')

bx.tick_params(axis='both', labelsize=14)

#============ Logarithmic Plot ==================
"""
fig, cx = plt.loglog(figsize=(8,10))

cx.set_xlim(-0.5, 2.5)
cx.set_ylim(20, -10)
cx.grid()
cx.set_title('H-R Diagram')

cx.title.set_fontsize(20)
cx.set_xlabel('Color index B-V')
cx.xaxis.label.set_fontsize(20)
cx.set_ylabel('Absolute magnitude')
cx.yaxis.label.set_fontsize(20)

cx.scatter(ColorIndex, absoluteMag,
           s=1, edgecolors='none', c='k')

cx.tick_params(axis='both', labelsize=14)

"""
dPar = fct.lin_LS(ColorIndex, absoluteMag)



