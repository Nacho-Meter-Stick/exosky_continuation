from math import sqrt, sin, cos
import numpy as np
from scipy.spatial.transform import rotation as R
'''
c = cos([rotation_magnitude]/2)
s = sin([rotation_magnitude]/2)
q = c + sAXIi + sAXJj + sAXKk
p1 = PIi + PJj + PKk
q* = c - sAXIi - sAXJj - sAXKk
p2 = qpq*
   = (-(sAXI*PI + sAXJ*PJ + sAXK*PK)
      +(c*PI + sAXJ*PK - sAXK*PJ)i
      +(c*PJ + sAXK*PI - sAXI*PK)j
      +(c*PK + sAXI*PJ - sAXJ*PI)k)(q*)
   = (a + bi + dj + fk)(c - sAXIi - sAXJj - sAXKk)
   = (ac + bsAXI + dsAXJ + fsAXK)
    +(bc + fsAXJ - asAXI - dsAXK)i
    +(dc + bsAXK - asAXJ - fsAXI)j
    +(fc + dsAXI - asAXK - bsAXJ)k
'''
def quaternions_product(A: tuple[float, float, float, float], 
                        B: tuple[float, float, float, float]) -> tuple[float, float, float, float]:
    return (A[0]*B[0] - A[1]*B[1] - A[2]*B[2] - A[3]*B[3], 
            A[0]*B[1] + A[1]*B[0] + A[2]*B[3] - A[3]*B[2], 
            A[0]*B[2] + A[2]*B[0] + A[3]*B[1] - A[1]*B[3], 
            A[0]*B[3] + A[3]*B[0] + A[1]*B[2] - A[2]*B[1])

def q_conjugate(q: tuple[float, float, float, float]) -> tuple[float, float, float, float]:
    return (q[0], -q[1], -q[2], -q[3])

def point_around_quaternion(p: tuple[float, float, float], 
                            q: tuple[float, float, float, float]) -> tuple[float, float, float]:
    return quaternions_product(quaternions_product(q, (0, p[0], p[1], p[2])), q_conjugate(q))

def normalized(vector_rectangular: tuple[float,...]) -> float:
    r = sqrt(sum(i*i for i in vector_rectangular))
    return tuple(i/r for i in vector_rectangular)

def quaternion(rotation_angle: float, 
               vector_rectangular: tuple[float, float, float] = None, 
               vector_polar: tuple[float, float, float] = None) -> tuple[float, float, float, float]:
    '''
    all angles must be radians
    '''
    if vector_polar is None:
        x, y, z = normalized(vector_rectangular)
    if vector_rectangular is None:
        _, theta, phi = vector_polar
        x, y, z = cos(theta), sin(theta)*sin(phi), cos(phi)
    c, s = cos(rotation_angle/2), sin(rotation_angle/2)
    return (c, s*x, s*y, s*z)

def apply_exo_rotation_to_starmap(star_map, longitude_of_ascending_node, inclination, argument_of_periapsis):
    rotation = R.from_euler('zxz', np.array([-longitude_of_ascending_node, -inclination, -argument_of_periapsis]))
    for entry in star_map: entry['coordinates'] = rotation.apply(entry['coordinates'])
