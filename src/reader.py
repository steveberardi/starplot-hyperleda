import math
from functools import cache

import pandas as pd
import numpy as np

from settings import DATA_PATH

N_DIGITS = 4
NA_VALUES = [999, 9.99, -999]


@cache
def ngc_to_m():
    from starplot import DSO, _

    messier = DSO.find(where=[_.m.notnull()])

    return {d.ngc: d.m for d in messier}


def parse_axis(axis_ratio, apparent_diameter) -> tuple[float, float]:
    if np.isnan(axis_ratio) or np.isnan(apparent_diameter):
        return None, None

    D = 10**apparent_diameter
    D_arcmin = D * 0.1
    R = 10**axis_ratio
    a = D_arcmin * math.sqrt(R) / 2
    b = D_arcmin / (2 * math.sqrt(R))
    return round(a, 6), round(b, 6)


def parse_ra(row):
    value = row.ra_string
    h = float(value[:2])
    m = float(value[2:4])
    s = float(value[4:])
    hours_dec = h + m / 60 + s / 3600
    return round(hours_dec * 15, N_DIGITS)


def parse_dec(row):
    value = row.dec_string
    sign = 1 if str(value[0]) == "+" else -1
    d = float(value[1:3])
    m = float(value[3:5])
    s = float(value[5:])
    return round(sign * (d + m / 60 + s / 3600), N_DIGITS)


def parse_name(value) -> tuple[str, str]:
    messier = ngc_to_m()

    if not value or not isinstance(value, str):
        return None, None

    designations = value.split()
    m, ngc, ic = None, None, None

    for d in designations:
        if d.startswith("NGC"):
            ngc = d[3:].strip()
            m = messier.get(ngc)
        if d.startswith("IC"):
            ic = d[2:].strip()

    return m, ngc, ic


def read_pgc():
    # Row Format
    #    1-  3  A3    ---          ---     [PCG]
    #    4- 10  I7    ---          PGC     [1/3099300] PGC number
    #       12  A1    ---          ---     [J]
    #   13- 14  I2    h            RAh     Right ascension (J2000)
    #   15- 16  I2    min          RAm     Right ascension (J2000)
    #   17- 20  F4.1  s            RAs     Right ascension (J2000)
    #       21  A1    ---          DE-     Declination sign (J2000)
    #   22- 23  I2    deg          DEd     Declination (J2000)
    #   24- 25  I2    arcmin       DEm     Declination (J2000)
    #   26- 27  I2    arcsec       DEs     Declination (J2000)
    #   29- 30  A2    ---          OType   [GM ] Object type (1)
    #   32- 36  A5    ---          MType   Provisional morphological type from LEDA
    #                                       according to the RC2 code.
    #   37- 41  F5.2 [0.1arcmin]   logD25  ?=9.99 Apparent diameter (2)
    #   42- 44  A3    ---          ---     [+/-]
    #   45- 48  F4.2 [0.1arcmin] e_logD25  ?=9.99 Actual error of logD25
    #   51- 54  F4.2  [---]        logR25  ?=9.99 Axis ratio in log scale
    #                                        (log of major axis to minor axis)
    #   55- 57  A3    ---          ---     [+/-]
    #   58- 61  F4.2  [---]      e_logR25  ?=9.99 Actual error on logR25
    #   64- 67  F4.0  deg          PA      ?=999. Adopted 1950-position angle (3)
    #   68- 70  A3    ---          ---     [+/-]
    #   71- 74  F4.0  deg        e_PA      ?=999. rms uncertainty on PA
    #   76- 77  I2    ---        o_ANames  Number of alternate names.
    #   79-341  A263  ---          ANames  Alternate names (4)

    column_names = [
        "pgc",
        "ra_string",
        "dec_string",
        "object_type",
        "diameter_apparent",
        "axis_ratio",
        "angle",
        "other_designations",
    ]
    colspecs = [
        (0, 10),  # 'PGC' and Number
        (12, 20),  # RA string
        (20, 27),  # DEC string
        (28, 30),  # object type
        (36, 41),  # apparent diameter
        (50, 54),  # axis ratio
        (63, 67),  # angle
        (75, None),  # Name string
    ]
    df = pd.read_fwf(
        DATA_PATH / "pgc.dat",
        header=None,
        colspecs=colspecs,
        names=column_names,
        na_values=NA_VALUES,
        dtype={
            "pgc": "string",
            "ra_string": "string",
            "dec_string": "string",
            "object_type": "string",
            "diameter_apparent": "float64",
            "axis_ratio": "float64",
            "other_designations": "string",
        },
    )

    df["ra_degrees"] = df.apply(parse_ra, axis=1)
    df["dec_degrees"] = df.apply(parse_dec, axis=1)

    return df
