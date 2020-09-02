import re
from pathlib import Path

from matplotlib import pyplot as plt
from skyfield.api import Loader, Topos


def planet_vector(ephem, time, loc):
    loc = earth + loc
    astrometric = loc.at(time).observe(ephem)
    apparent = astrometric.apparent()
    alt, az, _ = apparent.altaz()

    return (alt.dstr(), az.dstr())


def winjupos_times(file):
    pass


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

    t = ts.now()
    Melbourne = Topos("37.8142 S", "144.9632 E", elevation_m=43)

    alt, az = planet_vector(jupiter, t, Melbourne)
    print(f"Jupiter located at Alt:{alt}, Az:{az}")

    file = "2020-08-22-1315_6-U-L-Jup.ser"

    timestamp = re.search(r"\d{4}.\d{2}.\d{2}.\d{4}.\d{1}", file, re.M).group(0)
    print(timestamp)
