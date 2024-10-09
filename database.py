import csv
import math
from astropy.coordinates import spherical_to_cartesian
import numpy as np
import numpy.typing as npt

import xml.etree.ElementTree as ET, urllib.request, gzip, io

url = "https://github.com/OpenExoplanetCatalogue/oec_gzip/raw/master/systems.xml.gz"
oec = ET.parse(gzip.GzipFile(fileobj=io.BytesIO(urllib.request.urlopen(url).read())))

STAR_ENTRY_TYPE = np.dtype([('identifier', 'U15'), ('coordinates', np.float32, (3)), ('magnitude', np.float32), ('spectra', 'U15')])

def delta_star_magnitude(d1_squared: float, d2_squared: float) -> float:
    # delta_m = 5 * math.log(d2)/math.log(10) - 5 * math.log(d1)/math.log(10)
    # delta_m = 2.5 * math.log(d2_squared/d1_squared)/math.log(10)
    return 2.5*math.log(d2_squared/d1_squared)/math.log(10)

def convertHMSToRad(HMSstr: str) -> np.float32:
    H, M, S = HMSstr.split(" ")
    return (np.float32(H) * math.pi / 12
         + np.float32(M) * math.pi / (12*60)
         + np.float32(S) * math.pi / (12*60*60))

def convertDMSToRad(DMSstr: str) -> np.float32:
    D, M, S = DMSstr.split(" ")
    return (np.float32(D) * math.pi / 180
         + np.float32(M) * math.pi / (180*60)
         + np.float32(S) * math.pi / (180*60*60))

def getExoplanetData():
    planets = []
    for system in oec.findall(".//system"):
        systemDist = system.findtext("distance")
        try:
            if type(systemDist) is None or float(systemDist[0]) > 600:
                continue
        except:
            continue
        systemRightAscension = convertHMSToRad(str(system.findtext("rightascension")))
        systemDeclination = convertDMSToRad(str(system.findtext("declination")))
        for planet in system.findall(".//planet"):
            try:
                planetdict = dict(
                    name = planet.findtext("name"),
                    inclination = float(planet.findtext("inclination")),
                    periastron = float(planet.findtext("periastron")),
                    distance = float(systemDist),
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
        description = "Home. Discovered by humanity et al."))
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

def ShiftedCartesianDatabase(cartesian_database: npt.NDArray, new_origin: npt.NDArray[np.float32]) -> npt.NDArray:
    new_database = np.copy(cartesian_database)
    for entry in new_database:
        dist_sqr = np.sum(np.square(entry['coordinates']))
        entry['coordinates'] = entry['coordinates'] - new_origin
        new_dist_sqr = np.sum(np.square(entry['coordinates']))
        entry['magnitude'] += delta_star_magnitude(dist_sqr, new_dist_sqr)
    return new_database

def filterStarDatabase(star_database: npt.NDArray, max_magnitude: np.float32):
    starslist: list[tuple] = []
    for entry in star_database:
        if entry['magnitude'] > max_magnitude:
            continue
        starslist.append(entry)

    stars = np.array(starslist, dtype=STAR_ENTRY_TYPE)
    return stars
