'''Imports'''
# sys module
import sys
from time import sleep
# PyGame module
import pygame
# Random module
import random

import numpy as np

from enum import Enum

'''Project Imports'''
# from scripts.Text import Text as Text
# from scripts.Scene import Scene as Scene
from scripts.Game import Game
'''Variable for testing'''
global TEST
TEST = False # Change to true, if you want to be ingame right away


'''Global variables/constants'''
WHITE = pygame.Color('white')
BLACK = pygame.Color('black')
YELLOW = pygame.Color('yellow')
ENEMY_WIDTH = 48

'''Class declarations'''
# class Game(): ...
# # class Scene(): ...
# class MainMenu(): ...
# class InGame(): ...
# class Pause(): ...
# class End(): ...
# class Text(): ...

















'''Game creating'''
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60
game = Game(WINDOW_WIDTH, WINDOW_HEIGHT, fps=FPS, backgroundImagePath='assets/images/background_stars.png')


'''Difficulties Setting'''
DIFFICULTIES = {
	"easy": {
     
		# Game Settings
		"gameSpeed": 1,
		"scoreMultipler": 1.0,
     
		# Player Settings
		"jumpCount": 10,
		"jumpSegment": 0.065,
     
		# Enemies and Obstacles Settings
  		"maximumEnemiesCount": 5,
  		"maximumFlyingEnemiesCount": 1,
		"spawnRate": 1,
		"spawningSpeed": [1000, 1500],
  		"spawningSpeedFlyingEnemies": [5000,7500],
		"maximumObstaclesCount": 1,
		
  		# Projectile Settings
    	"projectileDelay": 700
     
	},
	"medium": {

		# Game Settings
		"gameSpeed": 1.5,
		"scoreMultipler": 1.75,
     
		# Player Settings
		"jumpCount": 10,
		"jumpSegment": 0.065,
     
		# Enemies and Obstacles Settings
  		"maximumEnemiesCount": 10,
  		"maximumFlyingEnemiesCount": 2,
		"spawnRate": 1,
		"spawningSpeed": [700, 1200],
  		"spawningSpeedFlyingEnemies": [4000,6000],
		"maximumObstaclesCount": 1, # TODO: Zmeniť adekvátne!
		
  		# Projectile Settings
    	"projectileDelay": 400
  
	},
	"doom": {

		# Game Settings
		"gameSpeed": 2.5,
		"scoreMultipler": 3,
     
		# Player Settings
		"jumpCount": 10,
		"jumpSegment": 0.065,
     
		# Enemies and Obstacles Settings
  		"maximumEnemiesCount": 15,
		"spawnRate": 1,
		"spawningSpeed": [500, 1000],
  		"spawningSpeedFlyingEnemies": [2000,4000],
		"maximumObstaclesCount": 1, # TODO: Zmeniť adekvátne!
		
  		# Projectile Settings
    	"projectileDelay": 200
  
	}
	
}

'''Main event loop'''
previous_time = pygame.time.get_ticks()
previous_time_enemies = pygame.time.get_ticks()
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
						current_time = pygame.time.get_ticks()
						if current_time - previous_time > 700:
							previous_time = current_time
							game.playerShootProjectile()
       
					if game.getEnemiesCount() < 5:
						current_time = pygame.time.get_ticks()
						print("Current enemies: {}".format(game.getEnemiesCount()))
						if current_time - previous_time_enemies > random.randint(500,1000):
							previous_time_enemies = current_time
							game.enemySpawn()

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
