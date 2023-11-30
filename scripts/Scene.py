import pygame
from scripts import Game
from scripts.Text import Text
from scripts.Difficulty import Difficulty
from . import Game
import os

BLACK = pygame.Color('black')


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
		self.difficulty = DificultyScene(self.game)
		self.changeTo(self.menu)
	
	# Pauses game
	def pauseScene(self) -> None:
		self.changeTo(self.pause)
	
	# Unpauses game
	def unpauseScene(self) -> None:
		self.changeTo(self.inGame)
	
	# Changes scene
	def changeTo(self, scene:'Scene') -> None:
		self.current = scene
	
	# Draws current scene
	def draw(self):
		self.current.draw()
	
	# Updates the current scene
	def update(self, x:int, y:int) -> None:
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
		self.play.changePosition((self.game.windowWidth//2 - self.play.width//2, 1/4*self.game.windowHeight - self.play.fontSizePixel))
		self.quit = Text('QUIT', fontSize)
		self.quit.changePosition((self.game.windowWidth//2 - self.play.width//2, 3/4*self.game.windowHeight - self.play.fontSizePixel))
	
	# Draws scene
	def draw(self) -> None:
		if self.game.score != 0: self.game.score = 0
		self.game.surface.fill(BLACK)
		self.game.surface.blit(self.play.rendered, self.play.position)
		self.game.surface.blit(self.quit.rendered, self.quit.position)
	
	# Updates if buttons are clicked
	def update(self, x:int, y:int) -> None:
		if self.play.doesCollide(x, y):
			self.game.scene.changeTo(self.game.scene.difficulty)
		if self.quit.doesCollide(x, y):
			self.game.quit()


'''Difficulty select'''
class DificultyScene(Scene):
	def __init__(self, game: Game) -> None:
		super().__init__(game)
		self.initialize()
		self.name = 'Select difficulty'
	
	def initialize(self) -> None:
		fontSizePixel = 40
		self.difficulty = Text("Select difficulty", 30)
		self.difficulty.changePosition((self.game.windowWidth//2 - self.difficulty.width//2, 1 * self.difficulty.fontSizePixel))

		self.difficultyEasy = Text("Easy", fontSizePixel)
		self.difficultyMedium = Text("Medium", fontSizePixel)
		self.difficultyHard = Text("Doom Eternal", fontSizePixel)

		goBackButtonFontSizePixel = 20
		self.goBackButton = Text("Return to main menu", goBackButtonFontSizePixel)
		goBackButtonPosition = (self.game.windowWidth//2 - self.goBackButton.width//2, \
														self.game.windowHeight - self.goBackButton.height - 10)
		self.goBackButton.changePosition(goBackButtonPosition)

		self.difficultyEasy.changePosition((self.game.windowWidth//2 - self.difficultyEasy.width//2,
																				1/4*self.game.windowHeight - self.difficultyEasy.fontSizePixel + 50))
		self.difficultyMedium.changePosition((self.game.windowWidth//2 - self.difficultyMedium.width//2,
																				2/4*self.game.windowHeight - self.difficultyMedium.fontSizePixel))
		self.difficultyHard.changePosition((self.game.windowWidth//2 - self.difficultyHard.width//2,
																				3/4*self.game.windowHeight - self.difficultyHard.fontSizePixel - 50))

	def draw(self):
		self.initialize()
		self.game.surface.fill(BLACK)
		self.game.surface.blit(self.difficulty.rendered, self.difficulty.position)
		self.game.surface.blit(self.difficultyHard.rendered, self.difficultyHard.position)
		self.game.surface.blit(self.difficultyMedium.rendered, self.difficultyMedium.position)
		self.game.surface.blit(self.difficultyEasy.rendered, self.difficultyEasy.position)
		self.game.surface.blit(self.goBackButton.rendered, self.goBackButton.position)
		
	def update(self, x:int, y:int) -> None:
		if self.difficultyEasy.doesCollide(x,y):
			self.game.setDifficulty(Difficulty.EASY)
			self.game.scene.changeTo(self.game.scene.inGame)
		if self.difficultyMedium.doesCollide(x, y):
			self.game.setDifficulty(Difficulty.MEDIUM)
			self.game.scene.changeTo(self.game.scene.inGame)
		if self.difficultyHard.doesCollide(x, y):
			self.game.setDifficulty(Difficulty.DOOM_ETERNAL)
			self.game.scene.changeTo(self.game.scene.inGame)
		if self.goBackButton.doesCollide(x, y):
			self.game.scene.changeTo(self.game.scene.menu)
		

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
		# Sound effect source: https://www.fesliyanstudios.com/play-mp3/2459
		fontSize = 50
		self.sound = pygame.mixer.Sound(os.path.join('sound', '../assets/Small-Grenade-Explosion.mp3'))
		pygame.mixer.Sound.play(self.sound, 1, 2)
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