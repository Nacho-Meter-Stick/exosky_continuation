# Exosky
This was a project created at the Space Apps 2024 Hackathon.

Ever since the dawn of civilization humans have looked at the sky and dreamed of what's above. From the surface of our planet, it is easy to imagine that the sky is a dynamic curtain; an absolute. The night sky is something that is familiar, but only from the perspective of Earth. The "Exosky Explorer" aims to simulate an experience similar to our distant ancestors by generating a unique and interactive night sky view from the perspective of an exoplanet. Our program generates an accurate star chart based on any selected exoplanet's position in our galaxy and allows the user to create their own constellations from those star charts.

## Our Challenge
> "What would the night sky look like if you were standing on one of the many exoplanets discovered by astronomers and space missions? The list of 5500+ exoplanets at the NASA Exoplanet Archive can be combined with the latest star catalogs to translate the location and brightness of millions or even billions of stars to another perspective. From that perspective, anyone could use their imagination to draw constellations, much like our ancestors did on Earth thousands of years ago. Your challenge is to develop an app or interface for students that allows them to choose an exoplanet and then either display an interactive star chart or export a high-quality image for printing or viewing on a computer or virtual reality display, where they can draw and name constellations." - NASA Space Apps Challenge

## Our Project!
The Exosky Explorer extracts data from the Hipparcos (HIP) star catalog, and the Open Exoplanet Catalogue (which includes data from the NASA Exoplanet Archive). While different characteristics are extracted from both objects, their Right Ascension (RA), Declination (DEC), and parallax are extracted and converted using the same process.

In order to easily shift the sky map according to the parent exoplanet's position, (and for shifting the exoplanet's position alone) the Right Ascension, Declination, and parallax are converted into cartesian coordinates. Once the shift is complete, both are converted back into RA/DEC coordinates in order to display the objects as a sky chart.

The Exosky Explorer also accounts for:
- Apparent Magnitude: The size of the stars is enlarged according to their apparent magnitude, or how bright they would appear to an observer on Earth. The apparent magnitude is also shifted according to the position of any selected exoplanet, since a star's brightness will change depending on its distance to the viewer.

- Exoplanet Orbital Inclination: The inclination of an exoplanet's orbit (or the angle between the exoplanet's orbit and the plane of the sky) is corrected.

- Spectral Type: A star will be assigned a specific color based on its spectral type, or surface temperature.

The goal of Exosky Explorer is to create a more dynamic and interactive experience for the user. More interest in astronomy may be sparked by the inclusion of completely alien starscapes that almost nobody has seen before - and the ability to paint your own symbols into a unique night sky. Not only is it our hope that Exosky Explorer will help people become interested in the stars but also that it will challenge their perspective on the world. Many people find that astronomy is a humbling experience because there are so many things other than Earth and in the grand scheme of things Earth can seem so small. However, our project aims to expand people's worldviews by showing them what the sky would look like from worlds other than our own. 

Features that we would like to implement in the future mainly include more educational and informative tools. This could be in the form of hover boxes that appear when you click on a star that gives information such as star age and spectral type. Additionally, short descriptions of the exoplanets should be included in the user interface. The ability to zoom in on a star chart and to name the constellations that the user creates are additional features that we hope to implement in the future as well. 

## Resources Used
### Space Agency Data
[NASA Exoplanet Archive](https://exoplanetarchive.ipac.caltech.edu/index.html)

### Other References
- [Open Exoplanet Catalogue](https://github.com/OpenExoplanetCatalogue/open_exoplanet_catalogue)
- [Astroquery](https://github.com/cds-astro/astroquery)
- [The Hipparcos and Tycho Catalogues](https://www.cosmos.esa.int/web/hipparcos/catalogues)
- [VizieR Catalogue Access Tool](https://vizier.cds.unistra.fr/viz-bin/VizieR)
