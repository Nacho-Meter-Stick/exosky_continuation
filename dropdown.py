import pygame
import database

COLOR_INACTIVE = (79, 81, 140)
COLOR_ACTIVE = (144, 122, 214)
COLOR_LIST_INACTIVE = (79, 81, 140)
COLOR_LIST_ACTIVE = (144, 122, 214)

pygame.init()
my_font = pygame.font.Font('./programFonts/font.ttf', 100)

class DropDown():
    def __init__(self, menu_color, option_color, x, y, w, h, default, options):
        self.menu_color = menu_color
        self.option_color = option_color
        self.rect = pygame.Rect(0, 0, w, h)
        self.options = options
        self.chosen = default
        self.font = pygame.font.SysFont(None, 30)
        self.menu_active = False
        self.draw_dropdown = False
        self.active_option = -1

    def draw(self, surf):
        pygame.draw.rect(surf, self.menu_color[self.menu_active], self.rect, 0)
        msg = self.font.render(self.chosen, 1, (0, 0, 0))
        surf.blit(msg, msg.get_rect(center = self.rect.center))

        if self.draw_dropdown:
            for i, text in enumerate(self.options):
                rect = self.rect.copy()
                rect.y += (i+1) * self.rect.height
                pygame.draw.rect(surf, self.option_color[1 if i == self.active_option else 0], rect, 0)
                msg = self.font.render(text, 1, (0, 0, 0))
                surf.blit(msg, msg.get_rect(center = rect.center))


    def update(self, event_list):
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
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.menu_active:
                    self.draw_dropdown = not self.draw_dropdown
                elif self.draw_dropdown and self.active_option >= 0:
                    self.draw_dropdown = False
                    return self.active_option
        return -1

planets = database.getExoplanetData()
planetNames = []
for planet in planets:
    planetNames.append(planet['name'])

# print(planetNames)

exoPlanetSelector = DropDown(
    [COLOR_INACTIVE, COLOR_ACTIVE],
    [COLOR_LIST_INACTIVE, COLOR_LIST_ACTIVE],
    50, 50, 250, 50,
    "Choose an exoplanet!", 
    planetNames)

if __name__ == "__main__":
    screen = pygame.display.set_mode((640, 480))

    dropDownSurf = pygame.Surface((640, 480))

    is_running = True
    while is_running:
        event_list = pygame.event.get()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

        selected_option = exoPlanetSelector.update(event_list)
        if selected_option >= 0:
            exoPlanetSelector.chosen = exoPlanetSelector.options[selected_option]

        #screen.blit(dropDownSurf, (0, 0), area=pygame.rect(50, 50, 200, 400))
        screen.fill((22, 21, 37))
        exoPlanetSelector.draw(screen)
        pygame.display.flip()