import pygame #import pygame system

pygame.init() #start all pygame tools like graphics

#setting the size of game window
window = pygame.display.set_mode((900, 700))
pygame.display.set_caption("YOU'RE in trouble") #sets the title at the top of the window
clock = pygame.time.Clock()

#load and scale images
shield_image = pygame.transform.scale(pygame.image.load("Shield.png"), (100, 150))
trouble_image = pygame.transform.scale(pygame.image.load("trouble.png"), (100, 150))
char1_image = pygame.transform.scale(pygame.image.load("char1.png"), (100, 150))
char2_image = pygame.transform.scale(pygame.image.load("char2.png"), (100, 150))

#Card data
shield_cards = [{"name": "shield", "colour":(128,128,128), "image":shield_image}]
trap_cards = [{"name": "You're in Trouble", "colour" : (255, 0, 0), "image":trouble_image}]
character_cards = [{"name" :"character 1", "colour" : (0, 255, 255), "image":char1_image}, 
                   {"name": "character 2", "colour" : (0, 0, 128), "image" : char2_image}]


#Main Game Loop
game_running = True 
while game_running: #start the loop - keep going while the game is on
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False #if player click close button,  the loop stops
    
    window.fill((255,255,255))

#show image using pygame blit
    window.blit(shield_image, (100,150)) #function to draw card
    window.blit(trouble_image, (220,150)) #function to draw card
    window.blit(char1_image, (340,150)) #function to draw card
    window.blit(char2_image, (460,150)) #function to draw card

    pygame.display.update()

pygame.quit()
