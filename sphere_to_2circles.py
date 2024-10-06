import numpy as np
import numpy.typing as npt
from quaternions import normalized
from database import STAR_ENTRY_TYPE

def sphere_to_circle(sphere_xyzs: list[tuple[float, float, float]]) -> tuple[list[tuple[float, float]], list[tuple[float, float]]]:
    '''
    returns circle projections with radius 1:
        (top circle, bottom circle)
    '''
    disc_points_top = []
    disc_points_bottom = []
    for point in sphere_xyzs:
        a, b, c = point
        if c > 0: disc_points_top.append((-a/(c+1), b/(c+1)))
        else: disc_points_bottom.append((-a/(c-1), -b/(c-1)))
    return disc_points_top, disc_points_bottom

def cartesian_STAR_MAP_to_circles(star_map: npt.NDArray) -> tuple[npt.NDArray, npt.NDArray]:
    disc_entries_top = []
    disc_entries_bottom = []
    for entry in star_map:
        entry_copy = np.copy(entry)
        entry_copy['coordinates'] = normalized(entry_copy['coordinates'])
        x, y, z = entry_copy['coordinates']
        if z > 0:
            entry_copy['coordinates'] = [(-x/(z+1)), y/(z+1), 1]
            disc_entries_top.append(entry_copy)
        else: 
            entry_copy['coordinates'] = [(-x/(z-1)), -y/(z-1), -1]
            disc_entries_bottom.append(entry_copy)

    return (np.array(disc_entries_top, dtype=STAR_ENTRY_TYPE), np.array(disc_entries_bottom, dtype=STAR_ENTRY_TYPE))
