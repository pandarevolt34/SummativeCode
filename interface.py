#Student ID: 5676187
import pygame

pygame.init() 


#the font function for interface
font = pygame.font.SysFont(None, 30)

#setting the size of game window
window = pygame.display.set_mode((900, 700))
pygame.display.set_caption("YOU'RE in trouble") #sets the title at the top of the window

#Background Images
background_img = pygame.transform.scale(pygame.image.load("Python image/BackG.png"), (900, 700))
instruction1_img = pygame.transform.scale(pygame.image.load("Python image/Instruction 1.png"), (900, 700))
instruction2_img = pygame.transform.scale(pygame.image.load("Python image/Instruction 2.png"), (900, 700))
ready2play_img = pygame.transform.scale(pygame.image.load("Python image/press to start.png"), (900, 700))
menu_img = pygame.transform.scale(pygame.image.load("Python image/menu image.png"), (900, 700))
paused_img = pygame.transform.scale(pygame.image.load("Python image/paused image.jpg"), (900, 700))
result_img = pygame.transform.scale(pygame.image.load("Python image/paused image.jpg"), (900, 700))


#Sound effects 
button_sf = pygame.mixer.Sound("Python image/button click.mp3")

#player image   
player = pygame.transform.scale(pygame.image.load("Python image/Player.jpg").convert_alpha(), (250,200)) #width and height both 200

#Define colours for drawing purpose
Dark_Green	= (0, 100, 0)
Light_Green = (144, 238, 144)
Black = (0, 0, 0)
White = (255, 255, 255)
Dark_Blue = (0, 0, 139)
Light_Blue = (173, 216, 230)
Orange = (255, 165, 0)


#LOAD IMAGES + IMAGE SIZES AND POSITIONS:
#e.g. image size (150, 240)
#1. Main Cards
main_cards = {
    "shield_image" : pygame.transform.scale(pygame.image.load("Python image/shield.png").convert_alpha(), (150, 240)),
    "trouble_image" : pygame.transform.scale(pygame.image.load("Python image/trouble.png").convert_alpha(), (150, 240)),
    }

#2. Action Cards 
action_cards = {
    "sick_leave" : pygame.transform.scale(pygame.image.load("Python image/sickleave.png").convert_alpha(), (150, 240)),
    "U_turn" :pygame.transform.scale(pygame.image.load("Python image/uturn.png").convert_alpha(), (150, 240)), 
    "Hacker" : pygame.transform.scale(pygame.image.load("Python image/hacker.png").convert_alpha(), (150, 240)), 
    "TheSpell" : pygame.transform.scale(pygame.image.load("Python image/spell.png").convert_alpha(), (150, 240)), 
    "Shuffle" : pygame.transform.scale(pygame.image.load("Python image/shuffle.png").convert_alpha(), (150, 240)), 
    "Reveal" : pygame.transform.scale(pygame.image.load("Python image/Reveal.png").convert_alpha(), (150, 240)), 
    "BeatIt" : pygame.transform.scale(pygame.image.load("Python image/Beat.png").convert_alpha(), (150, 240)), 
    "BegYou" : pygame.transform.scale(pygame.image.load("Python image/Beg.png").convert_alpha(), (150, 240)), 
    "no_chance" : pygame.transform.scale(pygame.image.load("Python image/nochance.png").convert_alpha(), (150, 240)),
    "mirror" : pygame.transform.scale(pygame.image.load("Python image/Mirror.png").convert_alpha(), (150, 240))
    }

#3. Character Cards
character_cards = {
    "char1_image" : pygame.transform.scale(pygame.image.load("Python image/char1.png").convert_alpha(), (150, 240)), 
    "char2_image" : pygame.transform.scale(pygame.image.load("Python image/char2.png").convert_alpha(), (150, 240)),
    "char3_image" : pygame.transform.scale(pygame.image.load("Python image/char3.png").convert_alpha(), (150, 240)), 
    "char4_image" : pygame.transform.scale(pygame.image.load("Python image/char4.png").convert_alpha(), (150, 240)), 
    "char5_image" : pygame.transform.scale(pygame.image.load("Python image/char5.png").convert_alpha(), (150, 240)), 
    "char6_image" : pygame.transform.scale(pygame.image.load("Python image/char6.png").convert_alpha(), (150, 240)), 
    }

#Fade transition between screens
def fade_transition(width, height,colour, next_screen):
    fade = pygame.Surface((width, height))
    fade.fill(colour)
    #alpha means opacity of the window

    #Fade-in effect
    for alpha in range (0,255): 
        fade.set_alpha(alpha)
        draw_window()
        window.blit(fade, (0,0))
        pygame.display.update()
        pygame.time.delay(3)
    
    #transitioning to next screen [mid-fade] (from chatgpt)
    global game_status 
    game_status = next_screen

    #Fade-out effect (solid green to transparent)
    for alpha in range(255, 0, -1):
        fade.set_alpha(alpha)
        draw_window()
        window.blit(fade, (0,0))
        pygame.display.update()
        pygame.time.delay(3)



