import pygame
from random import randint
import numpy as np
from database import buildSphericalDatabase
from database import buildCartesianDatabase
from quaternions import normalized
from sphere_to_2circles import sphere_to_circle

def generateSkySurface(width, height):
    sky_surface = pygame.Surface((width, height))
    spherical_database = buildSphericalDatabase()
    star_database = buildCartesianDatabase(spherical_database)
    for entry in star_database:
        entry['coordinates'] = normalized(entry['coordinates'])

    sphere_xyz = [entry['coordinates'] for entry in star_database]
    chartPos = sphere_to_circle(sphere_xyz)
    
    # Draw north
    for point in chartPos[0]:
        z = randint(50, 255)
        color = (z, z, z)
        x,y = point
        x *= int(width/4)
        y *= int(width/4)
        x += int(width/4)
        y += int(height/2)
        pygame.draw.circle(sky_surface, color, (x, y), 1, 0)        
    for point in chartPos[1]:
        z = randint(50, 255)
        color =(z, z, z)
        x,y = point
        x *= int(width/4)
        y *= int(width/4)
        x += int(3*width/4)
        y += int(height/2)
        pygame.draw.circle(sky_surface, color, (x, y), 1, 0)
    return sky_surface

white = (255, 255, 255)
pygame.init()
start_font = pygame.font.Font('./programFonts/font.ttf', 100)
planet_font = pygame.font.Font('./programFonts/font.ttf', 50)
title_text = start_font.render('Exosky Challenge!', False, '#907AD6')
start_text = start_font.render('Start', False, '#EEE3CE')
switch_text = planet_font.render('Switch Planets', False, '#907AD6')
exit_text = planet_font.render('Exit', False, '#907AD6')
save_text = planet_font.render('Save', False, '#907AD6')

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

while True:
    window_surface.blit(background, (0, 0))
    window_surface.blit(sky_surface, (0,0))

    planet_text = planet_font.render(planet_str, False, '#F39237')
    constellation_text = planet_font.render(constellation_str, False, '#907AD6')
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if(mapping):
                if(pos[0] != -1):
                    arr.append(pos[0]);arr.append(pos[1]);arr.append(pygame.mouse.get_pos()[0]);arr.append(pygame.mouse.get_pos()[1])
            pos = pygame.mouse.get_pos()
    if not(start):
        start_button = pygame.draw.rect(window_surface,'#F39237', pygame.Rect(810, 710, 280, 95),  0, 3)
        window_surface.blit(title_text, (525, 450))
        window_surface.blit(start_text, (825, 705))
        if start_button.collidepoint(pos):
            start = True
    else:
        if not(saving):
            text_rect = planet_text.get_rect(center=(1920/2, 40))
            window_surface.blit(planet_text, text_rect)
            switch_button = pygame.draw.rect(window_surface, '#F39237', pygame.Rect(1435, 15, 390, 70), 0, 3) 
            window_surface.blit(switch_text, (1450, 20))
            constellation_button = pygame.draw.rect(window_surface, '#F39237', pygame.Rect(70, 15, 370, 70), 0, 3)
            window_surface.blit(constellation_text, (85, 20))
            exit_button = pygame.draw.rect(window_surface, '#F39237', pygame.Rect(90, 1115, 130, 70), 0, 3)
            window_surface.blit(exit_text, (100, 1120))
            save_button = pygame.draw.rect(window_surface, '#F39237', pygame.Rect(1710, 1115, 120, 70), 0, 3)
            window_surface.blit(save_text, (1720, 1120))
        if switch_button.collidepoint(pos):
            print("planet switch!!")
            pos = (-1, -1)
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
        if exit_button.collidepoint(pos):
            exit()
        j = 0;
        for i in range(int(len(arr)/4)):
            pygame.draw.line(window_surface, '#F39237', (arr[j], arr[j+1]), (arr[j+2], arr[j+3]), 2)
            j+=4
        if saving:
            pygame.image.save(window_surface, "image.png")
            saving = False
        if save_button.collidepoint(pos):
            saving = True
            pos = (-1, -1)
    pygame.display.update()
