import pygame
from scripts.GameObject import GameObject
from scripts.Direction import Direction

YELLOW = pygame.Color('yellow')


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