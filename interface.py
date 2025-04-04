Student ID: 5676187

import pygame #import sysdt

pygame.init() #start all pygame tools like graphics

#setting the size of game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("YOU'RE in trouble") #sets the title at the top of the window

#to keep the game constantly running (controlling the main game loop)
game_running = True 
while game_running: #start the loop - keep going while the game is on
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False #if player click close button,  the loop stops
pygame.quit

