from math import radians, cos, sin


def scale_between(unscaled_num, min_allowed, max_allowed, _min, _max):
    # https://stackoverflow.com/a/31687097
    return (max_allowed - min_allowed) * (unscaled_num - _min) / (_max - _min) + min_allowed


def rotate_polygon(points, degrees):
    """ Rotate polygon the given angle about its center. """
    # https://stackoverflow.com/a/45511474

    theta = radians(degrees)  # Convert angle to radians
    cos_ang, sin_ang = cos(theta), sin(theta)

    #points = polygon.getPoints()
    # find center point of Polygon to use as pivot
    n = len(points)
    cx = sum(p[0] for p in points) / n
    cy = sum(p[1] for p in points) / n

    new_points = []
    for p in points:
        x, y = p[0], p[1]
        tx, ty = x-cx, y-cy
        new_x = (tx*cos_ang + ty*sin_ang) + cx
        new_y = (-tx*sin_ang + ty*cos_ang) + cy
        new_points.append((new_x, new_y))

    return new_points
    #rotated_ploygon = polygon.clone()  # clone to get current attributes
    #rotated_ploygon.points = new_points
    #return rotated_ploygon