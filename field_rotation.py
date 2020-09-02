import re
from datetime import datetime
from pathlib import Path

import numpy as np
from matplotlib import pyplot as plt
from skyfield.api import Loader, Topos, utc


def planet_vector(ephem, time, loc):
    "Determine alt/az of planet at given time and location"
    loc = earth + loc
    astrometric = loc.at(time).observe(ephem)
    apparent = astrometric.apparent()
    alt, az, _ = apparent.altaz()

    return (alt.degrees, az.degrees)


def winjupos_time(ts, file):
    "Parse time from winjupos filename and convert to skyfield utc time object"

    name = Path(file).stem
    timestamp = re.search(r"\d{4}.\d{2}.\d{2}.\d{4}.\d{1}", name, re.M).group(0)

    dt, sec = timestamp.split("_")
    sec = round(int(sec) * 6)
    y, m, d, tm = dt.split("-")
    hr, mi = tm[:2], tm[2:]

    timestamp = ts.utc(int(y), int(m), int(d), int(hr), int(mi), int(sec),)

    return timestamp


def planet_trajectory(ephem, loc, ts, data_dir):

    f_names = [f for f in Path(data_dir).glob("*.ser")]

    alt_az = []
    for f in f_names:
        timestamp = winjupos_time(ts, f)
        alt_az.append(planet_vector(ephem, timestamp, loc))

    return alt_az


if __name__ == "__main__":

    # Download Ephemerides & timescale files
    load = Loader("ephemerides")
    planets = load("de421.bsp")
    ts = load.timescale()

    # Solar System Ephemerides
    sun = planets["sun"]
    mercury = planets["mercury"]
    venus = planets["venus"]
    mars = planets["mars"]
    earth = planets["earth"]
    moon = planets["moon"]
    jupiter = planets["jupiter barycenter"]
    saturn = planets["saturn barycenter"]
    uranus = planets["uranus barycenter"]
    neptune = planets["neptune barycenter"]
    pluto = planets["pluto barycenter"]

    Melbourne = Topos("37.8142 S", "144.9632 E", elevation_m=43)

    # timestamp = winjupos_time(
    #    "/Volumes/Fangorn/planets/Jup/220820/2020-08-22-1315_6-U-L-Jup.ser"
    # )
    # alt, az = planet_vector(jupiter, timestamp, Melbourne)
    # print(f"Jupiter located at Alt:{alt}, Az:{az}")

    alt_az = planet_trajectory(jupiter, Melbourne, ts, "/Volumes/Fangorn/planets/Jup/290820")
    print(alt_az)
