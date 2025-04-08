import pygame #import pygame system

pygame.init() #start all pygame tools like graphics

#setting the size of game window
window = pygame.display.set_mode((900, 700))
pygame.display.set_caption("YOU'RE in trouble") #sets the title at the top of the window

#Defining screen:
#setting the starting position of the player
x = 200 
y = 200 
width = 40
height = 60
vel = 5 

#Min Game Loopp)
game_running = True 
while game_running: #start the loop - keep going while the game is on
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False #if player click close button,  the loop stops
    
    #move character by the velocity based on the their direction
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        x -= vel
    if keys[pygame.K_RIGHT]:
        x += vel
    if keys [pygame.K_UP]:
        y -= vel
    if keys[pygame.K_DOWN]:
        y += vel
    
    window.fill((0,0,0)) #fill screen before image
#rectangle
    pygame.draw.rect(window, (255, 255, 255), (x, y ,width, height))
    pygame.display.update()


pygame.quit()

#to be continued......
