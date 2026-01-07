import numpy as np
from shapely.geometry import Polygon, Point
from starplot import geod


def create_ellipse(
    ra: float, dec: float, maj_ax: float, min_ax: float, angle: float = 0
):
    if np.isnan(angle):
        angle = 0

    maj_ax_degrees = maj_ax / 60

    if np.isnan(min_ax):
        min_ax_degrees = maj_ax_degrees
    else:
        min_ax_degrees = min_ax / 60

    points = geod.ellipse(
        (ra, dec),
        min_ax_degrees,
        maj_ax_degrees,
        angle,
        num_pts=100,
    )

    def fix_ra(r):
        if r < 0:
            r += 360
        return round(r, 4)

    points = [(fix_ra(r), round(d, 4)) for r, d in points]

    return Polygon(points)


def create_geometry(
    ra: float, dec: float, maj_ax: float, min_ax: float, angle: float = 0
) -> Polygon | Point:
    if maj_ax and min_ax:
        return create_ellipse(ra, dec, maj_ax, min_ax, angle)
    return Point(ra, dec)


def size_deg2(geometry, a, b):
    """Returns size (in sq degrees) of minimum bounding rectangle of a DSO"""
    size = None
    geometry_types = geometry.geom_type

    if "Polygon" in geometry_types and "MultiPolygon" not in geometry_types:
        size = geometry.envelope.area

    elif "MultiPolygon" in geometry_types:
        size = sum([p.envelope.area for p in geometry.geoms])

    elif a and not np.isnan(b):
        size = (a / 60) * (b / 60)

    elif a:
        size = (a / 60) ** 2

    if size:
        size = round(size, 8)

    return size
