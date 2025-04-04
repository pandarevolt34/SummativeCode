#Student ID: 5676187

#The code below is the backbone of interface function:

import pygame #import pygame system

pygame.init() #start all pygame tools like graphics

#setting the size of game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("YOU'RE in trouble") #sets the title at the top of the window

#Defining screen:
#setting the starting position of the player
x = 200 #200 pixels from the left of the screen
y = 200 #200 pixels from the top of the screen
img = pygame.image.load('img/player/Idle/0.png') 
rectangle = img.get_rect() #used for control position for everything
rectangle.center = (x,y) #moves the rectangle (and image) to coordinates (200,200) ---> player's position


#to keep the game constantly running (controlling the main game loop)
game_running = True 
while game_running: #start the loop - keep going while the game is on
    
    screen.fill((255,255,255)) #this clears the screen to white at the start of every frame
    screen.blit(img, rectangle)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False #if player click close button,  the loop stops

pygame.quit()

#to be continued......
