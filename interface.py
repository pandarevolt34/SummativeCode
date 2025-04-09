
import pygame 

pygame.init() 

#setting the size of game window
window = pygame.display.set_mode((900, 700))
pygame.display.set_caption("YOU'RE in trouble") #sets the title at the top of the window

#Background Image
background_img = pygame.transform.scale(pygame.image.load("Python image/Background.jpg"), (900, 700))

#load and scale images
shield_image = pygame.transform.scale(pygame.image.load("Python image/shield.png").convert_alpha(), (100, 150))
trouble_image = pygame.transform.scale(pygame.image.load("Python image/trouble.png").convert_alpha(), (100, 150))
char1_image = pygame.transform.scale(pygame.image.load("Python image/char1.png").convert_alpha(), (100, 150))
char2_image = pygame.transform.scale(pygame.image.load("Python image/char2.png").convert_alpha(), (100, 150))
char3_image = pygame.transform.scale(pygame.image.load("Python image/char3.png").convert_alpha(), (100, 150))
char4_image = pygame.transform.scale(pygame.image.load("Python image/char4.png").convert_alpha(), (100, 150))


#Main Game Loop
game_running = True
while game_running: #start the loop - keep going while the game is on
    #event handler
    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            game_running = False #if player click close button, the loop stops
    
    window.fill((255,0,0))

#show image using pygame blit
    window.blit(background_img, (0,0))
    window.blit(shield_image, (100,400))
    window.blit(trouble_image, (220,400)) 
    window.blit(char1_image, (340,400)) 
    window.blit(char2_image, (460,400))
    window.blit(char3_image, (580,400))
    window.blit(char4_image, (700,400))
    
    pygame.display.update()


pygame.quit()

