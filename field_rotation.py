from skyfield.api import Loader, Topos


# Download Ephemerides & timescale files
load = Loader("ephemerides")
planets = load("de421.bsp")
ts = load.timescale()
t = ts.now()


# Solar System Ephemerides
sun = planets['sun']
mercury = planets["mercury"]
venus = planets["venus"]
mars = planets["mars"]
earth = planets['earth']
moon = planets["moon"]
jupiter = planets["jupiter barycenter"]
saturn = planets["saturn barycenter"]
uranus = planets["uranus barycenter"]
neptune = planets["neptune barycenter"]
pluto = planets["pluto barycenter"]
