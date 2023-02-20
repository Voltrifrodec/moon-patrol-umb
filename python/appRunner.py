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


# Global constants and variables initialization
BG_COLOR_DEFAULT = pygame.Color(0, 143, 230)
isFullscreen = False


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
    screen.fill(BG_COLOR_DEFAULT)
    
    # Window Update
    pygame.display.flip()
    delta = clock.tick(FPS) * 0.001
    clock.tick(FPS / delta)
