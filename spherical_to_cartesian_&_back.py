import numpy as np
import math
# All angles must be in radians
def dist_exo_star(r_star, r_exo, phi_star, phi_exo, theta_star, theta_exo):
    return np.sqrt(r_star**2 + r_exo**2 - 2*r_star*r_exo*np.sin(phi_star)*np.sin(phi_exo)*(np.cos(theta_star-theta_exo)-1))
def spherical_to_cartesian(obj: np.array[float, float, float]) -> np.array[float, float, float]:
    r, theta, phi = obj
    s1, c1 = np.sin(phi), np.cos(phi)
    s2, c2 = np.sin(theta), np.cos(theta)
    return r*np.array((s1*s2, s1*c2, c1))
def cartesian_to_spherical(obj: np.array[float, float, float]) -> np.array[float, float, float]:
    x, y, z = obj
    r = np.sqrt(x*x + y*y + z*z)
    phi = np.acos(z/r)
    theta = (1-2*(y<0))*np.acos(y/(r*np.sqrt(x*x + y*y)))
    return np.array((r, phi, theta))
# This takes an 2 (r, theta, phi)'s for a star and an exoplanet and spits out a 
#    (r, theta, phi) that represents the star from the exoplanet perspective.
# This assumes the celestial sphere of the exoplanet faces the exact same way as the celestial sphere of Earth.
def func(star: np.array[float, float, float], exoplanet: np.array[float, float, float]) -> np.array[float, float, float]:
    return cartesian_to_spherical(spherical_to_cartesian(star)-spherical_to_cartesian(exoplanet))
