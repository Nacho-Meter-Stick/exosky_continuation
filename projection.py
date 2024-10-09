import numpy as np
import numpy.typing as npt
from database import STAR_ENTRY_TYPE

def normalized(vector_rectangular: npt.NDArray) -> float:
    r = np.sqrt(np.sum(np.square(vector_rectangular)))
    return vector_rectangular/r

def cartesian_STAR_MAP_to_circles(star_map: npt.NDArray) -> tuple[npt.NDArray, npt.NDArray]:
    disc_entries_top = []
    disc_entries_bottom = []
    star_copy = np.copy(star_map)
    for entry in star_copy:
        entry['coordinates'] = normalized(entry['coordinates'])
        x, y, z = entry['coordinates']
        if z > 0:
            entry['coordinates'] = [(-x/(z+1)), y/(z+1), 1]
            disc_entries_top.append(entry)
        else: 
            entry['coordinates'] = [(-x/(z-1)), -y/(z-1), -1]
            disc_entries_bottom.append(entry)

    return (np.array(disc_entries_top, dtype=STAR_ENTRY_TYPE), np.array(disc_entries_bottom, dtype=STAR_ENTRY_TYPE))
