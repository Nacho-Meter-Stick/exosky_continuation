import pygame
import database
import time

COLOR_INACTIVE = (22, 21, 37)
COLOR_ACTIVE = (44, 42, 74)
COLOR_TEXT = (238, 227, 206)
COLOR_LIST_INACTIVE = (22, 21, 37)
COLOR_LIST_ACTIVE = (44, 42, 74)

pygame.init()
planet_font = pygame.font.Font('./programFonts/Cascadia.ttf', 40)

class SearchableDropDown():
    def __init__(self, menu_color, option_color, txt_color, chosen_txt_color, x, y, w, h, options, SIZE, text="Switch Planet!"):
        self.rect = pygame.Rect(x, y, w, h)
        self.textx = SIZE[0]/2 +20
        self.texty = 120

        self.menu_color = menu_color
        self.option_color = option_color
        self.txt_color = txt_color
        self.chosen_txt_color = chosen_txt_color

        self.options = options
        self.shownOptions = options
        self.text = text
        self.chosen = "Earth!"

        self.font = planet_font
        self.menu_active = False
        self.draw_dropdown = False
        self.active_option = -1
        self.text_surf = planet_font.render(text, True, self.menu_color[self.menu_active])
        self.chosen_text_surf = planet_font.render(self.chosen, True, self.menu_color[self.menu_active])

    def draw(self, surf):
        pygame.draw.rect(surf, self.menu_color[self.menu_active], self.rect, 0)
        surf.blit(self.text_surf, (self.rect.x+5, self.rect.y+5))
        surf.blit(self.chosen_text_surf, (self.textx - (len(self.chosen)//2), self.texty))

        # copy the box down for all options shown
        if self.draw_dropdown:
            for i, text in enumerate(self.shownOptions):
                rect = self.rect.copy()
                rect.y += (i+1) * self.rect.height
                pygame.draw.rect(surf, self.option_color[1 if i == self.active_option else 0], rect, 0)
                text = self.font.render(text, 1, self.txt_color)
                surf.blit(text, text.get_rect(center = rect.center))

    def update(self, event_list):
        mpos = pygame.mouse.get_pos()
        self.menu_active = self.rect.collidepoint(mpos)

        # Draw the dropdown 
        for i in range(len(self.shownOptions)):
            rect = self.rect.copy()
            rect.y += (i+1) * self.rect.height
            if rect.collidepoint(mpos):
                self.active_option = i
                break

        if not self.menu_active and self.active_option == -1:
            self.draw_dropdown = False

        # event handler
        for event in event_list:
            if event.type == pygame.KEYDOWN:
                if not self.menu_active:
                    continue
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.menu_active:
                    self.draw_dropdown = not self.draw_dropdown
                    self.text = ""
                elif self.draw_dropdown and self.active_option >= 0:
                    self.draw_dropdown = False
                    self.chosen = self.shownOptions[self.active_option]
                    self.text = "Switch Planet!"
                    self.font.render(self.chosen, True, self.chosen_txt_color)

        if not self.search() == None:
            self.shownOptions = self.search()
        else:
            self.shownOptions == self.options

        self.text_surf = self.font.render(self.text, True, self.txt_color)
        self.chosen_text_surf = self.font.render(self.chosen, True, self.chosen_txt_color)

        # make box longer when text gets too big
        width = max(355, self.text_surf.get_width()+10)
        self.rect.w = width
        return -1

    def search(self):
        matches = []
        for option in self.options:
            if self.text in option:
                matches.append(option)
        self.shownOptions = matches


class DropDown():
    def __init__(self, menu_color, option_color, x, y, w, h, default, options):
        self.menu_color = menu_color
        self.option_color = option_color
        self.rect = pygame.Rect(x, y, w, h)
        self.options = options
        self.chosen = default
        self.font = pygame.font.SysFont(None, 30)
        self.menu_active = False
        self.draw_dropdown = False
        self.active_option = -1

    def draw(self, surf):
        pygame.draw.rect(surf, self.menu_color[self.menu_active], self.rect, 0)
        text = self.font.render(self.chosen, 1, (0, 0, 0))
        surf.blit(text, text.get_rect(center = self.rect.center))

        if self.draw_dropdown:
            for i, text in enumerate(self.options):
                rect = self.rect.copy()
                rect.y += (i+1) * self.rect.height
                pygame.draw.rect(surf, self.option_color[1 if i == self.active_option else 0], rect, 0)
                text = self.font.render(text, 1, (0, 0, 0))
                surf.blit(text, text.get_rect(center = rect.center))


    def update(self, event):
        mpos = pygame.mouse.get_pos()
        self.menu_active = self.rect.collidepoint(mpos)

        for i in range(len(self.options)):
            rect = self.rect.copy()
            rect.y += (i+1) * self.rect.height
            if rect.collidepoint(mpos):
                self.active_option = i
                break

        if not self.menu_active and self.active_option == -1:
            self.draw_dropdown = False

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.menu_active:
                    self.draw_dropdown = not self.draw_dropdown
                elif self.draw_dropdown and self.active_option >= 0:
                    self.draw_dropdown = False
                    return self.active_option
        return -1

class UserInputBox():
    def __init__(self, x, y, w, h, text="Search an Exoplanet!"):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = pygame.font.SysFont(None, 30)
        self.active = False
        self.color = COLOR_ACTIVE
        self.txt_color = COLOR_INACTIVE
        self.text_surf = FONT.render(text, True, self.color)

    def update(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.active = not self.active
                    if self.active:
                        self.text = ""
                else:
                    self.active = False
            if event.type == pygame.KEYDOWN:
                if not self.active:
                    break
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                
        
        self.text_surf = self.font.render(self.text, True, self.txt_color)

        # make box longer when text gets too big
        width = max(200, self.text_surf.get_width()+10)
        self.rect.w = width

    def draw(self, surf):
        pygame.draw.rect(surf, self.color, self.rect, 0, border_radius=3)
        screen.blit(self.text_surf, (self.rect.x+5, self.rect.y+5))
        

if __name__ == "__main__":
    screen = pygame.display.set_mode((640, 480))
    dropDownSurf = pygame.Surface((640, 480))

    is_running = True
    while is_running:
        event_list = pygame.event.get()
        for event in pygame.event.get():
            # quit when needed
            if event.type == pygame.QUIT:
                is_running = False

        # update dropdown
        selected_option = exoPlanetSelector.update(event_list)
        if selected_option >= 0:
            exoPlanetSelector.chosen = exoPlanetSelector.options[selected_option]

        #screen.blit(dropDownSurf, (0, 0), area=pygame.rect(50, 50, 200, 400))
        screen.fill((238, 227, 206))
        exoPlanetSelector.draw(screen)
        pygame.display.update()
        #time.sleep(10)
