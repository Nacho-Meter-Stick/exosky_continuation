import pygame
from random import randint
import numpy as np
import  database

star_database = buildCartesianDatabase()
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

background = pygame.Surface((3000, 2000))
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
    planet_text = planet_font.render(planet_str, False, '#F39237')
    constellation_text = planet_font.render(constellation_str, False, '#907AD6')
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if(mapping):
                if(pos[0] != -1):
                    arr.append(pos[0]);arr.append(pos[1]);arr.append(pygame.mouse.get_pos()[0]);arr.append(pygame.mouse.get_pos()[1])
            pos = pygame.mouse.get_pos()
    #Drawing Star:
         #0, 0 is top left
         #1920, 1200 is bot right (computer resolution) for full screen
         #1920, 1130 is bot right (computer resolution dependant) for windowed full screen
    for i in range(1201):
        x = randint(50, 255)
        color = (x, x, x)
        pygame.draw.circle(window_surface, color,[randint(0, 1920), i], randint(1, 4), 0)
        pygame.draw.circle(window_surface, color,[randint(0, 1920), i], randint(1, 4), 0)
        pygame.draw.circle(window_surface, color,[randint(0, 1920), i], randint(1, 4), 0)
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
#declination if positive NOrthern, southern otherwise. 1- (Dec Rad/pi/2) gives radius (norhtern).  1+(Dec Rad/pi/2)
declination, ascension = 0
if declination > 0:
    x = np.cos(ascension)*(1-declination/(np.py/2))
    y = np.sin(ascension)*(1-declination/(np.py/2))
else:
    x = np.cos(ascension)*(1+declination/(np.py/2))
    y = np.sin(ascension)*(1+declination/(np.py/2))
