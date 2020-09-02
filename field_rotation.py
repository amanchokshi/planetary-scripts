import re
from datetime import datetime
from pathlib import Path

import numpy as np
from geopy.geocoders import Nominatim
from matplotlib import pyplot as plt
from matplotlib.dates import DateFormatter as mpl_df
from skyfield.api import Loader, Topos


def earth_loc(name):
    "Determine lat.lon.alt of place on Earth."

    locator = Nominatim(user_agent="telescope-loc")
    location = locator.geocode(name)

    lat = location.latitude
    if lat < 0:
        lt = f"{lat} S"
    else:
        lt = f"{lat} N"

    lon = location.longitude
    if lon < 0:
        ln = f"{lon} W"
    else:
        ln = f"{lon} E"

    loc = Topos(lt, ln, elevation_m=location.altitude)
    return loc


def planet_vector(ephem, time, loc):
    "Determine alt/az of planet at given time and location."
    loc = earth + loc
    astrometric = loc.at(time).observe(ephem)
    apparent = astrometric.apparent()
    alt, az, _ = apparent.altaz()

    return (alt.degrees, az.degrees)


def winjupos_time(ts, file):
    "Parse time from winjupos filename and convert to skyfield utc time object."

    name = Path(file).stem
    timestamp = re.search(r"\d{4}.\d{2}.\d{2}.\d{4}.\d{1}", name, re.M).group(0)

    dt, sec = timestamp.split("_")
    sec = round(int(sec) * 6)
    y, m, d, tm = dt.split("-")
    hr, mi = tm[:2], tm[2:]

    timestamp = ts.utc(int(y), int(m), int(d), int(hr), int(mi), int(sec),)

    return timestamp


def planet_trajectory(ephem, ts, data_dir, loc="Melbourne"):

    f_names = [f for f in Path(data_dir).glob("*.ser")]
    loc = earth_loc(loc)

    alt_az = []
    for f in f_names:
        timestamp = winjupos_time(ts, f)
        dt = timestamp.utc_datetime()
        alt, az = planet_vector(ephem, timestamp, loc)
        alt_az.append([dt, alt, az])

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

    alt_az = planet_trajectory(
        jupiter, ts, "/Volumes/Fangorn/planets/Jup/290820", loc="Melbourne"
    )
    
    dates = [i[0] for i in alt_az]
    alt = [i[1] for i in alt_az]
    az = [i[2] for i in alt_az]
    
    date_format = mpl_df('%H:%M')
    plt.style.use('seaborn')
    plt.plot_date(dates[::10], alt[::10])
    plt.gca().xaxis.set_major_formatter(date_format)
    plt.tight_layout()
    plt.show()
