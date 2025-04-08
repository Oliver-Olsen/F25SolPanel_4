#funktionen for solar elevation 
import numpy as np
def solar_elevation_angle(theta):
    alpha = np.deg2rad((90 - theta))
    return alpha #bruger formlen til at udregne alpha i radianer
