from astropy.coordinates import spherical_to_cartesian
import pygame
from random import randint
import numpy as np
from database import buildSphericalDatabase, buildCartesianDatabase, getExoplanetData, findPlanet, shiftCartesianDatabase
from quaternions import normalized
from sphere_to_2circles import sphere_to_circle, cartesian_STAR_MAP_to_circles
from dropdown import SearchableDropDown
import math

# COLORS
ORANGE = (243, 146, 55)
DARK = (22, 21, 37)
DARK_PURPLE = (44, 42, 74)
PURPLE = (79, 81, 140)
LIGHT_PURPLE = (144, 122, 214)
LIGHT = (238, 227, 206)
DIM = (75, 75, 75)

spectral_color_dict = dict(
    O=(50, 21, 199),
    B=(168, 183, 242),
    A=(255, 255, 255),
    F=(240, 240, 200),
    G=(230, 230, 160),
    K=(230, 100, 50),
    M=(250, 30, 50),
)

spherical_database = buildSphericalDatabase()
star_database = buildCartesianDatabase(spherical_database)
print(star_database[0])

sol_pos = np.array([0,0,0], dtype=np.float64)

def generateSkySurface(width, height):
    sky_surface = pygame.Surface((width, height))

    projected_starmap = cartesian_STAR_MAP_to_circles(star_database)

    color_grid = DIM

    pos1 = (int(width/4), int(height/2))
    pos2 = (int(3*width/4), int(height/2))
    radius = int(width/4)

    pygame.draw.circle(sky_surface, color_grid, pos1, radius,1)
    pygame.draw.circle(sky_surface, color_grid, pos2, radius,1)
    
    ring = 1
    while ring < 6:
        pygame.draw.circle(sky_surface, color_grid, pos1, int(radius * math.tan(math.pi/4 - ring*math.pi/12)), 1)
        ring += 1
    ring = 1
    while ring < 6:
        pygame.draw.circle(sky_surface, color_grid, pos2, int(radius * math.tan(math.pi/4 - ring*math.pi/12)), 1)
        ring += 1
    for i in range(12):
        pygame.draw.line(sky_surface, color_grid, (pos1), 
                         (int(radius * math.cos(2*math.pi/12 * i)) + pos1[0], 
                          int(radius * math.sin(2*math.pi/12 * i)) + pos1[1]), 1)
    for i in range(12):
        pygame.draw.line(sky_surface, color_grid, (pos2), 
                         (int(radius * math.cos(2*math.pi/12 * i)) + pos2[0], 
                          int(radius * math.sin(2*math.pi/12 * i)) + pos2[1]), 1)
    
    # Draw north
    for entry in projected_starmap[0]:
        if len(entry['spectra']) == 0: color = LIGHT
        else: color = spectral_color_dict.get(entry['spectra'][0], LIGHT)
        if (entry['magnitude'] <= 10):
            x,y,z = entry['coordinates']
            mag = int(6-entry['magnitude'])

            x *= int(width/4)
            y *= -int(width/4)
            x += int(width/4)
            y += int(height/2)

            x = int(x)
            y = int(y)

            coord = (x,y)

            pygame.draw.circle(surface=sky_surface, color=color, center=coord, radius=mag, width=0)
    for entry in projected_starmap[1]:
        if len(entry['spectra']) == 0: color = LIGHT
        else: color = spectral_color_dict.get(entry['spectra'][0], LIGHT)

        if (entry['magnitude'] <= 10):
            x,y,z = entry['coordinates']
            mag = int(6-entry['magnitude'])

            x *= int(width/4)
            y *= -int(width/4)
            x += int(3*width/4)
            y += int(height/2)

            x = int(x)
            y = int(y)

            coord = (x,y)
            pygame.draw.circle(surface=sky_surface, color=color, center=coord, radius=mag, width=0)
    return sky_surface

white = (255, 255, 255)
pygame.init()
start_font = pygame.font.Font('./programFonts/Cascadia.ttf', 90)
planet_font = pygame.font.Font('./programFonts/Cascadia.ttf', 40)
title_text = start_font.render('Exosky Explorer!', False, '#907AD6')
start_text = start_font.render('Start', False, '#EEE3CE')
switch_text = planet_font.render('Switch Planets', False, '#2C2A4A')
exit_text = planet_font.render('Exit', False, '#2C2A4A')
save_text = planet_font.render('Save', False, '#2C2A4A')
undo_text = planet_font.render('Undo', False, '#2C2A4A')
pygame.display.set_caption('Exosky!')

window_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) #or pygame.FULLSCREEN to have the window stay fullscreen (no bar at top) Two numbers indicate minimized size
size = pygame.display.get_window_size()
background = pygame.Surface((size[0], size[1]))
sky_surface = generateSkySurface(size[0], size[1])
background.fill(pygame.Color('#161525'))

pos = (-1, -1)
mapping = False
start = False
saving = False
check = True
planet_str = "Earth"
constellation_str = 'Start Charting'
arr = []
temp_len = 0
border_margin = 10
text_margin = 10
radii = 3

planets = getExoplanetData()
planetNames = []
for planet in planets:
    planetNames.append(planet['name'])

dimensions = (355, 60)
exoPlanetSelector = SearchableDropDown(
    [ORANGE, PURPLE],
    [PURPLE, LIGHT_PURPLE],
    DARK,
    ORANGE,
    size[0]-dimensions[0]-border_margin*3, border_margin, dimensions[0], dimensions[1],
    planetNames,
    size)



