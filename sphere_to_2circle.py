def sphere_to_circle(sphere_xyzs: list[tuple[float, float, float]]) -> tuple[list[tuple[float, float]], list[tuple[float, float]]]:
    '''
    returns circle projections with radius 2:
        (top circle, bottom circle)
    '''
    disc_points_top = []
    disc_points_bottom = []
    for point in sphere_xyzs:
        a, b, c = point
        if c > 0: disc_points_top.append((-2*a/(c+1), 2*b/(c+1)))
        else: disc_points_bottom.append((-2*a/(c-1), -2*b/(c-1)))
    return disc_points_top, disc_points_bottom
