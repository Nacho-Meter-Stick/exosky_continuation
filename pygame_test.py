import pygame
from random import randint
import time

white = (255, 255, 255)
pygame.init()
my_font = pygame.font.Font('./programFonts/font.ttf', 100)
text_surface = my_font.render('Exosky Challenge!', False, (153, 50, 204))

pygame.display.set_caption('Exosky!')
window_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) #or pygame.FULLSCREEN to have the window stay fullscreen (no bar at top) Two numbers indicate minimized size

background = pygame.Surface((3000, 2000))
background.fill(pygame.Color('#000000'))
is_running = True

while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
    window_surface.blit(background, (0, 0))
    pygame.draw.circle(window_surface, white,[1500, 300], 5, 0)  #surface, Color, coord, radius, line thickness where 0 is solid
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
    window_surface.blit(text_surface, (525, 450))
    pygame.display.update()
    time.sleep(10)

