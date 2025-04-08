#The code below is the backbone of interface function:

import pygame #import pygame system

pygame.init() #start all pygame tools like graphics

#setting the size of game window
window = pygame.display.set_mode((900, 700))
pygame.display.set_caption("YOU'RE in trouble") #sets the title at the top of the window
clock = pygame.time.Clock()

action_cards = 
shield_cards = [{"name": "shield", "colour":(128,128,128)}]
trap_cards = [{"name": "You're in Trouble", "colour" : (255, 0, 0)}]
character_cards = [{"name" :"character 1", "colour" : (0, 255, 255)}, {"name": "character 2", "colour" : (0, 0, 128)}, {"name": "character 3", "colour" : (0, 0, 255)}]

#Main Game Loopp)
game_running = True 
while game_running: #start the loop - keep going while the game is on
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False #if player click close button,  the loop stops


pygame.quit()
#to be continued......
