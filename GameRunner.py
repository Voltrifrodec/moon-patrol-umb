import pygame
from sys import exit


isRunning = True
while isRunning:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            exit()