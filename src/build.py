import logging

from skyfield.api import position_of_radec, load_constellation_map
from starplot import DSO, DsoType
from starplot.data import Catalog

from geometry import create_geometry, size_deg2
from magnitudes import read_magnitudes
from reader import read_pgc, parse_axis, parse_name
from settings import BUILD_PATH, __version__


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler("build.log", mode="a")
logger.addHandler(console_handler)
logger.addHandler(file_handler)
formatter = logging.Formatter(
    "{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M:%S",
)
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

constellation_map = load_constellation_map()


def get_constellation(ra, dec):
    pos = position_of_radec(ra / 15, dec)
    return constellation_map(pos).lower()


def dsos_all():
    logger.info("Reading pgc.dat...")
    df = read_pgc()
    logger.info("Reading magnitudes...")
    mag_by_pgc = read_magnitudes(bibcodes=[27103])
    ctr = 0
    for d in df.itertuples():
        ctr += 1
        pgc_id = int(d.pgc[3:])
        ra, dec = d.ra_degrees, d.dec_degrees

        maj_ax, min_ax = parse_axis(d.axis_ratio, d.diameter_apparent)
        geometry = create_geometry(ra, dec, maj_ax, min_ax, d.angle)

        m, ngc, ic = parse_name(d.other_designations)
        size = size_deg2(geometry, maj_ax, min_ax)
        magnitude = mag_by_pgc.get(pgc_id) or None
        g_type = (
            DsoType.GALAXY
            if d.object_type.strip() == "G"
            else DsoType.GROUP_OF_GALAXIES
        )

        yield DSO(
            pk=pgc_id,
            ra=ra,
            dec=dec,
            constellation_id=get_constellation(ra, dec),
            name=d.pgc,
            maj_ax=maj_ax,
            min_ax=min_ax,
            angle=d.angle,
            geometry=geometry,
            size=size,
            magnitude=magnitude,
            type=g_type,
            m=m,
            ngc=ngc,
            ic=ic,
        )

        if ctr % 10_000 == 0:
            logger.info(f"Total objects read: {ctr:,}")

    logger.info(f"Total objects read: {ctr:,}")


def build():
    logger.info("Building HyperLeda catalog...")
    output_path = BUILD_PATH / f"hyperleda.{__version__}.parquet"
    hyperleda = Catalog(path=output_path)
    hyperleda.build(
        objects=dsos_all(),
        chunk_size=1_000_000,
        columns=[
            "pk",
            "name",
            "ra",
            "dec",
            "constellation_id",
            "type",
            "maj_ax",
            "min_ax",
            "angle",
            "magnitude",
            "size",
            "m",
            "ngc",
            "ic",
            "geometry",
        ],
        sorting_columns=["magnitude", "m", "ngc", "ic"],
        compression="snappy",
        row_group_size=100_000,
    )

    all_galaxies = [d for d in DSO.all(catalog=hyperleda)]

    logger.info(f"Total objects: {len(all_galaxies):,}")
    assert len(all_galaxies) == 983_261

    andromeda = DSO.get(m="31", catalog=hyperleda)
    assert andromeda.ra == 10.6846
    assert andromeda.dec == 41.2694
    assert andromeda.maj_ax == 167.482720
    assert andromeda.min_ax == 59.425111
    assert andromeda.angle == 35

    logger.info("Checks passed!")


if __name__ == "__main__":
    build()
