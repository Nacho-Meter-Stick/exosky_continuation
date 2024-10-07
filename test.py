import pygame


white = (255, 255, 255)
pygame.init()
start_font = pygame.font.Font('./programFonts/Cascadia.ttf', 80)
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
background.fill(pygame.Color('#161525'))

pos = (-1, -1)
mapping = False
start = False
saving = False

check = True
border_margin = 10
text_margin = 5

planet_str = "Earth"
constellation_str = 'Start Charting'
radii = 3

arr = []
temp_len = 0


while True:
    window_surface.blit(background, (0, 0))

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
                    arr.pop();arr.pop();arr.pop();arr.pop()
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
