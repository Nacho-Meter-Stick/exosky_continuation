import pygame
from random import randint
import numpy as np
from database import buildSphericalDatabase, buildCartesianDatabase, getExoplanetData
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

def generateSkySurface(width, height):
    sky_surface = pygame.Surface((width, height))
    spherical_database = buildSphericalDatabase()
    star_database = buildCartesianDatabase(spherical_database)

    projected_starmap = cartesian_STAR_MAP_to_circles(star_database)

    color_grid = DIM
    color = LIGHT

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
        if (entry['magnitude'] <= 6):
            x,y,z = entry['coordinates']
            mag = int(6-entry['magnitude'])

            x *= int(width/4)
            y *= -int(width/4)
            x += int(width/4)
            y += int(height/2)

            coord = (x,y)

            pygame.draw.circle(surface=sky_surface, color=color, center=coord, radius=mag, width=0)
    for entry in projected_starmap[1]:
        if (entry['magnitude'] <= 6):
            x,y,z = entry['coordinates']
            mag = int(6-entry['magnitude'])

            x *= int(width/4)
            y *= -int(width/4)
            x += int(3*width/4)
            y += int(height/2)

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
planet_str = "Earth"
constellation_str = 'Start Charting'
arr = []
temp_len = 0

planets = getExoplanetData()
planetNames = []
for planet in planets:
    planetNames.append(planet['name'])

exoPlanetSelector = SearchableDropDown(
    [ORANGE, PURPLE],
    [PURPLE, LIGHT_PURPLE],
    DARK,
    ORANGE,
    1435, 15, 355, 60,
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
                if(pos[0] != -1):
                    arr.append(pos[0]);arr.append(pos[1]);arr.append(pygame.mouse.get_pos()[0]);arr.append(pygame.mouse.get_pos()[1])
            pos = pygame.mouse.get_pos()
    text_rect = title_text.get_rect(center=(size[0]/2, 50))
    window_surface.blit(title_text, text_rect)
    if not(start):
        start_button = pygame.draw.rect(window_surface,'#F39237', pygame.Rect(820, 1000, 280, 90),  0, 3)
        text_rect = start_text.get_rect(center=(size[0]/2, 1045))
        window_surface.blit(start_text, text_rect)
        if start_button.collidepoint(pos):
            start = True
    else:
        #text_rect = planet_text.get_rect(center=(size[0]/2, 120))
        #window_surface.blit(planet_text, text_rect)
        if not(saving):
            exoPlanetSelector.draw(window_surface) 
            constellation_button = pygame.draw.rect(window_surface, '#F39237', pygame.Rect(70, 15, 345, 60), 0, 3)
            window_surface.blit(constellation_text, (85, 20))
            exit_button = pygame.draw.rect(window_surface, '#F39237', pygame.Rect(90, 1115, 110, 60), 0, 3)
            window_surface.blit(exit_text, (100, 1120))
            save_button = pygame.draw.rect(window_surface, '#F39237', pygame.Rect(1710, 1115, 115, 60), 0, 3)
            window_surface.blit(save_text, (1720, 1120))

        selected_option = exoPlanetSelector.update(event_list)
        if selected_option >= 0:
            exoPlanetSelector.chosen = exoPlanetSelector.options[selected_option]

        if constellation_button.collidepoint(pos):
            if constellation_str == 'Start Charting':
                constellation_str = 'End Charting'
                mapping = True
                temp_len = len(arr)
            else:
                constellation_str = 'Start Charting'
                mapping = False
                if temp_len != len(arr):
                    arr.pop();arr.pop();arr.pop();arr.pop();
            pos = (-1, -1)
        if mapping:
            undo_button = pygame.draw.rect(window_surface, '#F39237', pygame.Rect(70, 80, 110, 60), 0, 3)
            window_surface.blit(undo_text, (85, 85))
            if undo_button.collidepoint(pos) and len(arr) > 1:
                arr.pop();arr.pop();arr.pop();arr.pop();
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