#The function below basically groups all the drawings in one place 
#makes code more organised, better for reuse purpose, and avoid repetition
#This function will be reused in the main game loop

def draw_window():
    #=============== MENU SCREEN =================
    if game_status == "menu":
        window.blit(menu_img,(0,0)) #add background image for menu
        other_buttons["Start"].draw()

    #================ INSTRUCTION SCREEN =================
    elif game_status == "instruction":

        #Instruction page 1
        if instruction_page == 1:
            window.blit(instruction1_img, (0,0))
            Next_button.draw()
        
        #Instruction page 2
        elif instruction_page == 2:
                window.blit(instruction2_img, (0,0))
                Next_button.draw()
          
        #ready to play (screen before main gameplay)
        elif instruction_page == 3:
                window.blit(ready2play_img, (0,0))
                ready_button.draw()
  
    #=============== MAIN GAMEPLAY SCREEN =================
    elif game_status == "playing":
        window.blit(background_img, (0,0)) #add background image 
        window.blit(player, (340, 505)) #add player's image
        button1.draw() 
            
        #grouped all cards 
        all_cards = {**main_cards, **action_cards, **character_cards} #Merge all card dictionaries together **

        #Display each card on the screen
        current_position = [375, 145] #fixed position for all cards
        for name, image in all_cards.items(): #items(), lopping dict
            window.blit(image, current_position)
            current_position = [current_position[0] + 2, current_position[1]] #position of the deck of cards, +2 means the gap between cards
        
    #PAUSING INTERFACE 
    elif game_status == "paused":
            window.blit(paused_img, (0,0)) #add background image when pausing
            other_buttons["resume"].draw()
            other_buttons["Menu"].draw()

    #WINNER INTERFACE
    elif game_status == "result":
            window.blit(result_img, (0,0))


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

#Game Buttons
button1 = TheButton("PUSH!", 800,  600, True)
Next_button = TheButton("NEXT", 800, 600, True)
ready_button = TheButton("Play Game", 380, 400, True)
other_buttons = {"Start": TheButton("Start Game", 375, 300, True), 
                 "resume": TheButton("Resume", 375, 300, True), 
                 "Menu": TheButton("Main Menu", 375, 360, True) }

#current game mode (initial)
game_status = "menu"
instruction_page = 1


#MAIN GAME LOOP
game_running = True
while game_running: #start the loop - keep going while the game is on
    for event in pygame.event.get():#event handler 
        
        if event.type == pygame.QUIT:#quit game 
            game_running = False #if player click close button, the loop stops   if event.type == pygame.KEYDOWN:
        
        elif event.type == pygame.KEYDOWN:  #KEYDOWN = whenever keyboard is pressed
            if game_status == "playing" and event.key == pygame.K_SPACE:
                game_status = "paused"
            elif game_status == "paused" and event.key == pygame.K_SPACE:
                game_status = "playing"
                
        #Buttons and pictures on Display based on current games status
    #=============== MENU SCREEN =================
        if game_status == "menu" and other_buttons["Start"].gets_clicked():
                button_sf.play()
                pygame.time.delay(300)
                game_status = "instruction"

    #================ INSTRUCTION SCREEN =================
       
        elif game_status == "instruction":
            #instruction page 1
            if instruction_page == 1 and Next_button.gets_clicked():  
                button_sf.play()
                pygame.time.delay(300) #delay a very small amount of time when pressing button
                instruction_page = 2
            
            #instruction page 2
            elif instruction_page == 2 and Next_button.gets_clicked():
                button_sf.play()
                pygame.time.delay(300)
                instruction_page = 3
            
            #ready to play (pahe before actual gameplay)
            elif instruction_page == 3 and ready_button.gets_clicked():
                    button_sf.play()
                    pygame.time.delay(300)
                    fade_transition(900, 700, White, "playing")
                    game_status = "playing"
                
                    
        
    #=============== MAIN GAMEPLAY SCREEN =================
        elif game_status == "playing":
            
            #grouped all cards 
            all_cards = {**main_cards, **action_cards, **character_cards} #Merge all card dictionaries together **

            #Display each card on the screen
            current_position = [375, 145] #fixed position for all cards
            for name, image in all_cards.items(): #items(), lopping dict
                window.blit(image, current_position)
                current_position = [current_position[0] + 2, current_position[1]] #position of the deck of cards, +2 means the gap between cards
        
    #================ PAUSING INTERFACE ==================
        elif game_status == "paused":
            if other_buttons["resume"].gets_clicked():
                game_status = "playing"
                button_sf.play()
                pygame.time.delay(300)
            elif other_buttons["Menu"].gets_clicked():
                game_status = "menu"
                button_sf.play()
                pygame.time.delay(300)
    #=============== WINNER INTERFACE ====================
        elif game_status == "result":
            window.blit(result_img, (0,0))


    draw_window()
    pygame.display.update()



pygame.quit()



