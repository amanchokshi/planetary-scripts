from skyfield.api import Loader, Topos


def planet_vector(ephem, time, loc):
    loc = earth + loc
    astrometric = loc.at(time).observe(ephem)
    apparent = astrometric.apparent()
    alt, az, _ = apparent.altaz()
    print(alt.dstr())
    print(az.dstr())


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
    Melbourne = Topos('37.8142 S', '144.9632 E', elevation_m=43)

    planet_vector(jupiter, t, Melbourne)
