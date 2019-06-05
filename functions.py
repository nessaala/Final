# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 22:46:39 2019

@author: Nessa
"""
import numpy as np


#============= Plotting HR Diagram =================

def AbsMag(apparentMag, distance):
    return (apparentMag - 5*np.log10(distance/100))

def Temp( cIndex):
    return 5601/(cIndex + 0.4)**(2/3)

def Radius ( Luminosity, Temperature):
  #  solLum = 1     # Luminosity given in units of solar lum in the data
    solTemp = 5777 # Kelvin
    solRadius = 695.51e6 #in meters
    # In units of solar radii
    radius = ((Temperature/solTemp)**2)*(Luminosity)**(1/2)
    return radius*solRadius # Radius in meters

def lin_LS( aX, aY):
    """
    - linear least squares assuming normal distributed errors in Y, no errors in X

    :param aX: - independent variable
    :param aY: - measured dependent variable

    :return: { 'a' :  float( <intercept>),
               'b' :  float( <slope>),
               'R2 :  float(), #coefficient of variation = r_p**2 for lin. regre
               'r_p:  float(), # correlation coefficient (Pearson)

               'Y_hat' : np.array(), # modeled values of aY using a and b
            }

    example:   TODO:
    """
    dLS   = {}
    N     = len(aX)
    if len( aX) != len( aY):
        error_str = 'input variable need to have same dimensions %i, %i'%( len( aX), len( aY))
        raise (ValueError, error_str)
    meanX = aX.mean()
    meanY = aY.mean()
    # variance and co-variance - 1./N term omitted because it cancels in the following ratio
    VarX  = ( (aX - meanX)**2).sum()
    VarY  = ( (aY - meanY)**2).sum()
    CovXY = ( (aY-meanY)*(aX-meanX)).sum()

    
    # slope and intercept, and fit
    dLS['b'] = CovXY/VarX
    dLS['a'] = meanY - meanX*dLS['b']
    dLS['Y_hat'] = dLS['b']*aX + dLS['a']
    # goodness-of-fit
    ResSS    = ( ( dLS['Y_hat'] - aY)**2).sum()
    dLS['R2']= 1 - ResSS/VarY
    # correlation coefficient
    dLS['r_p'] = 1./N*CovXY/(aX.std()*aY.std())
    return dLS

