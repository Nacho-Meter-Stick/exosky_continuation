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
def cartesian_STAR_MAP_to_circles(star_map) -> tuple[list[tuple[float, float, float]], list[tuple[float, float, float]]]:
    disc_points_top = []
    disc_points_bottom = []
    for entry in star_map:
        x, y, z = entry['coordinates']
        mag = entry['magnitude']
        if z > 0: disc_points_top.append((-x/(z+1), y/(z+1), mag))
        else: disc_points_bottom.append((-x/(z-1), -y/(z-1), mag))
    return disc_points_top, disc_points_bottom
