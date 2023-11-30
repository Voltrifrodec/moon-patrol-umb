import pygame, random
from scripts.Scene import Scene
from scripts.Enemy import Enemy, ENEMY_WIDTH
from scripts.GameObject import GameObject
from scripts.Player import Player
from scripts.Obstacle import Obstacle
from scripts.Projectile import Projectile
from scripts.Difficulty import Difficulty
import math

'''Game class'''
class Game():
	# Class constructor
	def __init__(self, windowWidth:int=640, windowHeight:int=480, fps:int=5,
							backgroundImagePath:str='assets/images/background_stars.png',
							groundSurfaceImagePath:str='assets/images/surface-final.png') -> None:
		self.windowWidth = windowWidth
		self.windowHeight = windowHeight
		self.fps = fps
		self.difficulty = Difficulty.EASY # Default mode
		self.backgroundImagePath = backgroundImagePath
		self.groundSurfaceImagePath = groundSurfaceImagePath

		self.initialize()
		
		# if TEST:
		# 	self.scene.changeTo(self.scene.inGame)
			
	# Initializes the game
	def initialize(self):
		pygame.init()
		self.clock = pygame.time.Clock()
		self.surface = pygame.display.set_mode((self.windowWidth, self.windowHeight))
		self.setCaption('Moon Patrol v2.0.0 - FPV UMB')
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
		self.addObject(Player(0, self.calculateGroundSurfaceY() + 5, None, './assets/images/player2.png', self.surface, 20, 48, 24))
		self.addObject(Obstacle(self.surface.get_width(), self.calculateGroundSurfaceY() + 28, 100, 100, None, './assets/images/ravine3.png', self.surface, 8))
		self.addObject(Enemy(self.surface.get_width(), self.calculateGroundSurfaceY(), ENEMY_WIDTH, 24, None, (f'assets/images/Enemy Land_{random.randint(1,4)}.png'), self.surface, self.difficulty.value["enemySpeed"]))

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
		self.clock.tick(self.fps)
	
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
					self.score += math.ceil(1 * self.difficulty.value["scoreMultipler"]) 
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
					self.score += math.ceil(1 * self.difficulty.value["scoreMultipler"]) 
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
						print("\tBoom, he got shot fr ong +1 L ration average Bratislava resident vibes 2004 Techno House Party")
						self.deleteObject(enemy)
						self.enemies.remove(enemy)
						self.deleteObject(projectile)
						self.score += math.ceil(1 * self.difficulty.value["scoreMultipler"])
						return

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

	def getEnemiesCount(self):
		return len(self.enemies)
	
	def getPlayerAttackSpeed(self) -> int:
		return self.difficulty.value["attackSpeed"]

	def enemySpawn(self):
		for iteration in range(0, self.difficulty.value["spawnRate"]):
			print(f'Creating {self.difficulty.value["spawnRate"]} enemies...')
			enemy = Enemy(self.surface.get_width() + iteration * random.randint(50,100), self.calculateGroundSurfaceY(), ENEMY_WIDTH, 24, None, ('assets/images/Enemy Land_{}.png'.format(random.randint(1,4))), self.surface, self.difficulty.value["enemySpeed"])
			self.addObject(enemy)
			
	def setDifficulty(self, difficulty=Difficulty) -> None:
		print(f"Selected difficulty: {self.difficulty}")
		self.difficulty = difficulty
