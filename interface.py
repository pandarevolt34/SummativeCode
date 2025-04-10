Student ID: 5676187

import pygame 

pygame.init() 


#the font function for interface
font = pygame.font.SysFont(None, 30)

#setting the size of game window
window = pygame.display.set_mode((900, 700))
pygame.display.set_caption("YOU'RE in trouble") #sets the title at the top of the window


#Background Image
background_img = pygame.transform.scale(pygame.image.load("Python image/Background.jpg"), (900, 700))

class TheButton:
    def __init__(self, text, x, y, activated):
        self.text = text
        self.x = x #position x
        self.y = y #position y
        self.activated = activated #to see whether button is enabled
        self.rect = pygame.Rect((self.x, self.y), (80, 37)) #pygame.Rect objhect that shows the clicklable area of the button

    #draw button 
    def draw(self):
        button_text = font.render(self.text, True, (255, 255, 255))
        button_rect = pygame.Rect((self.x, self.y),(80, 37))
        pygame.draw.rect(window, (0,0,0), button_rect)
        window.blit(button_text, (self.x +10, self.y +10))
    
    #mouse click detection
    def gets_clicked(self): #make button clickable
        mouse_position = pygame.mouse.get_pos() #gets current position of the mouse
        if self.rect.collidepoint(mouse_position): #check if mouse inside rect area
            if pygame.mouse.get_pressed()[0]: #check if left mouse button is pressed
                print("Click")


#load and scale images
shield_image = pygame.transform.scale(pygame.image.load("Python image/shield.png").convert_alpha(), (100, 150))
trouble_image = pygame.transform.scale(pygame.image.load("Python image/trouble.png").convert_alpha(), (100, 150))
char1_image = pygame.transform.scale(pygame.image.load("Python image/char1.png").convert_alpha(), (100, 150))
char2_image = pygame.transform.scale(pygame.image.load("Python image/char2.png").convert_alpha(), (100, 150))
char3_image = pygame.transform.scale(pygame.image.load("Python image/char3.png").convert_alpha(), (100, 150))
char4_image = pygame.transform.scale(pygame.image.load("Python image/char4.png").convert_alpha(), (100, 150))

button = TheButton("Push!", 800,  600, True)

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
    
    button.draw()

    if button.gets_clicked():
        print("Click!")

    pygame.display.update()


pygame.quit()

#to be continued.......
