import pygame
from sys import exit

#? Implementovane:
"""
- inicializacia pygame (vytvorenie okna, pridanie popisku, velkost)
- pridanie hlavneho cyklu (while True: ...)
- pridanie pozadia a zeme (ako surface a vyplnene farbou)

"""


#* Initialization of the pygame
pygame.init()
clock = pygame.time.Clock()

#* Colors
BG_COLOR_SCREEN = (40, 40, 40)
BG_COLOR_DEFAULT = (0, 143, 230)
BG_COLOR_SURFACE = (100, 100, 100)
COLOR_PLAYER = (200, 0, 0)
COLOR_OBSTACLE = (40, 50, 100)



#* Window settings
[SCREEN_WIDTH, SCREEN_HEIGHT] = [800, 600]
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Moon Patrol v0.0 - FPV UMB')
FPS = 60


#* Surfaces - Main
background_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
background_surface.fill(BG_COLOR_SCREEN)

ground_surface = pygame.Surface((SCREEN_WIDTH, 150))
ground_surface.fill(BG_COLOR_SURFACE)

# print(ground_surface.get_rect().top, ground_surface.get_rect().bottom)

#* Player
[PLAYER_WIDTH, PLAYER_HEIGHT] = [100, 100]
class Vehicle:
    def __init__(self, sizeX: int, sizeY: int, color: tuple, texture: str, surface: pygame.Surface):
        self.w = sizeX
        self.h = sizeY
        self.texture = None if texture == '' else texture
        self.color = color
        self.surface = surface
        self.rect = pygame.Rect(0, self.surface.get_height() - self.h - ground_surface.get_height(), self.w, self.h)
        self.isJumping = False
        self.jumpCount = 25
        self.defaultJumpCount = 25

        self.startPositionXY = (self.rect.x, self.rect.y)

        self.temp = -1
        self.jumpHeightMultiplier = 9.5 # Default - ako vysoko bude skakat
    
    def jump(self):
        if(self.isJumping):
            if(self.jumpCount >= -self.defaultJumpCount):
                self.temp = 1
                if(self.jumpCount < 0):
                    self.temp = -1
                self.rect.y -= self.jumpCount ** 2 * 0.005 * self.temp * self.jumpHeightMultiplier
                self.jumpCount -= 1
            else:
                self.isJumping = False
                self.jumpCount = self.defaultJumpCount
                self.rect.y = (self.rect.y - self.jumpCount * self.temp)
                if(self.rect.y > ground_surface.get_height()):
                    self.rect.y = self.surface.get_height() - self.h - ground_surface.get_height()
                if(self.rect.top < 0):
                    self.rect.top = 0

    
    def render(self):
        self.jump()
        pygame.draw.rect(screen, self.color, self.rect)
        
        
#* Obstacle
class Obstacle:
    def __init__(self):
        self.w = 100
        self.h = 25
        self.surface = ground_surface
        self.color = COLOR_OBSTACLE
        self.rect = pygame.Rect(self.surface.get_width() - self.w, background_surface.get_height() - self.surface.get_height(), self.w, self.h)
        self.speed = 10
    
    def move(self):
        if(self.rect.x > -self.rect.w):
            self.rect.x -= self.speed
        else:
            self.rect.x = self.surface.get_width()
    
    def render(self):
        self.move()
        pygame.draw.rect(screen, self.color, self.rect)

playerVehicle = Vehicle(PLAYER_WIDTH, PLAYER_HEIGHT, COLOR_PLAYER, '', background_surface)

testObstacle = Obstacle()


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
        # Keyboard Action Listeners

        if e.type == pygame.KEYDOWN:
            print('Some key got pressed')
            if e.key == pygame.K_SPACE and not playerVehicle.isJumping:
                playerVehicle.isJumping = True
                # playerVehicle.isJumping = True
                # playerVehicle.jumpCount = 10
                # playerVehicle.jump()
                # break
            # else:
                # playerVehicle.isJumping = False
                # break
            
                
    
    # Screen Render
    screen.fill(BG_COLOR_SCREEN)
    screen.blit(background_surface, (0, 0))
    screen.blit(ground_surface, (0, SCREEN_HEIGHT - ground_surface.get_height()))
    
    # Objects Render
    playerVehicle.render()
    testObstacle.render()
    
    
    # player_object = pygame.draw.rect(screen, (COLOR_PLAYER), (0, SCREEN_HEIGHT - PLAYER_HEIGHT - ground_surface.get_height(), PLAYER_WIDTH, PLAYER_HEIGHT), 1)
    
    # Window Update
    pygame.display.update()

    pygame.display.update()
    delta = clock.tick(FPS) * 0.001
    clock.tick(FPS / delta)
    
