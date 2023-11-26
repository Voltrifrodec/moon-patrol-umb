'''Imports'''
# sys module
import sys
# PyGame module
import pygame
# Random module
import random

import numpy as np

from enum import Enum

'''Variable for testing'''
global TEST
TEST = False # Change to true, if you want to be ingame right away


'''Global variables/constants'''
WHITE = pygame.Color('white')
BLACK = pygame.Color('black')
YELLOW = pygame.Color('yellow')
ENEMY_WIDTH = 48

'''Class declarations'''
class Game(): ...
class Scene(): ...
class MainMenu(): ...
class InGame(): ...
class Pause(): ...
class End(): ...
class Text(): ...

class Direction(Enum):
	RIGHT = 1,
	LEFT = -1

'''Text class'''
class Text():
	def __init__(self, text:str, fontSizePixel:int, position:tuple[int,int]=(0,0), font:str='unispace bd.ttf', antialias:bool=True, textColor=WHITE) -> None:
		self.text = text
		self.fontSizePixel = fontSizePixel
		self.position = position
		self.font = self.validateFont(font)
		self.rendered = self.font.render(self.text, antialias, textColor)
		self.rectangle = self.rendered.get_rect(topleft = (self.position))

		self.textSize = self.font.size(self.text)
		self.width = self.textSize[0]
		self.height = self.textSize[1]
	
	# Changes text
	def changeTo(self, text):
		self.text = text
	
	def changePosition(self, position):
		self.position = position
		self.rectangle = self.rendered.get_rect(topleft = (self.position))

	def doesCollide(self, x:int, y:int):
		return self.rectangle.collidepoint(x, y)

	def validateFont(self, font:str) -> pygame.font.Font:
		try:
			return pygame.font.Font(font, self.fontSizePixel)
		except FileNotFoundError as e:
			defaultFontPath = '/unispace bd.ttf'
			print(f'{e}')
			print(f'Using the default font: {defaultFontPath}')
			return pygame.font.Font(defaultFontPath, self.fontSizePixel)

'''Scene class'''
class Scene():
	def __init__(self, game:Game) -> None:
		self.current: Scene = None
		self.game = game
	
	# Initializes scenes
	def initialize(self) -> None:
		self.menu = MainMenu(self.game)
		self.inGame = InGame(self.game)
		self.pause = Pause(self.game)
		self.end = End(self.game)
		self.changeTo(self.menu)
	
	# Pauses game
	def pauseScene(self) -> None:
		self.changeTo(self.pause)
	
	# Unpauses game
	def unpauseScene(self) -> None:
		self.changeTo(self.inGame)
	
	# Changes scene
	def changeTo(self, scene:Scene) -> None:
		self.current = scene
	
	# Draws current scene
	def draw(self):
		self.current.draw()
	
	# Updates the current scene
	def update(self, x:int, y:int) -> None:
		# self.current.update(x, y)
		pass

