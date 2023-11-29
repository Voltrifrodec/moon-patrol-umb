import pygame
from scripts.GameObject import GameObject

BLACK = pygame.Color('black')

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