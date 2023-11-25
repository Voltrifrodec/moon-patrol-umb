'''Imports'''
# sys module
import sys
# PyGame module
import pygame
# Random module
import random

import numpy as np

'''Variable for testing'''
global TEST
TEST = False


'''Global variables/constants'''
WHITE = pygame.Color('white')
BLACK = pygame.Color('black')


'''Class declarations'''
class Game(): ...
class Scene(): ...
class MainMenu(): ...
class InGame(): ...
class Pause(): ...
class End(): ...
class Text(): ...

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
		self.current = None
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
		# TODO: You won info with points, green text color
		# TODO: You lost info with points, red text color
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
	def __init__(self, positionX:int=0, positionY:int=0, color:pygame.Color=BLACK, imagePath:str=None, surface:pygame.Surface=None) -> None:
		self.positionX = positionX
		self.positionY = positionY
		self.color = color
		self.imagePath = imagePath
		self.image = None
		self.screen = surface

		if color is not None:
			self.color = pygame.color.Color(color)
		
		if imagePath is not None:
			self.image = pygame.image.load(imagePath)
			self.image = pygame.transform.scale(self.image, (32, 32))
			self.imageRectangle = self.image.get_rect(x=positionX, y=positionY)
			self.imageWidth = self.image.get_width()
			self.imageHeight = self.image.get_height()
	
	# Draws object on screen
	def draw(self):
		if self.image is not None:
			self.imageRectangle = self.image.get_rect(x=self.positionX, y=self.positionY)
			self.screen.blit(self.image, self.imageRectangle)
	
	# Checks positions
	def checkcollision(self, x:int, y:int):
		return self.positionX == x or self.positionY == y

'''Player class'''
class Player(GameObject):
	def __init__(self, positionX, positionY, color: pygame.Color = None, imagePath: str = None, screen=None) -> None:
		super().__init__(positionX, positionY, color, imagePath, screen)
		self.startingPosition = positionX, positionY
		self.jumpCount = 10
		self.isJumping = False
		self.firstJump = True
		self.jumpSegment = 0.065 # 0.045 → 0.065, kvoli prekazke
		self.hranica = 200 # TODO: Change
		self.zemY = self.imageRectangle.y

		print(self.zemY)
		print(self.zemY)
	
	# Moves
	def move(self):
		if (self.isJumping):
			if (self.firstJump):
				self.imageRectangle.y -= 2 * self.jumpCount
				self.firstJump = False

			if (self.imageRectangle.top >= self.zemY):
				print('Si na zemi')
				self.jumpSegment = -self.jumpSegment
				self.isJumping = False
				self.firstJump = True
				self.imageRectangle.y = self.zemY
				return

			if (self.positionY <= self.hranica):
				print('Hitol si hranicu')
				self.jumpSegment = -self.jumpSegment
			
			if (self.imageRectangle.y <= self.zemY or self.imageRectangle.y >= self.hranica):
				print(f'skaces{self.imageRectangle.y}')
				print(f'posY: {self.positionY}')
				rovnica = -((self.positionY / 18) ** 2)
				print(f'rovnica: {rovnica}')
				self.positionY += rovnica * self.jumpSegment
	
	# Draws
	def draw(self):
		# print('draw was called.')
		if self.image is not None:
			# print('drawing image')
			self.imageRectangle = self.image.get_rect(x=self.positionX, y=self.positionY)
			self.screen.blit(self.image, self.imageRectangle)
	
	def jump(self):
		self.isJumping = True

	# Checks collisions
	def checkcollisions(self, obj:GameObject):
		return self.imageRectangle.colliderect(obj.imageRectangle)

