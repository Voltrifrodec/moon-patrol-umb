from enum import Enum


class Difficulty(Enum):
    EASY = {
        
		# Game Settings
		"gameSpeed": 1,
		"scoreMultipler": 1.0,
     
		# Player Settings
		"jumpCount": 10,
		"jumpSegment": 0.065,
        "attackSpeed": 600,
     
		# Enemies and Obstacles Settings
  		"maximumEnemiesCount": 5,
  		"maximumFlyingEnemiesCount": 1,
        "enemySpeed": 7,
		"spawnRate": 1,
		"spawningSpeed": [1000, 1500],
  		"spawningSpeedFlyingEnemies": [5000,7500],
		"maximumObstaclesCount": 1,
		
  		# Projectile Settings
    	"projectileDelay": 700

    }
    MEDIUM = {

		# Game Settings
		"gameSpeed": 1.5,
		"scoreMultipler": 1.75,
     
		# Player Settings
		"jumpCount": 10,
		"jumpSegment": 0.065,
        "attackSpeed": 300,
     
		# Enemies and Obstacles Settings
  		"maximumEnemiesCount": 10,
  		"maximumFlyingEnemiesCount": 2,
        "enemySpeed": 10,
		"spawnRate": 2,
		"spawningSpeed": [700, 1200],
  		"spawningSpeedFlyingEnemies": [4000,6000],
		"maximumObstaclesCount": 1, # TODO: Zmeniť adekvátne!
		
  		# Projectile Settings
    	"projectileDelay": 400
  
	}
    DOOM_ETERNAL = {

		# Game Settings
		"gameSpeed": 2.5,
		"scoreMultipler": 3,
     
		# Player Settings
		"jumpCount": 10,
		"jumpSegment": 0.065,
        "attackSpeed": 100,
     
		# Enemies and Obstacles Settings
  		"maximumEnemiesCount": 15,
  		"maximumFlyingEnemiesCount": 5,
        "enemySpeed": 17,
		"spawnRate": 2,
		"spawningSpeed": [500, 1000],
  		"spawningSpeedFlyingEnemies": [2000,4000],
		"maximumObstaclesCount": 1, # TODO: Zmeniť adekvátne!
		
  		# Projectile Settings
    	"projectileDelay": 200
  
	}
