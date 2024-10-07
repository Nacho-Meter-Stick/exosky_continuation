import math
def delta_star_magnitude(d1_squared: float, d2_squared: float) -> float:
    return 2.5*math.log(d2_squared/d1_squared)/math.log(10)
    # delta_m = 5 * math.log(d2)/math.log(10) - 5 * math.log(d1)/math.log(10)
    # delta_m = 2.5 * math.log(d2_squared/d1_squared)/math.log(10)