while True:
    window_surface.blit(background, (0, 0))
    window_surface.blit(sky_surface, (0,0))

    # planet_text = planet_font.render(planet_str, False, '#F39237')
    constellation_text = planet_font.render(constellation_str, False, '#2C2A4A')
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if(mapping):
                check = True
                if(pos[0] != -1):
                    arr.append(pos[0]);arr.append(pos[1]);arr.append(pygame.mouse.get_pos()[0]);arr.append(pygame.mouse.get_pos()[1])
                else:
                    check = False
            pos = pygame.mouse.get_pos()

    text_width = title_text.get_width()
    text_height = title_text.get_height()
    window_surface.blit(title_text, (size[0]/2-text_width/2, text_margin))
    if not(start):
        
        text_width = start_text.get_width()
        text_height = start_text.get_height()
        dimensions = (text_width+2*text_margin, text_height+2*text_margin)
        start_button = pygame.draw.rect(window_surface,'#F39237', pygame.Rect(size[0]/2 - dimensions[0]/2, size[1] - dimensions[1]-border_margin, dimensions[0], dimensions[1]),  0, radii)
        window_surface.blit(start_text, (size[0]/2 - text_width/2,  size[1] - dimensions[1] - border_margin + text_margin))
        if start_button.collidepoint(pos):
            start = True
    else:
        #text_rect = planet_text.get_rect(center=(size[0]/2, 120))
        #window_surface.blit(planet_text, text_rect)
        if not(saving):
            exoPlanetSelector.draw(window_surface)
            
            text_width = constellation_text.get_width()
            text_height = constellation_text.get_height()
            dimensions = (text_width+2*text_margin, text_height+2*text_margin)
            constellation_button = pygame.draw.rect(window_surface, '#F39237', pygame.Rect(border_margin*3, border_margin, dimensions[0], dimensions[1]), 0, radii)
            window_surface.blit(constellation_text, (border_margin*3+text_margin, border_margin+text_margin))
            
            text_width = exit_text.get_width()
            text_height = exit_text.get_height()
            dimensions = (text_width+2*text_margin, text_height+2*text_margin)
            exit_button = pygame.draw.rect(window_surface, '#F39237', pygame.Rect(border_margin*3, size[1] - dimensions[1] - border_margin, dimensions[0], dimensions[1]), 0, radii)
            window_surface.blit(exit_text, (border_margin*3+text_margin, size[1] - dimensions[1]-border_margin + text_margin))
            
            text_width = save_text.get_width()
            text_height = save_text.get_height()
            dimensions = (text_width+2*text_margin, text_height+2*text_margin)
            save_button = pygame.draw.rect(window_surface, '#F39237', pygame.Rect(size[0] - dimensions[0] - border_margin*3, size[1] - dimensions[1]-border_margin, dimensions[0], dimensions[1]),  0, radii)
            window_surface.blit(save_text, (size[0] - dimensions[0] - border_margin*3+text_margin,  size[1] - dimensions[1]-border_margin + text_margin))

        changed = exoPlanetSelector.update(event_list)
        if changed:
            planet = findPlanet(planets, exoPlanetSelector.getChosen())
            right_ascension = planet['rightascension']
            declination = planet['declination']
            distance = planet['distance']
            offset_vec = np.array(spherical_to_cartesian(distance, declination, right_ascension), dtype=np.float64)
            star_database = shiftCartesianDatabase(star_database, np.add(offset_vec,sol_pos))
            sol_pos = -offset_vec

            sky_surface = generateSkySurface(size[0], size[1])

        if constellation_button.collidepoint(pos):
            if constellation_str == 'Start Charting':
                constellation_str = 'End Charting'
                mapping = True
                temp_len = len(arr)
            else:
                constellation_str = 'Start Charting'
                mapping = False
                if temp_len != len(arr) and check:
                    arr.pop();arr.pop();arr.pop();arr.pop();
            pos = (-1, -1)
        if mapping:
            text_width = undo_text.get_width()
            text_height = undo_text.get_height()
            dimensions = (text_width+2*text_margin, text_height+2*text_margin)
            text_width = constellation_text.get_width()
            text_height = constellation_text.get_height()
            dimensions2 = (text_width+2*text_margin, text_height+2*text_margin)
            undo_button = pygame.draw.rect(window_surface, '#F39237', pygame.Rect(border_margin*3, dimensions2[1]+2*border_margin, dimensions[0], dimensions[1]), 0, radii)
            window_surface.blit(undo_text, (border_margin*3+text_margin, dimensions2[1]+2*border_margin+text_margin))
            
            if undo_button.collidepoint(pos) and len(arr) >= 4:
                if check:
                    arr.pop();arr.pop();arr.pop();arr.pop();
                if(len(arr) >= 4):
                   pos = (arr[len(arr)-4], arr[len(arr)-3])
                   arr.pop();arr.pop();arr.pop();arr.pop()
                   if len(arr) == 0:
                       pos = (-1, -1)
                else:
                    pos = (-1, -1)
                check = False
            elif undo_button.collidepoint(pos):
                pos = (-1, -1)
        if exit_button.collidepoint(pos):
            exit()
        j = 0;
        for i in range(int(len(arr)/4)):
            pygame.draw.line(window_surface, '#F39237', (arr[j], arr[j+1]), (arr[j+2], arr[j+3]), 3)
            j+=4
        if saving:
            pygame.image.save(window_surface, "image.png")
            saving = False
        if save_button.collidepoint(pos):
            saving = True
            pos = (-1, -1)
    pygame.display.update()