'''Main menu class'''
class MainMenu(Scene):
	def __init__(self, game=Game) -> None:
		super().__init__(game)
		self.name = 'Main Menu'
		self.initialize()
	
	# Initializes scene
	def initialize(self):
		fontSize = 50
		self.play = Text('PLAY', fontSize)
		self.play.changePosition((self.game.windowWidth//2 - self.play.width//2, 1.5 * self.play.fontSizePixel))
		self.quit = Text('QUIT', fontSize)
		self.quit.changePosition((self.game.windowWidth//2 - self.play.width//2, 4 * self.quit.fontSizePixel))
	
	# Draws scene
	def draw(self) -> None:
		if self.game.score != 0: self.game.score = 0
		self.game.surface.fill(BLACK)
		self.game.surface.blit(self.play.rendered, self.play.position)
		self.game.surface.blit(self.quit.rendered, self.quit.position)
	
	# Updates if buttons are clicked
	def update(self, x:int, y:int) -> None:
		if self.play.doesCollide(x, y):
			self.game.scene.changeTo(self.game.scene.inGame)
		if self.quit.doesCollide(x, y):
			self.game.quit()

'''In game class'''
class InGame(Scene):
	def __init__(self, game=Game) -> None:
		super().__init__(game)
		self.name = 'InGame'
		self.fontSizePixel = 20
	
	# Draws game and score
	def draw(self):
		self.game.draw()
		self.score = Text(f'SCORE {self.game.score:2}', self.fontSizePixel)
		# self.score.changePosition((self.game.windowWidth - self.score.width - 1, 0))
		self.game.surface.blit(self.score.rendered, self.score.position)
	
	# Does not do anything
	def update(self, x: int, y: int) -> None:
		pass

'''Pause class'''
class Pause(Scene):
	def __init__(self, game=Game) -> None:
		super().__init__(game)
		self.initialize()
		self.name = 'Paused'
	# Initializes class
	def initialize(self):
		fontSizePixel = 50
		self.paused = Text('PAUSED', fontSizePixel)
		self.paused.changePosition((self.game.windowWidth//2 - self.paused.width//2, self.game.windowHeight//2 - self.paused.fontSizePixel))
		self.resume = Text('PAUSED', fontSizePixel)
		self.resume.changePosition((self.game.windowWidth//2 - self.resume.width//2, self.game.windowHeight//2 + self.resume.fontSizePixel))
	# Updates if buttons are clicked
	def update(self, x:int, y:int):
		if self.resume.doesCollide(x, y):
			self.game.scene.changeTo(self.game.scene.inGame)
	# Draws a pause in the middle of the screen
	def draw(self):
		game.surface.blit(self.paused.rendered, self.paused.position)

'''End class'''
class End(Scene):
	def __init__(self, game=Game) -> None:
		super().__init__(game)
		self.name = 'End'
	# Initializes text
	def initialize(self) -> None:
		fontSize = 50
		self.gameEnded = Text('GAME ENDED', fontSize)
		self.gameEnded.changePosition((self.game.windowWidth//2 - self.gameEnded.width//2, 1 * self.gameEnded.fontSizePixel))

		self.finalScore = Text(f'FINAL SCORE: {self.game.score}', fontSize)
		self.finalScore.changePosition((self.game.windowWidth//2 - self.finalScore.width//2, 3 * self.finalScore.fontSizePixel))

		fontSize = 30
		self.menu = Text('MAIN MENU', fontSize)
		self.menu.changePosition((self.game.windowWidth//2 - self.menu.width//2, self.game.windowHeight - 3 * self.menu.fontSizePixel))
	# Draws the game ended screen with score
	def draw(self):
		self.initialize()
		self.game.surface.fill(BLACK)
		game.surface.blit(self.gameEnded.rendered, self.gameEnded.position)
		game.surface.blit(self.finalScore.rendered, self.finalScore.position)
		game.surface.blit(self.menu.rendered, self.menu.position)
	# Updates if button is clicked
	def update(self, x:int, y:int) -> None:
		if self.menu.doesCollide(x, y):
			self.game.scene.changeTo(self.game.scene.menu)


'''Game object class'''
class GameObject():
	def __init__(self, positionX:int=0, positionY:int=0, color:pygame.Color=BLACK, imagePath:str=None, surface:pygame.Surface=None, width:int=48, height:int=24) -> None:
		self.positionX = positionX
		self.positionY = positionY
		self.color = color
		self.imagePath = imagePath
		self.image = None
		self.surface = surface

		self.width = width
		self.height = height

		if color is None and imagePath is None:
			raise ValueError('One of color or imagePath must not be None!')

		if color is not None:
			self.color = pygame.color.Color(color)
		
		if imagePath is not None:
			self.image = pygame.image.load(imagePath)
			self.image = pygame.transform.scale(self.image, (self.width, self.height))
			self.rect = self.image.get_rect(x=positionX, y=positionY)
			self.imageWidth = self.image.get_width()
			self.imageHeight = self.image.get_height()
	
	# Draws object on screen
	def draw(self):
		if self.image is not None:
			self.rect = self.image.get_rect(x=self.positionX, y=self.positionY)
			self.surface.blit(self.image, self.rect)
	
	# Checks positions
	def checkcollision(self, x:int, y:int):
		return self.positionX == x or self.positionY == y


'''Player class'''
class Player(GameObject):
	def __init__(self, positionX, positionY, color: pygame.Color = None, imagePath: str = None, screen=None, projectileSpeed=10, width=48, height=28) -> None:
		super().__init__(positionX, positionY, color, imagePath, screen, width, height)
		self.startingPosition = positionX, positionY
		self.jumpCount = 10
		self.isJumping = False
		self.firstJump = True
		self.jumpSegment = 0.085 # 0.045 → 0.065, kvoli prekazke
		self.hranica = 200 # TODO: Change
		self.zemY = self.rect.y
		self.projectileSpeed = projectileSpeed

	# Moves
	def move(self):
		if (self.isJumping):
			if TEST: print('jumping')
			if (self.firstJump):
				self.rect.y -= 2 * self.jumpCount
				self.firstJump = False

			if (self.rect.top >= self.zemY):
				if TEST: print('Si na zemi')
				self.jumpSegment = -self.jumpSegment
				self.isJumping = False
				self.firstJump = True
				self.positionY = self.zemY
				return

			if (self.positionY < self.hranica):
				if TEST: print('Hitol si hranicu')
				self.jumpSegment = -self.jumpSegment
			
			if (self.positionY <= self.zemY or self.positionY <= self.hranica):
				if TEST: print('skaces')
				rovnica = -((self.positionY / 20) ** 2)
				self.positionY += rovnica * self.jumpSegment
	
	# Draws
	def draw(self):
		if self.image is not None:
			self.rect = self.image.get_rect(x=self.positionX, y=self.positionY)
			self.surface.blit(self.image, self.rect)
	
	def jump(self):
		self.isJumping = True

	# Checks collisions
	def checkcollisions(self, obj:GameObject):
		return self.rect.colliderect(obj.rect)
	
	def shoot(self):
		[projectileX, projectileY] = self.positionX + self.width, self.positionY + (self.height //2)
		return Projectile(projectileX, projectileY, surface=self.surface, projectileSpeed=self.projectileSpeed)


'''Obstacle class'''
class Obstacle(GameObject):
	def __init__(self, positionX:int=0, positionY:int=0, width:int=100, height:int=25, color: pygame.Color = BLACK, imagePath: str = 'assets/images/ravine3.png', surface:pygame.Surface=None, speed:int=10) -> None:
		super().__init__(positionX, positionY, color, imagePath, surface, width, height)
		self.defaultPositionX = positionX
		self.defaultPositionY = positionY
		self.speed = speed
	
	def move(self):
		self.positionX -= self.speed

	def draw(self):
		self.rect = self.image.get_rect(x=self.positionX, y=self.positionY)
		self.surface.blit(self.image, self.rect)
	
	def resetPosition(self):
		self.positionX = self.defaultPositionX
		self.positionY = self.defaultPositionY
	
	def isOutOfScreen(self) -> bool:
		return self.positionX + self.width < 0


'''Enemy class'''
class Enemy(GameObject):
	def __init__(self, positionX:int=0, positionY:int=0, width:int=100, height:int=25, color: pygame.Color = BLACK, imagePath: str = 'assets/images/Enemy Land.png', surface:pygame.Surface=None, speed:int=10) -> None:
		super().__init__(positionX, positionY, color, imagePath, surface, width, height)
		self.defaultPositionX = positionX
		self.defaultPositionY = positionY
		self.speed = speed
		self.rect = self.image.get_rect(x=self.positionX, y=self.positionY)
	
	def move(self):
		self.positionX -= self.speed

	def draw(self):
		self.rect = self.image.get_rect(x=self.positionX, y=self.positionY)
		self.surface.blit(self.image, self.rect)
	
	def resetPosition(self):
		self.positionX = self.defaultPositionX
		self.positionY = self.defaultPositionY
	
	def isOutOfScreen(self) -> bool:
		return self.positionX + self.width < 0
	
	# Checks collisions
	def checkcollisions(self, obj: GameObject):
		return self.rect.colliderect(obj.rect)


'''Projectile class'''
class Projectile(GameObject):
	def __init__(self, positionX: int = 0, positionY: int = 0, color: pygame.Color = YELLOW, imagePath: str = None, surface: pygame.Surface = None, projectileSpeed:int=15, direction:Direction=Direction.RIGHT, width:int=10, height:int=5) -> None:
		super().__init__(positionX, positionY, color, imagePath, surface)
		self.w = width
		self.h = height
		self.rect = pygame.Rect(self.positionX, self.positionY, self.w, self.h)
		self.projectileSpeed = projectileSpeed
		self.direction = direction
	
	def move(self) -> bool:
		if (self.direction == Direction.RIGHT):
			self.rect.x += self.projectileSpeed
		
		if (self.direction == Direction.LEFT):
			self.rect.x -= self.projectileSpeed
	
	def isOutOfScreen(self) -> bool:
		if (self.direction == Direction.RIGHT):
			if(self.rect.x > self.surface.get_width()):
				return True
		if (self.direction == Direction.LEFT):
			if(self.rect.x < 0):
				return True
		return False
	
	def draw(self):
		pygame.draw.rect(self.surface, self.color, self.rect)


'''Game class'''
class Game():
	# Class constructor
	def __init__(self, windowWidth:int=640, windowHeight:int=480, fps:int=5,
							backgroundImagePath:str='assets/images/background_stars.png',
							groundSurfaceImagePath:str='assets/images/surface-final.png') -> None:
		self.windowWidth = windowWidth
		self.windowHeight = windowHeight
		self.fps = fps

		self.backgroundImagePath = backgroundImagePath
		self.groundSurfaceImagePath = groundSurfaceImagePath

		self.initialize()
		
		if TEST:
			self.scene.changeTo(self.scene.inGame)
		
	# Initializes the game
	def initialize(self):
		pygame.init()
		self.clock = pygame.time.Clock()
		self.surface = pygame.display.set_mode((self.windowWidth, self.windowHeight))
		self.setCaption('Moon Patrol v1.0 - FPV UMB')
		self.score = 0
		self.initializeObjects()
		self.scene = Scene(self)
		self.scene.initialize()
		self.groundSurfacePositionY = 150

		self.backgroundImage = pygame.image.load(self.backgroundImagePath)
		self.groundSurfaceSurface = pygame.image.load(self.groundSurfaceImagePath)
		self.groundSurfaceSurface = pygame.transform.scale(self.groundSurfaceSurface, (self.surface.get_width(), self.groundSurfacePositionY))

		self.addPlayers()

		self.paused = True
		self.RUNNING = True
	
	# Initializes objects
	def initializeObjects(self):
		self.player = None
		self.enemies: list[Enemy] = []
		self.objects: list[GameObject] = []

	# Adds players
	def addPlayers(self):
		self.addObject(Player(0, self.calculateGroundSurfaceY(), None, './assets/images/player2.png', self.surface, 10, 48, 24))
		self.addObject(Obstacle(self.surface.get_width(), self.calculateGroundSurfaceY() + 28, 100, 100, None, './assets/images/ravine3.png', self.surface, 8))
		self.addObject(Enemy(self.surface.get_width(), self.calculateGroundSurfaceY(), ENEMY_WIDTH, 24, None, 'assets/images/Enemy Land.png', self.surface, 5))

	def calculateGroundSurfaceY(self):
		return self.surface.get_height() - self.groundSurfacePositionY

	# Sets the window caption
	def setCaption(self, caption:str='') -> None:
		pygame.display.set_caption(caption)

	# Adds an object to belonging arrays
	def addObject(self, gameObject:GameObject):
		if isinstance(gameObject, Player): self.player = gameObject
		if isinstance(gameObject, Enemy):	self.enemies.append(gameObject)
		if isinstance(gameObject, GameObject): self.objects.append(gameObject)
	
	# Updates the screen from double buffer
	def update(self):
		pygame.display.flip()
		game.clock.tick(self.fps)
	
	def jumpPlayer(self):
		if (self.player is None): return
		self.player.jump()

	def moveObjects(self):
		for obj in self.objects:
			# Player
			if isinstance(obj, Player):
				self.player.move()
			# Obstacles
			if (isinstance(obj, Obstacle)):
				isOutOfScreen = obj.isOutOfScreen()
				if (isOutOfScreen):
					obj.resetPosition()
				else:
					obj.move()
			# Projectiles
			if (isinstance(obj, Projectile)):
				isOutOfScreen = obj.isOutOfScreen()
				if (isOutOfScreen):
					self.deleteObject(obj)
				else:
					obj.move()
			# Enemies
			if (isinstance(obj, Enemy)):
				isOutOfScreen = obj.isOutOfScreen()
				if (isOutOfScreen):
					obj.resetPosition()
				else:
					obj.move()

	def deleteObject(self, obj):
		self.objects.remove(obj)
		del obj
	
	# Checks collisions on all objects
	def checkCollisionOnAllObjects(self):
		for obj in self.objects:
			# Obstacles
			if isinstance(obj, Obstacle):
				if self.player.checkcollisions(obj):
					self.endCurrentGame()
			# Enemies
			if isinstance(obj, Enemy):
				if self.player.checkcollisions(obj):
					self.endCurrentGame()
			# Check destroying enemies
			for enemy in self.enemies:
				if (isinstance(obj, Projectile)):
					projectile = obj
					if enemy.checkcollisions(projectile):
						self.deleteObject(projectile)
						enemy.resetPosition()
						self.score += 1
	
	# Draws all the objects
	def draw(self):
		self.moveObjects()
		self.drawBackground()
		self.drawGroundSurface()
		self.drawAllObjects()
		self.checkCollisionOnAllObjects()
	
	def drawBackground(self):
		self.surface.blit(self.backgroundImage, (0, 0))
	
	def drawGroundSurface(self):
		groundSurfacePosition = (0, self.surface.get_height() - self.groundSurfaceSurface.get_height())
		self.surface.blit(self.groundSurfaceSurface, groundSurfacePosition)
	
	# Draws all objects
	def drawAllObjects(self):
		for gameObject in self.objects:
			gameObject.draw()
	
	# Draws the current scene
	def drawScene(self):
		self.scene.draw()
	
	# Pauses the current game
	def pause(self):
		if self.paused:
			self.scene.unpauseScene()
			self.paused = False
			return
		self.scene.pauseScene()
		self.paused = True
	
	# Exits the current game completely
	def quit(self):
		self.RUNNING = False
	
	# Ends the current game
	def endCurrentGame(self):
		self.scene.changeTo(self.scene.end)
		self.initializeObjects()
		self.addPlayers()
	
	# Resets the score
	def resetScore(self):
		self.score = 0
	
	# Checks if the current game is on
	def isInGame(self) -> bool:
		return self.scene.current == self.scene.inGame
	
	# Checks if the current game is paused
	def isPaused(self) -> bool:
		return self.scene.current == self.scene.pause
	
	def playerShootProjectile(self):
		projectileObject = self.player.shoot()
		self.addObject(projectileObject)


'''Game creating'''
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60
game = Game(WINDOW_WIDTH, WINDOW_HEIGHT, fps=FPS, backgroundImagePath='assets/images/background_stars.png')


'''Main event loop'''
while game.RUNNING:
	# Processing events
	for event in pygame.event.get():
		# Check if left mouse button was clicked
		if pygame.mouse.get_pressed(3)[0]:
			game.scene.current.update(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
		# Checks the keys if the game is playing or paused
		if game.isInGame() or game.isPaused():
			# Checks if any key is pressed
			if event.type == pygame.KEYDOWN:
				# Checks if the game should be paused
				if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
					game.pause()
				
				if not game.isPaused():
					# Player jumps when the spacebar is pressed
					if event.key == pygame.K_SPACE:
						print('space was pressed')
						game.jumpPlayer()
					# Player shoots when the "e" key is pressed
					if event.key == pygame.K_e:
						game.playerShootProjectile()

		# Checks if the game is about to be quitted
		if event.type == pygame.QUIT:
			game.quit()
			break
	# Draws the current scene
	game.drawScene()
	# Update double buffer
	game.update()


'''Quit afterparty'''
# Quits the game
pygame.quit()
# Frees the resources
sys.exit()
