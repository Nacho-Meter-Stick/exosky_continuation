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
START_TEXT = START_FONT.render('Start', False, '#EEE3CE')

START_TEXT_WIDTH = START_TEXT.get_width()
START_TEXT_HEIGHT = START_TEXT.get_height()
START_DIMENSIONS = (START_TEXT_WIDTH+2*TEXT_MARGIN, 
                    START_TEXT_HEIGHT+2*TEXT_MARGIN)
START_RECT = pygame.Rect(SIZE[0]/2 - START_DIMENSIONS[0]/2, 
                         SIZE[1] - START_DIMENSIONS[1]-BORDER_MARGIN, 
                         START_DIMENSIONS[0], START_DIMENSIONS[1])
START_TEXT_POS = (SIZE[0]/2 - START_TEXT_WIDTH/2, 
                  SIZE[1] - START_DIMENSIONS[1] - BORDER_MARGIN + TEXT_MARGIN)
##################################################################################################
EXIT_TEXT = PLANET_FONT.render('Exit', False, '#2C2A4A')

EXIT_DIMENSIONS = (EXIT_TEXT.get_width()+2*TEXT_MARGIN, 
                    EXIT_TEXT.get_height()+2*TEXT_MARGIN)
EXIT_RECT = pygame.Rect(BORDER_MARGIN*3, 
                        SIZE[1] - EXIT_DIMENSIONS[1] - BORDER_MARGIN, 
                        EXIT_DIMENSIONS[0], EXIT_DIMENSIONS[1])

EXIT_TEXT_POS = (BORDER_MARGIN*3+TEXT_MARGIN, 
                 SIZE[1] - EXIT_DIMENSIONS[1] - BORDER_MARGIN + TEXT_MARGIN)
##################################################################################################
SAVE_TEXT = PLANET_FONT.render('Save', False, '#2C2A4A')

SAVE_DIMENSIONS = (SAVE_TEXT.get_width()+2*TEXT_MARGIN, 
                    SAVE_TEXT.get_height()+2*TEXT_MARGIN)
SAVE_RECT = pygame.Rect(SIZE[0] - SAVE_DIMENSIONS[0] - BORDER_MARGIN*3, 
                        SIZE[1] - SAVE_DIMENSIONS[1] - BORDER_MARGIN, 
                        SAVE_DIMENSIONS[0], SAVE_DIMENSIONS[1])
SAVE_TEXT_POS = (SIZE[0] - SAVE_DIMENSIONS[0] - BORDER_MARGIN*3+TEXT_MARGIN,  
                 SIZE[1] - SAVE_DIMENSIONS[1] - BORDER_MARGIN + TEXT_MARGIN)
##################################################################################################
START_CHARTING_TEXT = PLANET_FONT.render('Start Charting', False, '#2C2A4A')
START_CHARTING_DIMENSIONS = (START_CHARTING_TEXT.get_width()+2*TEXT_MARGIN, 
                             START_CHARTING_TEXT.get_height()+2*TEXT_MARGIN)
START_CHARTING_RECT = pygame.Rect(BORDER_MARGIN*3, BORDER_MARGIN, 
                                 START_CHARTING_DIMENSIONS[0], 
                                 START_CHARTING_DIMENSIONS[1])
START_CHARTING_TEXT_POS = (BORDER_MARGIN*3+TEXT_MARGIN, 
                           BORDER_MARGIN+TEXT_MARGIN)
##################################################################################################
END_CHARTING_TEXT = PLANET_FONT.render('End Charting', False, '#2C2A4A')
END_CHARTING_DIMENSIONS = (END_CHARTING_TEXT.get_width()+2*TEXT_MARGIN, 
                             END_CHARTING_TEXT.get_height()+2*TEXT_MARGIN)
END_CHARTING_RECT = pygame.Rect(BORDER_MARGIN*3, BORDER_MARGIN, 
                                END_CHARTING_DIMENSIONS[0], 
                                END_CHARTING_DIMENSIONS[1])
END_CHARTING_TEXT_POS = (BORDER_MARGIN*3+TEXT_MARGIN, 
                         BORDER_MARGIN+TEXT_MARGIN)
##################################################################################################
UNDO_TEXT = PLANET_FONT.render('Undo', False, '#2C2A4A')

UNDO_DIMENSIONS = (UNDO_TEXT.get_width()+2*TEXT_MARGIN, 
                    UNDO_TEXT.get_height()+2*TEXT_MARGIN)
