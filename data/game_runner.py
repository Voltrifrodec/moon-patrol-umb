import math
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
COLOR_PLAYER = (0, 200, 200)
COLOR_OBSTACLE = (0, 0, 0)



#* Window settings
[SCREEN_WIDTH, SCREEN_HEIGHT] = [800, 600]
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Moon Patrol v0.0 - FPV UMB')
FPS = 60


#* Surfaces - Main
background_surface = pygame.image.load("assets/images/background_stars.png")
background_surface = pygame.transform.scale(background_surface, (SCREEN_WIDTH, SCREEN_HEIGHT + 50))

ground_surface = pygame.image.load("assets/images/surface-final.png")
ground_surface = pygame.transform.scale(ground_surface, (SCREEN_WIDTH, 150))

#* Player
[PLAYER_WIDTH, PLAYER_HEIGHT] = [100, 100]
image = pygame.image.load('assets/images/player2.png').convert_alpha()
class Vehicle:
	def __init__(self, sizeX: int, sizeY: int, color: tuple, texture: str, surface: pygame.Surface):
		self.w = sizeX
		self.h = sizeY
		self.texture = None if texture == '' else texture
		self.color = (255,255,255)
		self.surface = surface
		# self.rect = pygame.Rect(0, self.surface.get_height() - self.h - ground_surface.get_height(), self.w, self.h)
		self.rect = image.get_rect(center= (int(image.get_width() / 2), self.surface.get_height() - ground_surface.get_height() - int(image.get_height() / 2)))
		self.isJumping = False
		self.jumpCount = 10

		self.firstJump = True
		self.jumpSegment = 0.065 # 0.045 → 0.065, kvoli prekazke
		self.hranica = 100
		self.zem = self.rect.y

	
	def jump(self):
		if (self.isJumping):
			if (self.firstJump):
				self.rect.y -= 2 * self.jumpCount
				self.firstJump = False

			if (self.rect.top >= self.zem):
				print('Si na zemi')
				self.jumpSegment = -self.jumpSegment
				self.isJumping = False
				self.firstJump = True
				self.rect.y = self.zem
				return

			if (self.rect.top <= self.hranica):
				print('Hitol si hranicu')
				self.jumpSegment = -self.jumpSegment
			
			if (self.rect.y <= self.zem or self.rect.y >= self.hranica):
				rovnica = -((self.rect.y / 18) ** 2)
				self.rect.y += rovnica * self.jumpSegment
	
	def render(self):
		self.jump()
		# pygame.draw.rect(screen, self.color, self.rect)
		screen.blit(image, self.rect)

playerVehicle = Vehicle(PLAYER_WIDTH, PLAYER_HEIGHT, COLOR_PLAYER, '', background_surface)


#* Obstacle
class Obstacle:
	def __init__(self):
		self.w = 100
		self.h = 25
		self.surface = ground_surface
		self.color = COLOR_OBSTACLE
		self.rect = pygame.Rect(self.surface.get_width(), background_surface.get_height() - ground_surface.get_height() - 21, self.w, self.h)
		self.image = pygame.image.load('assets/images/ravine3.png')
		self.speed = 10
	
	def move(self):
		if(self.rect.x > -self.rect.w):
			self.rect.x -= self.speed
		else:
			self.rect.x = self.surface.get_width()

	def render(self):
		self.move()
		screen.blit(self.image, self.rect)


#* Projectile
projectile_arr = []
class Projectile():
	def __init__(self, posY: int):
		self.w = 10
		self.h = 10
		self.color = (200, 200, 0)
		self.surface = background_surface
		# self.rect = pygame.Rect(self.surface.get_width - playerVehicle.w, self.surface.get_height() - playerVehicle.rect.y, self.w, self.h)
		self.rect = pygame.Rect(playerVehicle.rect.w, playerVehicle.rect.top + (playerVehicle.rect.h / 2), self.w, self.h)
		self.projectileSpeed = 10
	
	def move(self):
		if(self.rect.x < self.surface.get_width()):
			self.rect.x += self.projectileSpeed
	
	def render(self):
		self.move()
		pygame.draw.rect(screen, self.color, self.rect)

