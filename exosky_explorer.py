from astropy.coordinates import spherical_to_cartesian
import pygame
import numpy as np
from database import buildSphericalDatabase, buildCartesianDatabase, getExoplanetData, findPlanet, ShiftedCartesianDatabase
from projection import cartesian_STAR_MAP_to_circles
from dropdown import SearchableDropDown
import math
import numpy.typing as npt

pygame.init()

# COLORS
ORANGE = (243, 146, 55)
DARK = (22, 21, 37)
DARK_PURPLE = (44, 42, 74)
PURPLE = (79, 81, 140)
LIGHT_PURPLE = (144, 122, 214)
LIGHT = (238, 227, 206)
DIM = (75, 75, 75)
BUTTON_COLOR = '#F39237'
CONSTELLATION_COLOR = '#F39237'

SPECTRAL_COLOR_DICT = {
    'O' : (50, 21, 199),
    'B' : (168, 183, 242),
    'A' : (255, 255, 255),
    'F' : (240, 240, 200),
    'G' : (230, 230, 160),
    'K' : (230, 100, 50),
    'M' : (250, 30, 50)
}

PLANETS = getExoplanetData()
PLANET_NAMES = [planet['name'] for planet in PLANETS]
STAR_DATABASE = buildCartesianDatabase(buildSphericalDatabase())

def unit_vec(angle):
    return np.array((math.cos(angle), math.sin(angle)))
def int_vec(vec: npt.NDArray):
    return np.array((int(vec[0]), int(vec[1])))
def generateSkySurface(width, height, y_pos, cartesian_star_map):
    sky_surface = pygame.Surface((width, height))

    projected_starmap = cartesian_STAR_MAP_to_circles(cartesian_star_map)

    color_grid = DIM

    pos1 = (int(width/4), y_pos)
    pos2 = (int(3*width/4), y_pos)
    radius = int(width/4)

    pygame.draw.circle(sky_surface, color_grid, pos1, radius, 1)
    pygame.draw.circle(sky_surface, color_grid, pos2, radius, 1)
    
    for ring in range(1, 6):
        pygame.draw.circle(sky_surface, color_grid, pos1, int(radius * math.tan(math.pi/4 - ring*math.pi/12)), 1)
        pygame.draw.circle(sky_surface, color_grid, pos2, int(radius * math.tan(math.pi/4 - ring*math.pi/12)), 1)
    for i in range(12):
        pygame.draw.line(sky_surface, color_grid, pos1, int_vec(radius*unit_vec(2*math.pi/12 * i) + np.array(pos1)), 1)
        pygame.draw.line(sky_surface, color_grid, pos2, int_vec(radius*unit_vec(2*math.pi/12 * i) + np.array(pos2)), 1)
    
    # Draw northern hemisphere
    for entry in projected_starmap[0]:
        if len(entry['spectra']) == 0: color = LIGHT
        else: color = SPECTRAL_COLOR_DICT.get(entry['spectra'][0], LIGHT)
        if (entry['magnitude'] <= 10):
            mag = int(6-entry['magnitude'])
            x, y, _ = entry['coordinates']

            x = int(x*radius + pos1[0])
            y = int(-y*radius + pos1[1])

            pygame.draw.circle(surface=sky_surface, color=color, center=(x,y), radius=mag, width=0)
    # Draw southern hemisphere
    for entry in projected_starmap[1]:
        if len(entry['spectra']) == 0: color = LIGHT
        else: color = SPECTRAL_COLOR_DICT.get(entry['spectra'][0], LIGHT)

        if (entry['magnitude'] <= 10):
            mag = int(6-entry['magnitude'])
            x, y, _ = entry['coordinates']

            x = int(x*radius + pos2[0])
            y = int(-y*radius + pos2[1])

            pygame.draw.circle(surface=sky_surface, color=color, center=(x,y), radius=mag, width=0)
    return sky_surface

window_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SIZE = pygame.display.get_window_size()
BACKGROUND = pygame.Surface((SIZE[0], SIZE[1]), masks=pygame.Color('#161525'))
sky_surface = generateSkySurface(SIZE[0], SIZE[1], SIZE[1]-SIZE[0]/4, STAR_DATABASE)

BORDER_MARGIN = 10
TEXT_MARGIN = 10
BORDER_RADIUS = 3

START_FONT = pygame.font.Font('./programFonts/Cascadia.ttf', 90)
PLANET_FONT = pygame.font.Font('./programFonts/Cascadia.ttf', 40)
switch_text = PLANET_FONT.render('Switch Planets', False, '#2C2A4A')

##################################################################################################
TITLE_TEXT = START_FONT.render('Exosky Explorer!', False, '#907AD6')