UNDO_RECT = pygame.Rect(BORDER_MARGIN*3, 
                        END_CHARTING_DIMENSIONS[1]+2*BORDER_MARGIN, 
                        UNDO_DIMENSIONS[0], UNDO_DIMENSIONS[1])
UNDO_TEXT_POS = (BORDER_MARGIN*3+TEXT_MARGIN, 
                 END_CHARTING_DIMENSIONS[1]+2*BORDER_MARGIN+TEXT_MARGIN)
##################################################################################################
pygame.display.set_caption('Exosky!')
user_be_drawing = False
saving = False

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
constellations = {planetName: [[]]}
################################### Loop on start screen #####################################
while True:
    window_surface.blit(BACKGROUND, (0, 0))
    window_surface.blit(sky_surface, (0, 0))
    window_surface.blit(TITLE_TEXT, TITLE_TEXT_POS)
    event_list = pygame.event.get()
    start = False
    for event in event_list:
        if event.type == pygame.MOUSEBUTTONDOWN and START_RECT.collidepoint(event.pos):
            start = True
            break
    if start: break
    # START BUTTON
    start_button = pygame.draw.rect(window_surface, BUTTON_COLOR, START_RECT,  0, BORDER_RADIUS)
    window_surface.blit(START_TEXT, START_TEXT_POS)

    pygame.display.update()
###################################  USER HAS DECIDED TO START THE GAME  #####################################
def undo(constellations_planetName):
    if (constellations_planetName): 
        if len(constellations_planetName[-1]) == 0: 
            constellations_planetName.pop()
            undo(constellations_planetName)
        elif len(constellations_planetName) > 1: 
            constellations_planetName[-1].pop()
while True:
    ###################################  PROCESS EVENTS  #####################################
    event_list = pygame.event.get()
    for event in event_list:
        if event.type != pygame.MOUSEBUTTONDOWN: continue
        pos = event.pos
        if EXIT_RECT.collidepoint(pos): exit()
        elif SAVE_RECT.collidepoint(pos): saving = True
        elif user_be_drawing:
            if END_CHARTING_RECT.collidepoint(pos): user_be_drawing = False
            elif UNDO_RECT.collidepoint(pos):
                undo(constellations[planetName])
            elif exoPlanetSelector.pos_is_not_on_menu(pos): constellations[planetName][-1].append(pos)
        elif START_CHARTING_RECT.collidepoint(pos):
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
        sky_surface = generateSkySurface(SIZE[0], SIZE[1], SIZE[1]-SIZE[0]/4, ShiftedCartesianDatabase(STAR_DATABASE, offset_vec))
        

    #############################  Add main view before saving  ##########################
    window_surface.blit(BACKGROUND, (0, 0))
    window_surface.blit(sky_surface, (0, 0))
    for chain in constellations[planetName]:
        for i in range(len(chain)-1):
            pygame.draw.line(window_surface, CONSTELLATION_COLOR, chain[i], chain[i+1], 3)
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
    # EXIT BUTTON
    pygame.draw.rect(window_surface, BUTTON_COLOR, EXIT_RECT, 0, BORDER_RADIUS)
    window_surface.blit(EXIT_TEXT, EXIT_TEXT_POS)
    # SAVE BUTTON
    pygame.draw.rect(window_surface, BUTTON_COLOR, SAVE_RECT,  0, BORDER_RADIUS)
    window_surface.blit(SAVE_TEXT, SAVE_TEXT_POS)

    if not user_be_drawing:
        # START CHARTING BUTTON
        pygame.draw.rect(window_surface, BUTTON_COLOR, START_CHARTING_RECT, 0, BORDER_RADIUS)
        window_surface.blit(START_CHARTING_TEXT, START_CHARTING_TEXT_POS)
    if user_be_drawing:
        # END CHARTING BUTTON
        pygame.draw.rect(window_surface, BUTTON_COLOR, END_CHARTING_RECT, 0, BORDER_RADIUS)
        window_surface.blit(END_CHARTING_TEXT, END_CHARTING_TEXT_POS)
        # UNDO BUTTON
        pygame.draw.rect(window_surface, BUTTON_COLOR, UNDO_RECT, 0, BORDER_RADIUS)
        window_surface.blit(UNDO_TEXT, UNDO_TEXT_POS)
    pygame.display.update()