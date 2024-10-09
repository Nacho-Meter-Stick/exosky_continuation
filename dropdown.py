import pygame

COLOR_INACTIVE = (22, 21, 37)
COLOR_ACTIVE = (44, 42, 74)
COLOR_TEXT = (238, 227, 206)
COLOR_LIST_INACTIVE = (22, 21, 37)
COLOR_LIST_ACTIVE = (44, 42, 74)

pygame.init()
PLANET_FONT = pygame.font.Font('./programFonts/Cascadia.ttf', 40)

class SearchableDropDown():
    def __init__(self, menu_color, option_color, txt_color, chosen_txt_color, x, y, w, h, options, SIZE, text="Switch Planet!"):
        self.rect = pygame.Rect(x, y, w, h)
        self.textx = int(SIZE[0]/2)
        self.texty = 120

        self.menu_color = menu_color
        self.option_color = option_color
        self.txt_color = txt_color
        self.chosen_txt_color = chosen_txt_color

        self.options = options
        self.shownOptions = options
        self.text = text
        self.chosen = "Earth"

        self.font = PLANET_FONT
        self.menu_active = False
        self.draw_dropdown = False
        self.active_option = -1
        self.text_surf = self.font.render(text, True, self.menu_color[self.menu_active])
        self.chosen_text_surf = self.font.render(self.chosen, True, self.menu_color[self.menu_active])

    def draw_planetName_on(self, surf, y=None):
        if y is None:
            surf.blit(self.chosen_text_surf, (self.textx - (self.chosen_text_surf.get_rect().width//2), self.texty))
        else:
            surf.blit(self.chosen_text_surf, (self.textx - (self.chosen_text_surf.get_rect().width//2), y))
        return

    def draw_dropdown_on(self, surf):
        pygame.draw.rect(surf, self.menu_color[self.menu_active], self.rect, 0)
        surf.blit(self.text_surf, (self.rect.x+5, self.rect.y+5))

        # copy the box down for all options shown
        if self.draw_dropdown:
            for i, text in enumerate(self.shownOptions):
                rect = self.rect.copy()
                rect.y += (i+1) * self.rect.height
                pygame.draw.rect(surf, self.option_color[(i == self.active_option)], rect, 0)
                text = self.font.render(text, 1, self.txt_color)
                surf.blit(text, text.get_rect(center = rect.center))

    def pos_is_not_on_menu(self, pos):
        if self.rect.collidepoint(pos): return False
        if self.draw_dropdown:
            for i, text in enumerate(self.shownOptions):
                rect = self.rect.copy()
                rect.y += (i+1) * self.rect.height
                if rect.collidepoint(pos): return False
        return True

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
        changed = False
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
                    new_chosen = self.shownOptions[self.active_option]
                    if new_chosen != self.chosen:
                        self.chosen = new_chosen
                        changed = True
                    self.text = "Switch Planet!"
                    self.font.render(self.chosen, True, self.chosen_txt_color)

        if self.search() is not None:
            self.shownOptions = self.search()
        else:
            self.shownOptions == self.options

        self.text_surf = self.font.render(self.text, True, self.txt_color)
        self.chosen_text_surf = self.font.render(self.chosen, True, self.chosen_txt_color)

        # make box longer when text gets too big
        width = max(355, self.text_surf.get_width()+10)
        self.rect.w = width
        return changed

    def search(self):
        matches = []
        for option in self.options:
            if self.text in option:
                matches.append(option)
        self.shownOptions = matches

    def getChosen(self):
        return self.chosen