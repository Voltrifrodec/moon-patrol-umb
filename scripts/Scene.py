import pygame
from scripts.Text import Text
from . import Game



BLACK = pygame.Color('black')


class Scene(): ...

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
		self.game.surface.blit(self.paused.rendered, self.paused.position)

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
		self.game.surface.blit(self.gameEnded.rendered, self.gameEnded.position)
		self.game.surface.blit(self.finalScore.rendered, self.finalScore.position)
		self.game.surface.blit(self.menu.rendered, self.menu.position)
	# Updates if button is clicked
	def update(self, x:int, y:int) -> None:
		if self.menu.doesCollide(x, y):
			self.game.scene.changeTo(self.game.scene.menu)