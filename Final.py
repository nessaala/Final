# -*- coding: utf-8 -*-
#anaconda/python3.7
"""
Spyder Editor

Anaconda/python 3.7


This is a temporary script file.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
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
Radius = fct.Radius(Luminosity, Temperatures)

#========== Plotting an HR diagram =================================
plt.figure(1)
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

norm = mpl.colors.Normalize(vmin = -1.5, vmax = .1)
cmap = 'Spectral'
ax.scatter(ColorIndex, absoluteMag,
           s=1, edgecolors='none', norm = norm, c=-ColorIndex, cmap = cmap)

ax.tick_params(axis='both', labelsize=14)
#====================================================================

#============= What's up with those -15 and brighter stars? ==================
"""
sel = np.logical_not(absMag >(-14))

brightBois = ID[sel]
"""

#======== Temperatures ==============================
"""
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
"""

#================ Least Square method using restricted radius =================

""" 
Only using stars that are approximately 1 solar radius, we can determine
the exponent on L = R**alpha * T** Beta to determine the dependence of Luminosity
on the temperature of the star.  
"""
solsel = np.isclose(Radius, 1, 0.05)
SolarRadiiStarsRad = Radius[solsel]
SolarRadiiStarsLum = Luminosity[solsel]
SolarRadiiStarsTemp = Temperatures[solsel]
dParT = fct.lin_LS(np.log(SolarRadiiStarsTemp), np.log(SolarRadiiStarsLum))

solarLum = 3.827e26 # Solar Luminosity in Watts
solarTemp = 5777 #temperature of the Sun so that Temp is in solar units
tempsel = np.isclose(Temperatures/solarTemp, 1, 0.05)
SolarTempStarsTemp = Temperatures[tempsel]
SolarTempStarsLum = Luminosity[tempsel]
SolarTempStarsRad = Radius[tempsel]
dParR = fct.lin_LS(np.log10(SolarTempStarsRad), np.log10(SolarTempStarsLum))

#======== Plot of Temperature vs Luminosity for 1 solar Radius stars ==========
"""
This is mostly to prove to myself that this data is indeed a power function
"""
plt.figure(1)
plt.title('One Solar Radius Stars')
plt.loglog(SolarRadiiStarsTemp, SolarRadiiStarsLum,'ro', markersize = 2)

plt.xlabel('Temperature')
plt.ylabel('Luminosity')
plt.grid(True)
plt.show()

plt.figure(3)
plt.title('Solar Temperature Stars')
plt.loglog(SolarTempStarsLum, SolarTempStarsRad, 'bo', markersize = 2)
plt.xlabel('Luminosity (L$\odot$)')
plt.ylabel('Radii(R$\odot$')
plt.show()

plt.figure(4)
plt.title('Values of Luminosity Using new a and b (Same Temperature')
plt.plot(SolarTempStarsRad, 10**dParR['Y_hat'], 'go', markersize = 2)
plt.ylabel('Luminosity (L$\odot$)')
plt.xlabel('Radius (R$\odot$)')
plt.show()

plt.figure(5)
plt.title('Values of Temperature using new a and b for (Same Radius)')
plt.plot(SolarRadiiStarsLum, 10**dParT['Y_hat'], 'bo', markersize = 2)
plt.xlabel('Luminosity (L$\odot$)')
plt.ylabel('Temperature (K)')
plt.xlim(0, 125)
plt.ylim(0, 70000)
plt.show()



#==============================================================================
#============ SOLVING FINALLY =================================================



