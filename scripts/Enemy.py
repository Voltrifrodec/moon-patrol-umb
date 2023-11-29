import pygame
from scripts.GameObject import GameObject


BLACK = pygame.Color('black')
global ENEMY_WIDTH
ENEMY_WIDTH = 48

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


'''Flying Enemy class'''
class FlyingEnemy(GameObject):
	pass