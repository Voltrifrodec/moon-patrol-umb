import pygame


BLACK = pygame.Color('black')

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