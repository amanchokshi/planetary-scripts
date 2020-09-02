from skyfield.api import load

planets = load('de421.bsp')

mercury = planets["MERCURY"]
venus = planets["VENUS"]
mars = planets["MARS"]
moon = planets["MOON"]
jupiter = planets["JUPITER BARYCENTER"]
saturn = planets["SATURN BARYCENTER"]
uranus = planets["URANUS BARYCENTER"]
neptune = planets["NEPTUNE BARYCENTER"]
pluto = planets["PLUTO BARYCENTER"]
