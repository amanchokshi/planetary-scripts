import math
import re
from pathlib import Path

import numpy as np
from astropy.time import Time
from geopy.geocoders import Nominatim
from matplotlib import pyplot as plt
from matplotlib.dates import DateFormatter as mpl_df
from scipy.interpolate import InterpolatedUnivariateSpline
from skyfield.api import Loader, Topos

from tiff import read_tif, write_tif


def earth_loc(name):
    "Determine lat.lon.alt of place on Earth."

    try:
        locator = Nominatim(user_agent="telescope-loc")
        location = locator.geocode(name)

        lat = location.latitude
        lon = location.longitude

        loc = Topos(f"{lat} N", f"{lon} E", elevation_m=location.altitude)

    except Exception:
        print("Unable to determine lat/lon, using Melbourne as default")

        lat = -37.814
        lon = 144.96332

        loc = Topos(f"{lat} N", f"{lon} E", elevation_m=location.altitude)

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


def rotation_rate(lat, alt, az):
    """Compute Rate of Rotation of FoV.

    http://www.jdso.org/volume7/number4/Frey_216_226.pdf
    """

    # Angular velocity of Earth's Rotation
    # W = 4.178 x 10-3 degrees/sec
    W = 4.178e-3

    ror = (W * np.cos(np.radians(lat)) * np.cos(np.radians(az))) / np.cos(
        np.radians(alt)
    )

    return ror


def field_rotation(ephem, ts, data_dir, loc="Melbourne"):

    f_names = sorted([f for f in Path(data_dir).glob("*.tif")])
    loc = earth_loc(loc)
    lat = loc.latitude.degrees

    field_rot = {}
    field_rot["timestamp"] = []
    field_rot["alt"] = []
    field_rot["az"] = []
    field_rot["ror"] = []

    gps_t = []

    for f in f_names:
        timestamp = winjupos_time(ts, f)
        dt = timestamp.utc_datetime()
        gps = int(Time(dt).gps)
        alt, az = planet_vector(ephem, timestamp, loc)
        ror = rotation_rate(lat, alt, az)

        field_rot["timestamp"].append(dt)
        field_rot["alt"].append(alt)
        field_rot["az"].append(az)
        field_rot["ror"].append(ror)
        gps_t.append(gps)

    ΔT = np.array(gps_t) - gps_t[0]
    field_rot["delta_t"] = ΔT

    # Spline interpolate data to get smooth function for rotation rate
    f = InterpolatedUnivariateSpline(
        np.array(field_rot["delta_t"]), np.array(field_rot["ror"]), k=3
    )

    # Total rotation of each observation from the beginning of the night
    rot_tot = [f.integral(field_rot["delta_t"][0], i) for i in field_rot["delta_t"]]
    field_rot["rot_tot"] = rot_tot

    return field_rot


def rot_image(file=None, border=False, out_dir=None):

    img = read_tif(file=file)
    height, width, cc = img.shape

    if border:

        # border color
        ochre = [49408, 20480, 8448]
        img[:3] = ochre
        img[-3:] = ochre
        img[:, :3] = ochre
        img[:, -3:] = ochre

    # Maximum width/height of image with any rotation
    diag = math.ceil(np.sqrt(height ** 2 + width ** 2))

    black = (0, 0, 0)
    img_rot = np.full((diag, diag, cc), black, dtype=img.dtype)

    # compute center offset
    xx = (diag - width) // 2
    yy = (diag - height) // 2

    # copy img image into center of result image
    img_rot[yy : yy + height, xx : xx + width] = img

    write_tif(img_rot, file="sdkjfb.tif")


if __name__ == "__main__":

#    # Download Ephemerides & timescale files
#    load = Loader("ephemerides")
#    planets = load("de421.bsp")
#    ts = load.timescale()
#
#    # Solar System Ephemerides
#    sun = planets["sun"]
#    mercury = planets["mercury"]
#    venus = planets["venus"]
#    mars = planets["mars"]
#    earth = planets["earth"]
#    moon = planets["moon"]
#    jupiter = planets["jupiter barycenter"]
#    saturn = planets["saturn barycenter"]
#    uranus = planets["uranus barycenter"]
#    neptune = planets["neptune barycenter"]
#    pluto = planets["pluto barycenter"]
#
#    field_rot = field_rotation(
#        jupiter, ts, "/Users/amanchokshi/Documents/Photography/Frames", loc="Melbourne",
#    )
#
#    date_format = mpl_df("%H:%M")
#    plt.style.use("seaborn")
#    plt.plot_date(field_rot["timestamp"][::10], field_rot["rot_tot"][::10])
#    plt.gca().xaxis.set_major_formatter(date_format)
#    plt.tight_layout()
#    plt.show()

    rot_image(file="2020-09-03-1601_5-2020-09-03-1601_4-U-L-Mars_pipp_AS_F4000_lapl4_ap42_Drizzle15.tif", border=True)
