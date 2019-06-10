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

file = 'hygdata_v3.txt'

# Filtered out unwanted columns in the data file
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
ID = Data[0]
RA = Data[1]
Dec = Data[2]
distance = Data[3]
apparentMag = Data[4]
absoluteMag = Data[5]
ColorIndex = Data[6]
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

Temperatures = fct.Temp(ColorIndex) #can calculate temperatures using formula with color index
Radius = fct.Radius(Luminosity, Temperatures) 
 #Was not given radius, calculate radius, then test to see if data fits

#========== Plotting an HR diagram =================================

fig1, ax = plt.subplots(figsize=(8,10))

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
plt.savefig('HR')
#====================================================================

#============= What's up with those -15 and brighter stars? ==================
"""
sel = np.logical_not(absMag >(-14))

brightBois = ID[sel]
"""
# Found out that a lot of the data is incorrect. There are many dubious values
# and given more time I'd filter more of them out

#============== Least Square method using restricted variables ================

""" 
Only using stars that are approximately the same temperature as the Sun, we can determine
the exponent on L = R**alpha * T**Beta to determine the dependence of Luminosity
on the temperature and the Radius of the star.  
"""
solarLum = 3.827e26  # Solar Luminosity in Watts
solarTemp = 5777     # temperature of the Sun so that Temp is in solar units

tempsel = np.isclose(Temperatures/solarTemp, 1, 0.05)   #All stars of similar Temp as the Sun
SolarTempStarsTemp = Temperatures[tempsel]
SolarTempStarsLum = Luminosity[tempsel]
SolarTempStarsRad = Radius[tempsel]
dParR = fct.lin_LS(np.log10(SolarTempStarsRad), np.log10(SolarTempStarsLum))

solsel = np.isclose(Radius, 1, 0.05)            # all stars of similar radius to the Sun
SolarRadiiStarsRad = Radius[solsel]
SolarRadiiStarsLum = Luminosity[solsel]
SolarRadiiStarsTemp = Temperatures[solsel]
dParT = fct.lin_LS(np.log(SolarRadiiStarsTemp/solarTemp), np.log(SolarRadiiStarsLum))

def Lumin (Temperature, alpha):     #Function for checking expected Luminosity
    return (Temperature**alpha)
def LuminR (Radius, beta):          # ''
    return (Radius**beta)
expR = LuminR(SolarTempStarsRad, dParR['b'])            #Expected Values for Luminosity for found exponent of R
exp = Lumin(SolarRadiiStarsTemp/solarTemp, dParT['b'])  #Expected values for found exponent of T

#======== Plots of star data and expected values ==============================
"""
Comparing the Expected values to the actual values
"""
fig = plt.figure( figsize = (16,10))
# log-log graph of the stars with the same radius, temp vs luminosity
# Shows relationship between Temperature and Luminosity
plt.subplot(221)
plt.title('One Solar Radius Stars', weight = 300)
plt.loglog(SolarRadiiStarsTemp, SolarRadiiStarsLum,'ko', markersize = 2)
plt.xlabel('Temperature (K)')
plt.ylabel('Luminosity (L$\odot$)')
plt.grid(True)
#plt.show()


plt.subplot(222)
#log-log graph of the stars with the same temperature, radius vs luminosity
#shows relationship between radius and luminosity
plt.title('Solar Temperature Stars', weight = 300)
plt.loglog(SolarTempStarsRad, SolarTempStarsLum, 'ko', markersize = 2)
plt.ylabel('Luminosity (L$\odot$)')
plt.xlabel('Radii(R$\odot$)')
plt.grid(True)
#plt.show()

plt.subplot(224)
plt.title('Comparing Luminosity of Solar Temperature Stars', weight = 300)
#Comparing expected values of Luminosity given different radii but same Temperature
plt.plot(SolarTempStarsRad, expR, 'bo', markersize = 2, label = 'Expected')
plt.plot(SolarTempStarsRad, SolarTempStarsLum, 'ko', markersize = 2, label = 'Actual Data')
plt.ylabel('Luminosity (L$\odot$)')
plt.xlabel('Radius (R$\odot$)')
plt.xlim(0, 50)
plt.ylim(0, 1000)
plt.legend()
plt.grid(True)
#plt.show()

plt.subplot(223)
plt.title('Comparing Luminosity of Solar Radius Stars', weight = 300)
# Comparing expected values of Luminosity given same radius, but different temp
plt.plot(SolarRadiiStarsTemp, exp, 'ro', markersize = 2, label = 'Expected')
plt.plot(SolarRadiiStarsTemp, SolarRadiiStarsLum, 'ko', markersize = 2, label = 'Actual Data')
plt.ylabel('Luminosity (L$\odot$)')
plt.xlabel('Temperature (K)')
plt.xlim(0, 15500)
plt.ylim(0, 50)
plt.grid(True)
#plt.show()
plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.25,
                    wspace=0.35)
plt.legend()
plt.savefig('Comparisons')

#==============================================================================
#============ Plotting Stars ==================================================

degrees = fct.degrees(RA) #Changes RA into degrees
RA = fct.radians(degrees)

#plotting the positions of the stars. A projection
fig = plt.figure( figsize = (16,10))
bx = fig.add_subplot(111, projection = 'hammer')
plt.title('Locations of Stars', size = 20, weight = 600)
# Change both units of RA and DEC into radians from degrees
bx.scatter( RA - np.pi , fct.radians(Dec), marker = 'o', color = 'k', s = 0.7)
xlab = ['14h','16h','18h','20h','22h','0h','2h','4h','6h','8h','10h'] #changes tick marks to units of RA
bx.set_xticklabels(xlab, weight=800, color = 'r', size = 20)
bx.grid(color = 'b')

plt.savefig('Star map')



