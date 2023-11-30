import pygame
from scripts.GameObject import GameObject
from scripts.Projectile import Projectile


'''Player class'''
class Player(GameObject):
	def __init__(self, positionX, positionY, color: pygame.Color = None, imagePath: str = None, screen=None, projectileSpeed=10, width=48, height=28) -> None:
		super().__init__(positionX, positionY, color, imagePath, screen, width, height)
		self.startingPosition = positionX, positionY
		self.jumpCount = 10
		self.isJumping = False
		self.firstJump = True
		self.jumpSegment = 0.065 # 0.045 → 0.065, kvoli prekazke
		self.hranica = 200 # TODO: Change
		self.zemY = self.rect.y
		self.projectileSpeed = projectileSpeed
		self.hitCeiling = False

	# Moves
	def move(self):
		if (self.isJumping):
			# if TEST: print('jumping')
			if (self.firstJump):
				self.rect.y -= 2 * self.jumpCount
				self.firstJump = False
				self.fallSpeed = self.jumpCount  

			if (self.rect.top >= self.zemY):
				# if TEST: print('Si na zemi')
				self.jumpSegment = -self.jumpSegment
				self.isJumping = False
				self.firstJump = True
				self.positionY = self.zemY
				self.hitCeiling = False
				self.fallSpeed = 0.05
				return

			if (self.positionY < self.hranica):
				# if TEST: print('Hitol si hranicu')
				self.jumpSegment = -self.jumpSegment
				self.hitCeiling = True
			
			if (self.positionY <= self.zemY or self.positionY <= self.hranica):
				# if TEST: print('skaces')
				if(self.hitCeiling is True):
					pass
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
