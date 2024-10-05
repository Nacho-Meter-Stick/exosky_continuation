import xml.etree.ElementTree as ET, urllib.request, gzip, io
url = "https://github.com/OpenExoplanetCatalogue/oec_gzip/raw/master/systems.xml.gz"
oec = ET.parse(gzip.GzipFile(fileobj=io.BytesIO(urllib.request.urlopen(url).read())))

def getExoplanetData():
    planets = []
    for system in oec.findall(".//system"):
        systemDist = system.findtext("distance"),
        systemRightAscension = system.findtext("rightascension"), 
        systemDeclination = system.findtext("declination")
        for planet in system.findall(".//planet"):
            planetdict = dict(
                name = planet.findtext("name"), 
                inclination = planet.findtext("inclination"),
                distance = systemDist,
                rightascension = systemRightAscension,
                declination = systemDeclination
            )
            planets.append(planetdict)
    return planets

database = getExoplanetData()
for planet in database:
    print(planet)