import math
import csv

from io import StringIO
from pprint import pprint

import requests
import pandas as pd
import numpy as np

from settings import DATA_PATH
from reader import read_pgc

N_DIGITS = 4
NA_VALUES = [999, 9.99, -999]


def chunked(lst, chunk_size):
    """Yield successive chunks from lst."""
    for i in range(0, len(lst), chunk_size):
        yield lst[i : i + chunk_size]


def get_magnitudes(pgc_names: list):
    url = "http://atlas.obs-hp.fr/hyperleda/fG.cgi"
    params = {
        "a": "t",
        "sql": "bandname='B'",
        "o": ",".join(pgc_names),
        "n": "a107",
        "c": "o",
        "of": "1,leda,simbad",
        "d": "$objname,$L,$j2000,$field[mag],loga,iso,code_mag,correction,bandname,$link[iref,iref]",
        "nra": "l",
    }
    response = requests.get(url, params=params)

    column_names = [
        "pgc",
        "mag",
        "bibcode",
    ]
    colspecs = [
        (0, 20),  # 'PGC' and Number
        (48, 53),  # magnitude
        (90, None),  # bibcode
    ]

    df = pd.read_fwf(
        StringIO(response.text),
        sep="\t",
        comment="#",
        na_values=NA_VALUES,
        colspecs=colspecs,
        names=column_names,
        header=None,
    )

    results = []
    for _, d in df.iterrows():
        results.append((d["pgc"], d["mag"], d["bibcode"]))

    return results


def parse_axis(axis_ratio, apparent_diameter) -> tuple[float, float]:
    D = 10**apparent_diameter
    D_arcmin = D * 0.1
    R = 10**axis_ratio
    a = D_arcmin * math.sqrt(R) / 2
    b = D_arcmin / (2 * math.sqrt(R))
    return a, b


def parse_ra(row):
    value = row.ra_string
    h = float(value[:2])
    m = float(value[2:4])
    s = float(value[4:])
    return round(h + m / 60 + s / 3600, N_DIGITS)


def parse_dec(row):
    value = row.dec_string
    sign = 1 if str(value[0]) == "+" else -1
    d = float(value[1:3])
    m = float(value[3:5])
    s = float(value[5:])
    return round(sign * (d + m / 60 + s / 3600), N_DIGITS)


def parse_name(value) -> tuple[str, str]:
    if not value or not isinstance(value, str):
        return None, None

    designations = value.split()
    ngc, ic = None, None

    for d in designations:
        if d.startswith("NGC"):
            ngc = d[3:].strip()
        if d.startswith("IC"):
            ic = d[2:].strip()

    return ngc, ic


def chunked(lst, chunk_size):
    """Yield successive chunks from lst."""
    for i in range(0, len(lst), chunk_size):
        yield lst[i : i + chunk_size]


def get_mags():
    df = read_csv()

    # TODO : need to update these start/stop for next run!
    start = 800_000
    stop = 1_000_000
    print(start, stop)
    pgc_names_all = df["pgc"].tolist()[start:stop]

    # note: PGC number in mags.csv is not 0-padded

    ctr = 0
    with open(DATA_PATH / "mags2.csv", "a") as magfile:
        writer = csv.writer(magfile)
        for chunk in chunked(pgc_names_all, 500):
            print(ctr)
            mags = get_magnitudes(chunk)
            # all_mags.extend(mags)
            # time.sleep(0.1)
            ctr += 1
            print(f"Retrieved {len(mags)}")

            for row in mags:
                writer.writerow(row)

    print(start, stop)


def get_bibcodes():
    with open(DATA_PATH / "mags.csv", "r") as magfile:
        reader = csv.reader(magfile)
        next(reader)
        return {int(row[2]) for row in reader}


def read_magnitudes(bibcodes: list[int]) -> dict:
    """
    Args:
        bibcodes: Allowed bibcodes in priority order

    Returns:
        Dictionary keyed on integer PGC ID and value is magnitude from first bibcode with result
    """
    df = read_pgc()
    pgc_names_all = df["pgc"].tolist()
    mag_by_pgc = {}

    pgc_bibcode_mags = {}
    with open(DATA_PATH / "mags.csv", "r") as magfile:
        reader = csv.reader(magfile)
        next(reader)
        for pgc, mag, code in reader:
            code = int(code)
            if not pgc.startswith("PGC"):
                continue
            pgc_id = int(pgc[3:])
            pgc_bibcode_mags[(pgc_id, code)] = float(mag)

    for pgc in pgc_names_all:
        pgc_id = int(pgc[3:])

        for code in bibcodes:
            if (pgc_id, code) in pgc_bibcode_mags:
                mag_by_pgc[pgc_id] = pgc_bibcode_mags[(pgc_id, code)]
                break

    return mag_by_pgc
    # pprint(mag_by_pgc)
    # print(len(mag_by_pgc.keys()))


def get_bibcode_dist():
    df = read_pgc()

    pgc_names_all = df["pgc"].tolist()
    pgc_bibcodes = {}  # dict keyed on PGC integer and value is set of bibcodes
    bc_count = {}

    with open(DATA_PATH / "mags.csv", "r") as magfile:
        reader = csv.reader(magfile)
        next(reader)

        for pgc, mag, code in reader:
            code = int(code)
            if not pgc.startswith("PGC"):
                continue
            pgc_id = int(pgc[3:])
            if pgc_id in pgc_bibcodes:
                pgc_bibcodes[pgc_id].add(code)
            else:
                pgc_bibcodes[pgc_id] = {code}

            if code not in bc_count:
                bc_count[code] = 0

    no_mag = 0

    for pgc in pgc_names_all:
        pgc_id = int(pgc[3:])
        codes = pgc_bibcodes.get(pgc_id)

        if not codes:
            no_mag += 1
            continue

        for bc in codes:
            bc_count[bc] += 1

    print(f"No mag = {no_mag}")
    pprint(bc_count)


if __name__ == "__main__":
    # get_mags()
    # print(get_bibcodes())
    # get_bibcode_dist()
    read_magnitudes([27103])
