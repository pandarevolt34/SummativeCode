#Student ID: 5676187

import pygame 
import random 

pygame.init() 


#the font function for interface
font = pygame.font.SysFont(None, 30)

#setting the size of game window
window = pygame.display.set_mode((900, 700))
pygame.display.set_caption("YOU'RE in trouble") #sets the title at the top of the window

#Background Image
background_img = pygame.transform.scale(pygame.image.load("Python image/BackG.png"), (900, 700))

#Cards
class Cards:
    def __init__(self, name, image, card_positions):
        self.name = name
        self.image = image
        self.card_positions = card_positions
    def draw(self,window):
        window.blit(self.image, self.card_positions)
        
#Button
class TheButton:
    def __init__(self, text, x, y, activated):
        self.text = text
        self.x = x #position x
        self.y = y #position y
        self.activated = activated #to see whether button is enabled
        self.rect = pygame.Rect((self.x, self.y), (80, 37)) #pygame.Rect object that shows the clicklable area of the button

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
player = pygame.transform.scale(pygame.image.load("Python image/Player.jpg").convert_alpha(), (250,200)) #width and height both 200
              
#LOAD IMAGES + IMAGE SIZES AND POSITIONS:
#e.g. image size (100, 150)
#1. Main Cards
main_cards = {
    "shield_image" : (pygame.transform.scale(pygame.image.load("Python image/shield.png").convert_alpha(), (100, 150)), (50, 190)), 
    "trouble_image" : (pygame.transform.scale(pygame.image.load("Python image/Trouble.png").convert_alpha(), (100, 150)), (170, 190)),
    }

#2. Action Cards
action_cards = {
    "sick_leave" : (pygame.transform.scale(pygame.image.load("Python image/sickleave.png").convert_alpha(), (100, 150)), (340, 190)),
    "U_turn" : (pygame.transform.scale(pygame.image.load("Python image/Uturn (2).png").convert_alpha(), (100, 150)), (460, 190)),
    "Hacker" : (pygame.transform.scale(pygame.image.load("Python image/hacker (2).png").convert_alpha(), (100, 150)), (580, 190)),
    "TheSpell" : (pygame.transform.scale(pygame.image.load("Python image/spell.png").convert_alpha(), (100, 150)), (700, 190)),
    "Shuffle" : (pygame.transform.scale(pygame.image.load("Python image/shuffle.png").convert_alpha(), (100, 150)), (820, 350)),
    "Reveal" : (pygame.transform.scale(pygame.image.load("Python image/reveal.png").convert_alpha(), (100, 150)), (940, 350)),
    "BeatIt" : (pygame.transform.scale(pygame.image.load("Python image/beat.png").convert_alpha(), (100, 150)), (460, 350)),
    "BegYou" : (pygame.transform.scale(pygame.image.load("Python image/beg.png").convert_alpha(), (100, 150)), (580, 350)),
    "no_chance" : (pygame.transform.scale(pygame.image.load("Python image/no chance.png").convert_alpha(), (100, 150)), (700, 350)),
    "mirror" : (pygame.transform.scale(pygame.image.load("Python image/mirror.png").convert_alpha(), (100, 150)), (820, 350)),
}

#3. Character Cards
character_cards = {
    "char1_image" : (pygame.transform.scale(pygame.image.load("Python image/char1.png").convert_alpha(), (100, 150)), (100, 350)),
    "char2_image" : (pygame.transform.scale(pygame.image.load("Python image/char2.png").convert_alpha(), (100, 150)), (220, 350)),
    "char3_image" : (pygame.transform.scale(pygame.image.load("Python image/char3.png").convert_alpha(), (100, 150)), (340, 350)),
    "char4_image" : (pygame.transform.scale(pygame.image.load("Python image/char4.png").convert_alpha(), (100, 150)), (460, 350)),
    "char5_image" : (pygame.transform.scale(pygame.image.load("Python image/char5.png").convert_alpha(), (100, 150)), (580, 350)),
    "char6_image" : (pygame.transform.scale(pygame.image.load("Python image/char6.png").convert_alpha(), (100, 150)), (700, 350)),
}

button = TheButton("Shuffle", 800,  600, True)
full_deck = list(main_cards.values()) + list(action_cards.values()) + list(character_cards.values())



#MAIN GAME LOOP
game_running = True
while game_running: #start the loop - keep going while the game is on
    #event handler
    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            game_running = False #if player click close button, the loop stops
    
    window.fill((255,0,0)) #fill background colour
    

#Background images(must come first so that it wont cover the card images)
    window.blit(background_img, (0,0))

#Player image (position)
    window.blit(player, (340, 505))

    #grouped all cards 
    all_cards = {}
    all_cards.update(main_cards)
    all_cards.update(action_cards)
    all_cards.update(character_cards)

    # Draw all cards at once
    for name, (image, position) in all_cards.items(): #items(), lopping dict
        window.blit(image, position)

    button.draw()

    if button.gets_clicked():
        print("Deck Shuffled!")
    random.shuffle(full_deck)


    pygame.display.update()


pygame.quit()