TITLE_TEXT_WIDTH = TITLE_TEXT.get_width()
TITLE_TEXT_HEIGHT = TITLE_TEXT.get_height()
TITLE_TEXT_POS = (SIZE[0]/2-TITLE_TEXT_WIDTH/2, TEXT_MARGIN)
##################################################################################################
class Button():
    def __init__(self, TEXT, RECT_POS):
        self.dims = (TEXT.get_width() + 2*TEXT_MARGIN, TEXT.get_width() + 2*TEXT_MARGIN)
        self.rect = pygame.Rect(RECT_POS[0], RECT_POS[1], self.dims[0], self.dims[1])
        self.rect_pos = RECT_POS
        self.text = TEXT
        self.text_pos = (RECT_POS[0] + TEXT_MARGIN, RECT_POS[1] + TEXT_MARGIN)
    def draw_on(self, surf):
        pygame.draw.rect(surf, BUTTON_COLOR, self.rect, 0, BORDER_RADIUS)
        window_surface.blit(self.text, self.text_pos)
    def collidepoint(self, pos):
        return self.rect.collidepoint(pos)
##################################################################################################
START_TEXT = START_FONT.render('Start', False, '#EEE3CE')
START_DIMENSIONS = (START_TEXT.get_width() + 2*TEXT_MARGIN, 
                    START_TEXT.get_height() + 2*TEXT_MARGIN)
START_RECT_POS = (SIZE[0]/2 - START_DIMENSIONS[0]/2, 
                  SIZE[1] - START_DIMENSIONS[1] - BORDER_MARGIN)
START_BUTTON = Button(START_TEXT, START_RECT_POS)
##################################################################################################
EXIT_TEXT = PLANET_FONT.render('Exit', False, '#2C2A4A')
EXIT_DIMENSIONS = (EXIT_TEXT.get_width()+2*TEXT_MARGIN, 
                    EXIT_TEXT.get_height()+2*TEXT_MARGIN)
EXIT_RECT_POS = (BORDER_MARGIN*3, 
                 SIZE[1] - EXIT_DIMENSIONS[1] - BORDER_MARGIN)
EXIT_BUTTON = Button(EXIT_TEXT, EXIT_RECT_POS)
##################################################################################################
SAVE_TEXT = PLANET_FONT.render('Save', False, '#2C2A4A')
SAVE_DIMENSIONS = (SAVE_TEXT.get_width()+2*TEXT_MARGIN, 
                    SAVE_TEXT.get_height()+2*TEXT_MARGIN)
SAVE_RECT_POS = (SIZE[0] - SAVE_DIMENSIONS[0] - BORDER_MARGIN*3, 
                 SIZE[1] - SAVE_DIMENSIONS[1] - BORDER_MARGIN)
SAVE_BUTTON = Button(SAVE_TEXT, SAVE_RECT_POS)
##################################################################################################
START_CHARTING_TEXT = PLANET_FONT.render('Start Charting', False, '#2C2A4A')
START_CHARTING_DIMENSIONS = (START_CHARTING_TEXT.get_width()+2*TEXT_MARGIN, 
                             START_CHARTING_TEXT.get_height()+2*TEXT_MARGIN)
START_CHARTING_RECT_POS = (BORDER_MARGIN*3, BORDER_MARGIN)
START_CHARTING_BUTTON = Button(START_CHARTING_TEXT, START_CHARTING_RECT_POS)
##################################################################################################
END_CHARTING_TEXT = PLANET_FONT.render('End Charting', False, '#2C2A4A')
END_CHARTING_DIMENSIONS = (END_CHARTING_TEXT.get_width()+2*TEXT_MARGIN, 
                             END_CHARTING_TEXT.get_height()+2*TEXT_MARGIN)
END_CHARTING_RECT_POS = (BORDER_MARGIN*3, BORDER_MARGIN)
END_CHARTING_BUTTON = Button(END_CHARTING_TEXT, END_CHARTING_RECT_POS)
##################################################################################################
UNDO_TEXT = PLANET_FONT.render('Undo', False, '#2C2A4A')
UNDO_DIMENSIONS = (UNDO_TEXT.get_width()+2*TEXT_MARGIN, 
                    UNDO_TEXT.get_height()+2*TEXT_MARGIN)
UNDO_RECT_POS = (BORDER_MARGIN*3, 
                 END_CHARTING_DIMENSIONS[1]+2*BORDER_MARGIN)
UNDO_BUTTON = Button(UNDO_TEXT, UNDO_RECT_POS)
##################################################################################################
pygame.display.set_caption('Exosky!')
user_be_drawing = False
saving = False

def undo(constellations, planetName):
    if constellations[planetName]: 
        if len(constellations[planetName][-1]) == 0: 
            constellations[planetName].pop()
        elif len(constellations[planetName]) > 1: 
            constellations[planetName][-1].pop()