'''Obstacle class'''
class Obstacle(GameObject):
	def __init__(self, positionX:int=0, positionY:int=0, width:int=100, height:int=25, color: pygame.Color = BLACK, imagePath: str = 'assets/images/ravine3.png', screen:pygame.Surface=None) -> None:
		super().__init__(positionX, positionY, color, imagePath, screen)
		self.w = width
		self.h = height
		self.surface = pygame.image.load("assets/images/surface-final.png")
		self.surface = pygame.transform.scale(self.surface, (WINDOW_WIDTH, WINDOW_HEIGHT + 50))
		self.rect = pygame.Rect(self.surface.get_width(), self.surface.get_height() - self.surface.get_height() - 21, self.w, self.h)
		self.image = pygame.image.load('assets/images/ravine3.png')
		self.speed = 10
	
	def move(self):
		if(self.rect.x > -self.rect.w):
			self.rect.x -= self.speed
		else:
			self.rect.x = self.surface.get_width()

	def render(self):
		self.move()
		self.screen.blit(self.image, self.rect)

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
		
	# Initializes objects
	def initializeObjects(self):
		self.player = None
		self.enemies = []
		self.objects: list[GameObject] = []
		self.points = []

	# Adds players
	def addPlayers(self):
		# TODO: ADD Player as a vehicle
		self.addObject(Player(0, self.calculateGroundSurfaceY(), None, './assets/images/player2.png', self.surface))
		# TODO: Add Enemy, that will be destroyed
		# TODO: Add Obstacle
		# self.addObject(Obstacle(self.screen.get_width(), self.screen.get_height(), 100, 25, 'Player', BLACK, './assets/images/player2.png', self.screen))
		# self.addObject(Enemy(32*8, 32*5, 'Ragdolle', None, './assets/images/enemy1.png', self.screen))
		# self.addObject(Enemy(32*9, 32*5, 'Oilerov', None, './assets/images/enemy2.png', self.screen))
		pass

	def calculateGroundSurfaceY(self):
		return 400
		return self.surface.get_rect().y - self.groundSurfaceSurface.get_height()
	
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

		self.backgroundImage = pygame.image.load(self.backgroundImagePath)
		self.groundSurfaceSurface = pygame.image.load(self.groundSurfaceImagePath)
		self.groundSurfaceSurface = pygame.transform.scale(self.groundSurfaceSurface, (self.surface.get_width(), 150))

		self.addPlayers()

		self.paused = True
		self.RUNNING = True

	# Sets the window caption
	def setCaption(self, caption:str='') -> None:
		pygame.display.set_caption(caption)

	# Adds an object to belonging arrays
	def addObject(self, gameObject:GameObject):
		if isinstance(gameObject, Player): self.player = gameObject
		# if isinstance(gameObject, Enemy):	self.enemies.append(gameObject)
		# if isinstance(gameObject, Point): 	self.points.append(gameObject)
		if isinstance(gameObject, GameObject): self.objects.append(gameObject)
	
	# Updates the screen from double buffer
	def update(self):
		pygame.display.flip()
		game.clock.tick(self.fps)
	
	# Moves the player and checkes the interference with other objects
	def movePlayer(self):
		if (self.player is None): return
		self.player.move()

	def jumpPlayer(self):
		if (self.player is None): return
		self.player.jump()

	# Moves all the enemies and checkes the interference with other objects
	def moveEnemies(self):
		for n in self.enemies:
			n.direction.randomDirection()

			enemyDirection = n.direction.currentDirection

			nextX = n.positionY // n.imageHeight + enemyDirection[1]
			nextY = n.positionX // n.imageWidth + enemyDirection[0]

			n.move()
	
	# Checks collisions on all objects
	def checkCollisionOnAllObjects(self):
		for enemy in self.enemies:
			print(enemy)
			if self.player.checkcollisions(enemy):
				self.endCurrentGame()
	
	# Draws all the objects
	def draw(self):
		self.moveEnemies()
		self.movePlayer()
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
		# TODO: Add player.shoot method
		# self.player.shoot()
		pass


'''Game creating'''
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 30
game = Game(WINDOW_WIDTH, WINDOW_HEIGHT, fps=FPS, backgroundImagePath='assets/images/background_stars.png')


'''Main event loop'''
while game.RUNNING:
	# Processing events
	for event in pygame.event.get():
		# Check left mouse button click
		if pygame.mouse.get_pressed(3)[0]:
			game.scene.current.update(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
		# Checks the keys if the game is playing or paused
		if game.isInGame() or game.isPaused():
			# Checks if any key is pressed
			if event.type == pygame.KEYDOWN:
				# Checks if the game should be paused
				if event.key == pygame.K_ESCAPE \
					or event.key == pygame.K_p: game.pause()
				# Player jumps when the spacebar is pressed
				if event.key == pygame.K_SPACE: game.jumpPlayer()
				
				if event.key == pygame.K_e:
					print('Player shot a projectile!')
					game.playerShootProjectile()

		# Checks if the game is about to be quitted
		if event.type == pygame.QUIT:
			game.quit()
	# Draws the current scene
	game.drawScene()
	# Update double buffer
	game.update()


'''Quit afterparty'''
# Quits the game
pygame.quit()
# Frees the resources
sys.exit()