#* Fonts
game_font_main = pygame.font.Font('assets/fonts/PublicPixel-z84yD.ttf', 18)
game_font_dev = pygame.font.Font('C:\Windows\Fonts\Arial.ttf', 10)
testObstacle = Obstacle()

 
#* Enemy
(ENEMY_WIDTH, ENEMY_HEIGHT) = (75, 75)
COLOR_ENEMY = (200, 0, 0)
enemy_arr = []
class Enemy():
	def __init__(self):
		self.w = ENEMY_WIDTH
		self.h = ENEMY_HEIGHT
		self.moveSpeed = 2
		self.projectileSpeed = 5
		self.isDead = False
		self.surface = background_surface
		self.color = COLOR_ENEMY
		self.rect = pygame.Rect(self.surface.get_width(), self.surface.get_height() - self.h - ground_surface.get_height(), self.w, self.h)

	def move(self):
		if self.isDead is not True:
			if(self.rect.x > -self.rect.w):
				self.rect.x -= self.moveSpeed
			else:
				self.rect.x = self.surface.get_width()
		else:
			self.isDead = False
			self.rect.x = self.surface.get_width() + 100
			return

	def render(self):
		self.move()
		pygame.draw.rect(screen, self.color, self.rect)

enemy_arr.append(Enemy())


#* Game Runner
gameRunner = True
score = 0
score_text = game_font_main.render("Score: {}".format(str(score)), False, (0, 0, 0))
dev_text = game_font_dev.render("{} {} {}".format(len(projectile_arr), len(enemy_arr), 0), False, (0, 0, 0))
while gameRunner:
	
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
			if e.key == pygame.K_e:
				print('Player shot a projectile!')
				projectile_arr.append(Projectile(playerVehicle.rect.y))
	
	# Screen Render
	screen.fill(BG_COLOR_SCREEN)
	screen.blit(background_surface, (0, 0))
	screen.blit(ground_surface, (0, SCREEN_HEIGHT - ground_surface.get_height()))
	screen.blit(image, playerVehicle)
	
	# Text Render
	score_text = game_font_main.render("Score: {}".format(str(score)), False, (0, 0, 0))
	screen.blit(score_text, (int(SCREEN_HEIGHT / 2), SCREEN_HEIGHT - 100))
	dev_text = game_font_dev.render("{} {} {}".format(len(projectile_arr), len(enemy_arr), "issue/texture-implementation"), False, (0, 0, 0))
	screen.blit(dev_text, (10, SCREEN_HEIGHT - 20))
	
	
	# Objects Render
	playerVehicle.render()
	testObstacle.render()

	# print('Projectile on screen:', len(projectile_arr))
	for i, obj in enumerate(projectile_arr):
		if(obj.rect.x >= screen.get_width()):
			print('Object is outside screen width, removing...')
			del projectile_arr[i]
		else:
			obj.render()
			
	for i, obj in enumerate(enemy_arr):
		obj.render()
		# If Enemy is shot
		if(len(projectile_arr) != 0):
			for j, projectile in enumerate(projectile_arr):
				if(obj.rect.colliderect(projectile.rect)):
					print("One of the projectile hit enemy! Reseting him...")
					obj.isDead = True
					score += 100
					del projectile_arr[j]
					break
		# If Enemy hit player (bump)
		if(obj.rect.colliderect(playerVehicle.rect)):
			print("Player bumped into Enemy. Game over!")
			gameRunner = False
	
	
	if(playerVehicle.rect.colliderect(testObstacle.rect)):
		# if((playerVehicle.rect.centerx == testObstacle.rect.centerx) & (playerVehicle.rect.midbottom <= testObstacle.rect.topleft)):
		print("Obstacle was hit! Game over")
		gameRunner = False

	
	
	# Window Update
	pygame.display.update()
	clock.tick(FPS)
	
