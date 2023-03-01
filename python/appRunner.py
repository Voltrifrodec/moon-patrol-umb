#? Used libraries
import pygame
import sys
    

# Initialization of pygame
pygame.init()
clock = pygame.time.Clock();


# Window settings
[SCREEN_WIDTH, SCREEN_HEIGTH] = [800, 600]
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGTH))
pygame.display.set_caption('Moon Patrol v1.0 - FPV UMB')
FPS = 60


# Fonts
game_font = pygame.font.Font('assets/fonts/PublicPixel-z84yD.ttf', 14)


# Surface - Main
#TODO: Pridat oramovanie (3 - 5px max, solid white)
background_surface = pygame.image.load('assets/images/bg_stars-01.png')
background_surface = pygame.transform.scale(background_surface, (750, 450))
# ground_surface = pygame.image.load('assets/images/ground2.png')
ground_surface = pygame.Surface((750, 50))
ground_surface.fill((200, 200, 200))
game_border = pygame.draw.rect(background_surface, (0, 0, 0), (0, 0, background_surface.get_width(), background_surface.get_height()), 1)

# Surface - Text
text_surface = game_font.render('Moon Patrol - UMB Version v1.0', False, (255, 255, 255))


# Global constants and variables initialization
BG_COLOR_DEFAULT = pygame.Color(0, 143, 230)
isFullscreen = False


# Class for Object
class Object:
    def __init__(self, sizeX: int, sizeY: int, color: tuple, texture: str):
        self.w = sizeX
        self.h = sizeY
        self.texture = None if texture == 'none' else texture
        


# Game Runner
while True:
    for e in pygame.event.get():
        # Window close
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Fullscreen Mode
        if e.type == pygame.KEYDOWN:
            print('Some key got pressed.')
            if e.key == pygame.K_F5 and isFullscreen is False:
                print('Windowed -> Fullscreen')
                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGTH), pygame.FULLSCREEN)
                pygame.display.update()
                isFullscreen = True
                break
            if e.key == pygame.K_F5 and isFullscreen:
                print('Fullscreen -> Windowed')
                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGTH))
                pygame.display.update()
                isFullscreen = False
                break

    
    # Objects Render
    screen.fill((40, 40, 40))
    
    # Render Surface
    screen.blit(background_surface, (25, 25)) # blit - putting surface on surface
    screen.blit(ground_surface, (25, (background_surface.get_height() - ground_surface.get_height() + 25)))
    screen.blit(text_surface, (int(400 - text_surface.get_width() / 2), 571))
    
    
    
    # Window Update
    pygame.display.update() # Alebo pygae.display.flip()
    delta = clock.tick(FPS) * 0.001
    clock.tick(FPS / delta)
