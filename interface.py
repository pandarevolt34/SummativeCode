#Student ID: 5676187
import pygame 
import random 

pygame.init() 


#the font function for interface
font = pygame.font.SysFont(None, 30)

#setting the size of game window
window = pygame.display.set_mode((900, 700))
pygame.display.set_caption("YOU'RE in trouble") #sets the title at the top of the window

#Background Images
background_img = pygame.transform.scale(pygame.image.load("Python image/BackG.png"), (900, 700))
menu_img = pygame.transform.scale(pygame.image.load("Python image/menu image.png"), (900, 700))
paused_img = pygame.transform.scale(pygame.image.load("Python image/paused image.jpg"), (900, 700))

#player image   
player = pygame.transform.scale(pygame.image.load("Python image/Player.jpg").convert_alpha(), (250,200)) #width and height both 200

#Cards
class Cards:
    def __init__(self, name, image, card_positions):
        self.name = name
        self.image = image
        self.card_positions = card_positions
    def draw(self,window):
        window.blit(self.image, self.card_positions)
        
#Button Class
class TheButton:
    def __init__(self, text, x, y, activated):
        self.text = text
        self.x = x #position x
        self.y = y #position y
        self.activated = activated #to see whether button is enabled
        self.rect = pygame.Rect((self.x, self.y), (80, 37)) #pygame.Rect object that shows the clicklable area of the button
        self.hover_rect = pygame.Rect((self.x, self.y), (80, 37))

    #draw button 
    def draw(self):
        #hover effect
        mouse_pos = pygame.mouse.get_pos()
        button_hover = self.rect.collidepoint(mouse_pos) #detects mouse click 

        #the buttons
        button_text = font.render(self.text, True, (255, 255, 255)) #(255, 255, 255) ---> text colour
        button_rect = pygame.Rect((self.x, self.y),(127, 37)) #length and width of rectangle
        pygame.draw.rect(window, (144, 238, 144) if button_hover else (29,45,10), button_rect, border_radius = 10)
        #colour and rounded border of rectangle
        window.blit(button_text, (self.x +10, self.y +10))
    
    #mouse click detection
    def gets_clicked(self): #make button clickable
        mouse_position = pygame.mouse.get_pos() #gets current position of the mouse
        if self.rect.collidepoint(mouse_position): #check if mouse inside rect area
            if pygame.mouse.get_pressed()[0]: #check if left mouse button is pressed
                print("Click")
                return True



#LOAD IMAGES + IMAGE SIZES AND POSITIONS:
#e.g. image size (100, 150)


#1. Main Cards
main_cards = {
    "shield_image" : pygame.transform.scale(pygame.image.load("Python image/shield.png").convert_alpha(), (100, 150)),
    "trouble_image" : pygame.transform.scale(pygame.image.load("Python image/trouble.png").convert_alpha(), (100, 150)),
    }

#2. Action Cards 1. shuffle
action_cards = {
    "sick_leave" : pygame.transform.scale(pygame.image.load("Python image/sickleave.png").convert_alpha(), (100, 150)),
    "U_turn" :pygame.transform.scale(pygame.image.load("Python image/uturn.png").convert_alpha(), (100, 150)), 
    "Hacker" : pygame.transform.scale(pygame.image.load("Python image/hacker.png").convert_alpha(), (100, 150)), 
    "TheSpell" : pygame.transform.scale(pygame.image.load("Python image/spell.png").convert_alpha(), (100, 150)), 
    "Shuffle" : pygame.transform.scale(pygame.image.load("Python image/shuffle.png").convert_alpha(), (100, 150)), 
    "Reveal" : pygame.transform.scale(pygame.image.load("Python image/Reveal.png").convert_alpha(), (100, 150)), 
    "BeatIt" : pygame.transform.scale(pygame.image.load("Python image/Beat.png").convert_alpha(), (100, 150)), 
    "BegYou" : pygame.transform.scale(pygame.image.load("Python image/Beg.png").convert_alpha(), (100, 150)), 
    "no_chance" : pygame.transform.scale(pygame.image.load("Python image/nochance.png").convert_alpha(), (100, 150)),
    "mirror" : pygame.transform.scale(pygame.image.load("Python image/Mirror.png").convert_alpha(), (100, 150))
    }

#3. Character Cards
character_cards = {
    "char1_image" : pygame.transform.scale(pygame.image.load("Python image/char1.png").convert_alpha(), (100, 150)), 
    "char2_image" : pygame.transform.scale(pygame.image.load("Python image/char2.png").convert_alpha(), (100, 150)),
    "char3_image" : pygame.transform.scale(pygame.image.load("Python image/char3.png").convert_alpha(), (100, 150)), 
    "char4_image" : pygame.transform.scale(pygame.image.load("Python image/char4.png").convert_alpha(), (100, 150)), 
    "char5_image" : pygame.transform.scale(pygame.image.load("Python image/char5.png").convert_alpha(), (100, 150)), 
    "char6_image" : pygame.transform.scale(pygame.image.load("Python image/char6.png").convert_alpha(), (100, 150)), 
    }



#Game Buttons
button = TheButton("PUSH!", 800,  600, True)
other_buttons = {"Start": TheButton("Start Game", 375, 300, True), 
                 "resume": TheButton("Resume", 375, 300, True), 
                 "Menu": TheButton("Main Menu", 375, 360, True) }


#current game mode
game_status = "menu"


#MAIN GAME LOOP
game_running = True
while game_running: #start the loop - keep going while the game is on
    #event handler
    for event in pygame.event.get():
        #quit game   
        if event.type == pygame.QUIT:
            game_running = False #if player click close button, the loop stops   if event.type == pygame.KEYDOWN:
        
        elif event.type == pygame.KEYDOWN:  #KEYDOWN = whenever keyboard is pressed
            if game_status == "playing" and event.key == pygame.K_SPACE:
                game_status = "paused"
            elif game_status == "paused" and event.key == pygame.K_SPACE:
                game_status = "playing"
                
        #Buttons and pictures on Display based on current games status
        #menu interface
        if game_status == "menu":
            window.blit(menu_img,(0,0)) #add background image for menu
            other_buttons["Start"].draw()
            if other_buttons["Start"].gets_clicked():
                game_status = "playing"
        
        #game running interface
        elif game_status == "playing":
            window.blit(background_img, (0,0)) #add background image for playing game
            window.blit(player, (340, 505))
            button.draw()
            
            #grouped all cards 
            all_cards = {**main_cards, **action_cards, **character_cards} #Merge all cards dictionaries together

            #Display each card on the screen
            current_position = [400, 200] 
            for name, image in all_cards.items(): #items(), lopping dict
                window.blit(image, current_position)
                current_position = [current_position[0] + 2, current_position[1]] #position of the deck of cards, +2 means the gap
        
        
        #paused interface
        elif game_status == "paused":
            window.blit(paused_img, (0,0)) #add background image when pausing
            other_buttons["resume"].draw()
            other_buttons["Menu"].draw()
            if other_buttons["resume"].gets_clicked():
                game_status = "playing"
            elif other_buttons["Menu"].gets_clicked():
                game_status = "menu"


    pygame.display.update()




pygame.quit()

