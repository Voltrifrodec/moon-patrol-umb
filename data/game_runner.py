import pygame
from sys import exit

#? Implementovane:
"""
- inicializacia pygame (vytvorenie okna, pridanie popisku, velkost)
- pridanie hlavneho cyklu (while True: ...)

"""


#* Initialization of the pygame
pygame.init()
clock = pygame.time.Clock()


#* Window settings
[SCREEN_WIDTH, SCREEN_HEIGHT] = [800, 600]
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Moon Patrol v0.0 - FPV UMB')
FPS = 60


#* Fonts
game_font_main = pygame.font.Font('assets/fonts/PublicPixel-z84yD.ttf', 14)


#* Game Runner
while True:
    
    # Event Listener
    for e in pygame.event.get():
        # Window Close
        if e.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    # Screen Render
    screen.fill((40, 40, 40))
    
    # Window Update
    pygame.display.update()
    delta = clock.tick(FPS) * 0.001
    clock.tick(FPS / delta)
    