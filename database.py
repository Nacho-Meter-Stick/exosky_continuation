import csv
import math
from astropy.coordinates import spherical_to_cartesian
import numpy as np
import numpy.typing as npt
import matplotlib.pyplot as plt
from star_mag import delta_star_magnitude

import xml.etree.ElementTree as ET, urllib.request, gzip, io

url = "https://github.com/OpenExoplanetCatalogue/oec_gzip/raw/master/systems.xml.gz"
oec = ET.parse(gzip.GzipFile(fileobj=io.BytesIO(urllib.request.urlopen(url).read())))

STAR_ENTRY_TYPE = np.dtype([('identifier', 'U15'), ('coordinates', np.float32, (3)), ('magnitude', np.float32), ('spectra', 'U15')])

def convertHMSToRad(HMSstr: str) -> np.float32:
    HMSparts = HMSstr.split(" ")
    return np.float32(HMSparts[0]) * math.pi / 12 \
         + np.float32(HMSparts[1]) * math.pi / 12 / 60 \
         + np.float32(HMSparts[2]) * math.pi / 12 / 60 / 60

def convertDMSToRad(DMSstr: str) -> np.float32:
    DMSparts = DMSstr.split(" ")
    return np.float32(DMSparts[0]) * math.pi / 180 \
         + np.float32(DMSparts[1]) * math.pi / 180 / 60 \
         + np.float32(DMSparts[2]) * math.pi / 180 / 60 / 60

def getExoplanetData():
    planets = []
    for system in oec.findall(".//system"):
        systemDist = system.findtext("distance")
        try:
            if type(systemDist) == None or float(systemDist[0]) > 600:
                continue
        except:
            continue
        systemDist = float(systemDist[0])
        systemRightAscension = convertHMSToRad(str(system.findtext("rightascension")))
        systemDeclination = convertDMSToRad(str(system.findtext("declination")))
        for planet in system.findall(".//planet"):
            try:
                planetdict = dict(
                    name = planet.findtext("name"),
                    inclination = float(planet.findtext("inclination")),
                    periastron = float(planet.findtext("periastron")),
                    distance = systemDist,
                    rightascension = systemRightAscension,
                    declination = systemDeclination,
                    description = planet.findtext("description")
                )
            except:
                continue 
            planets.append(planetdict)
    planets.append(dict(
        name = "Earth",
        inclination = 0,
        periastron = 0,
        distance = 0,
        rightascension = 0,
        declination = 0,
        description = "Home. Discovered by humanity et al."
    ))
    return planets

def findPlanet(planetData, planetName):
    for planet in planetData:
        if planet["name"] == planetName:
            return planet
    return -1

def buildSphericalDatabase() -> npt.NDArray:
    starslist: list[tuple] = []
    with open("HIP database.csv", mode="r") as HIP_database:
        csvFile = csv.DictReader(HIP_database)
        for lines in csvFile:
            if not str(lines.get("Distance (pc)")).replace('.', '1').isnumeric():
                continue

            RArad = convertHMSToRad(str(lines.get("RA (hms)")))
            DErad = convertDMSToRad(str(lines.get("DE (dms)")))

            coordinates = np.array([lines.get("Distance (pc)"), RArad, DErad], dtype=np.float32)
            starTuple = (
                lines.get("Designation"),
                coordinates,
                np.float64(lines.get("Magnitude (Vmag)")),
                lines.get("Spectral Type")
            )

            starslist.append(starTuple)
    stars = np.array(starslist, dtype=STAR_ENTRY_TYPE)

    return stars

def buildCartesianDatabase(spherical_database: npt.NDArray) -> npt.NDArray:
    star_database = np.copy(spherical_database)
    for entry in star_database:
        r, lon, lat = entry['coordinates']
        entry['coordinates'] = spherical_to_cartesian(r, lat, lon)
    return star_database

def shiftCartesianDatabase(cartesian_database: npt.NDArray, new_origin: npt.NDArray[np.float32]) -> npt.NDArray:
    for entry in cartesian_database:
        dist_sqr = np.sum(np.multiply(entry['coordinates'], entry['coordinates']))
        entry['coordinates'] = entry['coordinates'] - new_origin
        new_dist_sqr = np.sum(np.multiply(entry['coordinates'], entry['coordinates']))
        entry['magnitude'] += delta_star_magnitude(dist_sqr, new_dist_sqr)

    return cartesian_database

def filterStarDatabase(star_database: npt.NDArray, max_magnitude: np.float32):
    starslist: list[tuple] = []
    for entry in star_database:
        if entry['magnitude'] > max_magnitude:
            continue
        starslist.append(entry)

    stars = np.array(starslist, dtype=STAR_ENTRY_TYPE)
    return stars

planet_database = getExoplanetData()
star_database_spherical = buildSphericalDatabase()
star_database = buildCartesianDatabase(star_database_spherical)