def draw_constellations(constellations, planetName, surface):
    for chain in constellations[planetName]:
        for i in range(len(chain)-1):
            pygame.draw.line(surface, CONSTELLATION_COLOR, chain[i], chain[i+1], 3)

EXOPLANETSELECTOR_DIMENSIONS = (355, 60)
exoPlanetSelector = SearchableDropDown(
    [ORANGE, PURPLE],
    [PURPLE, LIGHT_PURPLE],
    DARK,
    ORANGE,
    SIZE[0]-EXOPLANETSELECTOR_DIMENSIONS[0]-BORDER_MARGIN*3, 
    BORDER_MARGIN, 
    EXOPLANETSELECTOR_DIMENSIONS[0], 
    EXOPLANETSELECTOR_DIMENSIONS[1],
    PLANET_NAMES,
    SIZE
)
planetName = exoPlanetSelector.getChosen()
'''
Heres how constellations are going to work.
Its going to be a list of lists of tuples. The tuples are pixel coordinates.
Each row is going to be a chain. So anytime you 'pick the pen up and put it back down',
you end the last row and append a new empty row.

Not only that, but every planet is going to have its own unique list of lists. 
So really, constellations is a dict of these 2d lists.
Yes, there are many planets, and this could become a memory problem. 
But the amount of time you would have to spend waiting for the 'switch planet' function to work would be literally insane.
'''

constellations: dict[str, list[list[tuple[int, int]]]] = {planetName: [[]]}
################################### Loop on start screen #####################################
while True:
    window_surface.blit(BACKGROUND, (0, 0))
    window_surface.blit(sky_surface, (0, 0))
    window_surface.blit(TITLE_TEXT, TITLE_TEXT_POS)
    event_list = pygame.event.get()
    start = False
    for event in event_list:
        if event.type == pygame.MOUSEBUTTONDOWN and START_BUTTON.collidepoint(event.pos):
            start = True
            break
    if start: break
    START_BUTTON.draw_on(window_surface)
    pygame.display.update()
###################################  USER HAS DECIDED TO START THE GAME  #####################################
while True:
    ###################################  PROCESS EVENTS  #####################################
    event_list = pygame.event.get()
    for event in event_list:
        if event.type != pygame.MOUSEBUTTONDOWN: continue
        pos = event.pos
        if EXIT_BUTTON.collidepoint(pos): exit()
        elif SAVE_BUTTON.collidepoint(pos): saving = True
        elif user_be_drawing:
            if END_CHARTING_BUTTON.collidepoint(pos): user_be_drawing = False
            elif UNDO_BUTTON.collidepoint(pos): undo(constellations, planetName)
            elif exoPlanetSelector.pos_is_not_on_menu(pos): constellations[planetName][-1].append(pos)
        elif START_CHARTING_BUTTON.collidepoint(pos):
            user_be_drawing = True
            constellations[planetName].append([])

    demand_to_change_planet = exoPlanetSelector.update(event_list)
    if demand_to_change_planet:
        constellations[planetName].append([])
        planetName = exoPlanetSelector.getChosen()
        planet = findPlanet(PLANETS, planetName)
        if planetName not in constellations: constellations[planetName] = [[]]
        offset_vec = np.array(spherical_to_cartesian(planet['distance'], 
                                                     planet['declination'], 
                                                     planet['rightascension']), dtype=np.float64)
        # Turns out, the shiftCartesianDatabase() function was creating a deepcopy every time anyways.
        # And besides, we really do not want to try to do that weird relativity thing if we ever do rotations.
        sky_surface = generateSkySurface(SIZE[0], SIZE[1], SIZE[1]-SIZE[0]/4, ShiftedCartesianDatabase(STAR_DATABASE, offset_vec))
    #############################  Add main view before saving  ##########################
    window_surface.blit(BACKGROUND, (0, 0))
    window_surface.blit(sky_surface, (0, 0))
    draw_constellations(constellations, planetName, window_surface)
    ##################  Save screen before reloading buttons if needed  ##################
    if saving: # In this case, we actually want the planet name up a bit higher
        exoPlanetSelector.draw_planetName_on(window_surface, y=TEXT_MARGIN)
        pygame.image.save(window_surface, "image.png")
        saving = False
    else:
        exoPlanetSelector.draw_planetName_on(window_surface)
    ##############  Reload title, buttons, dropdown menu, and constellations  #############
    window_surface.blit(TITLE_TEXT, TITLE_TEXT_POS)
    exoPlanetSelector.draw_dropdown_on(window_surface)
    EXIT_BUTTON.draw_on(window_surface)
    SAVE_BUTTON.draw_on(window_surface)
    if not user_be_drawing:
        START_CHARTING_BUTTON.draw_on(window_surface)
    if user_be_drawing:
        END_CHARTING_BUTTON.draw_on(window_surface)
        UNDO_BUTTON.draw_on(window_surface)
    pygame.display.update() # Start next frame