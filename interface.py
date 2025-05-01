#Student ID: 5676187
import pygame

pygame.init() 

#============================================================ GAME VARIABLES I =============================================================================================
#the font function for interface#Adjust font size
font_1 = pygame.font.SysFont("None", 25)
font_2 = pygame.font.SysFont("None", 40)
font_3 = pygame.font.SysFont("None", 30)

#setting the size of game window
window = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("YOU'RE in trouble") #sets the title at the top of the window

#Background Images
background_img = pygame.transform.scale(pygame.image.load("c:/Users/Braden Chin Jia Shen/OneDrive/Documents/Warwick/Compsci/Crash Course/Python image/Gameplay Backg 2.png"), (1000, 800))
instruction1_img = pygame.transform.scale(pygame.image.load("c:/Users/Braden Chin Jia Shen/OneDrive/Documents/Warwick/Compsci/Crash Course/Python image/Instruction 1.png"), (1000, 800))
instruction2_img = pygame.transform.scale(pygame.image.load("c:/Users/Braden Chin Jia Shen/OneDrive/Documents/Warwick/Compsci/Crash Course/Python image/Instruction 2.png"), (1000, 800))
ready2play_img = pygame.transform.scale(pygame.image.load("c:/Users/Braden Chin Jia Shen/OneDrive/Documents/Warwick/Compsci/Crash Course/Python image/press to start.png"), (1000, 800))
menu_img = pygame.transform.scale(pygame.image.load("c:/Users/Braden Chin Jia Shen/OneDrive/Documents/Warwick/Compsci/Crash Course/Python image/menu image.png"), (1000, 800))
paused_img = pygame.transform.scale(pygame.image.load("c:/Users/Braden Chin Jia Shen/OneDrive/Documents/Warwick/Compsci/Crash Course/Python image/paused image.jpg"), (1000, 800))

#Main Gameplay image   
player1 = pygame.transform.scale(pygame.image.load("c:/Users/Braden Chin Jia Shen/OneDrive/Documents/Warwick/Compsci/Crash Course/Python image/PLAYER 1.png").convert_alpha(), (250,200)) #width and height both 200
player2 = pygame.transform.scale(pygame.image.load("c:/Users/Braden Chin Jia Shen/OneDrive/Documents/Warwick/Compsci/Crash Course/Python image/PLAYER 2.png").convert_alpha(), (250,200)) #width and height both 200
player3 = pygame.transform.scale(pygame.image.load("c:/Users/Braden Chin Jia Shen/OneDrive/Documents/Warwick/Compsci/Crash Course/Python image/PLAYER 3.png").convert_alpha(), (250,200)) #width and height both 200

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
    "shield_image" : pygame.transform.scale(pygame.image.load("c:/Users/Braden Chin Jia Shen/OneDrive/Documents/Warwick/Compsci/Crash Course/Python image/shield.png").convert_alpha(), (150, 240)),
    "trouble_image" : pygame.transform.scale(pygame.image.load("c:/Users/Braden Chin Jia Shen/OneDrive/Documents/Warwick/Compsci/Crash Course/Python image/trouble.png").convert_alpha(), (150, 240)),
    }

#an extra shield that will be displayed next to the screen
extra_shield_img = pygame.transform.scale(pygame.image.load("c:/Users/Braden Chin Jia Shen/OneDrive/Documents/Warwick/Compsci/Crash Course/Python image/shield.png").convert_alpha(), (100, 160))
shield_rect = extra_shield_img.get_rect(topleft=(470, 575))

#2. Action Cards 
action_cards = {
    "Sick Leave" : pygame.transform.scale(pygame.image.load("c:/Users/Braden Chin Jia Shen/OneDrive/Documents/Warwick/Compsci/Crash Course/Python image/sickleave.png").convert_alpha(), (150, 240)),
    "U turn" :pygame.transform.scale(pygame.image.load("c:/Users/Braden Chin Jia Shen/OneDrive/Documents/Warwick/Compsci/Crash Course/Python image/uturn.png").convert_alpha(), (150, 240)), 
    "Hacker" : pygame.transform.scale(pygame.image.load("c:/Users/Braden Chin Jia Shen/OneDrive/Documents/Warwick/Compsci/Crash Course/Python image/hacker.png").convert_alpha(), (150, 240)), 
    "The Spell" : pygame.transform.scale(pygame.image.load("c:/Users/Braden Chin Jia Shen/OneDrive/Documents/Warwick/Compsci/Crash Course/Python image/spell.png").convert_alpha(), (150, 240)), 
    "Shuffle" : pygame.transform.scale(pygame.image.load("c:/Users/Braden Chin Jia Shen/OneDrive/Documents/Warwick/Compsci/Crash Course/Python image/shuffle.png").convert_alpha(), (150, 240)), 
    "Reveal" : pygame.transform.scale(pygame.image.load("c:/Users/Braden Chin Jia Shen/OneDrive/Documents/Warwick/Compsci/Crash Course/Python image/reveal.png").convert_alpha(), (150, 240)), 
    "Beat" : pygame.transform.scale(pygame.image.load("c:/Users/Braden Chin Jia Shen/OneDrive/Documents/Warwick/Compsci/Crash Course/Python image/Beat.png").convert_alpha(), (150, 240)), 
    "Beg You" : pygame.transform.scale(pygame.image.load("c:/Users/Braden Chin Jia Shen/OneDrive/Documents/Warwick/Compsci/Crash Course/Python image/Beg.png").convert_alpha(), (150, 240)), 
    "No Chance" : pygame.transform.scale(pygame.image.load("c:/Users/Braden Chin Jia Shen/OneDrive/Documents/Warwick/Compsci/Crash Course/Python image/nochance.png").convert_alpha(), (150, 240)),
    "Mirror" : pygame.transform.scale(pygame.image.load("c:/Users/Braden Chin Jia Shen/OneDrive/Documents/Warwick/Compsci/Crash Course/Python image/Mirror.png").convert_alpha(), (150, 240))
    }

#3. Character Cards
character_cards = {
    "Ice King" : pygame.transform.scale(pygame.image.load("c:/Users/Braden Chin Jia Shen/OneDrive/Documents/Warwick/Compsci/Crash Course/Python image/char1.png").convert_alpha(), (150, 240)), 
    "Bimo" : pygame.transform.scale(pygame.image.load("c:/Users/Braden Chin Jia Shen/OneDrive/Documents/Warwick/Compsci/Crash Course/Python image/char2.png").convert_alpha(), (150, 240)),
    "Finn" : pygame.transform.scale(pygame.image.load("c:/Users/Braden Chin Jia Shen/OneDrive/Documents/Warwick/Compsci/Crash Course/Python image/char3.png").convert_alpha(), (150, 240)), 
    "Jack" : pygame.transform.scale(pygame.image.load("c:/Users/Braden Chin Jia Shen/OneDrive/Documents/Warwick/Compsci/Crash Course/Python image/char4.png").convert_alpha(), (150, 240)), 
    "Bubblegum" : pygame.transform.scale(pygame.image.load("c:/Users/Braden Chin Jia Shen/OneDrive/Documents/Warwick/Compsci/Crash Course/Python image/char5.png").convert_alpha(), (150, 240)), 
    "Lumpy" : pygame.transform.scale(pygame.image.load("c:/Users/Braden Chin Jia Shen/OneDrive/Documents/Warwick/Compsci/Crash Course/Python image/char6.png").convert_alpha(), (150, 240)), 
    }

card_list = []

action_pile = None 

#======================================================== GAME EFFECTS =============================================================

#1. Sound effects 
button_sf = pygame.mixer.Sound("C:/Users/Braden Chin Jia Shen/OneDrive/Documents/Warwick/Compsci/Crash Course/Python image/button click.mp3")
text_sf = pygame.mixer.Sound("C:/Users/Braden Chin Jia Shen/OneDrive/Documents/Warwick/Compsci/Crash Course/Python image/text sound (2).mp3")

#2. Fade transition effect between screens
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



#======================================================== CARD CLASS ===========================================================

class Cards:
    def __init__(self, name, image, card_positions):
        self.name = name
        self.image = image
        self.card_positions = card_positions

    def draw(self,window):
        window.blit(self.image, self.card_positions)

#========================================================= CLICKABLE TEXT CLASS ====================================================

#action = None means that if no action is provided, it defaults to None

class Clickable_text:
    def __init__(self, text, font, ori_colour, hover_colour, x, y, gets_clicked = None):
        self.text = text
        self.font = font
        self.ori_colour = ori_colour
        self.hover_colour = hover_colour
        self.x = x
        self.y = y
        self.hovering = False
        self.rect = self.font.render(self.text, True, self.ori_colour).get_rect(topleft=(self.x, self.y))
        #renders the text as an image using the font and colour, and gets a transparent rectangle that is the size of the rendered text and places it at the position (self.x, self.y)
    
    def position(self):
        mouse_position = pygame.mouse.get_pos() #gets current position of the mouse
        self.hovering= self.rect.collidepoint(mouse_position) #check if mouse is over the button (rect area)
     #collidepoint(...) check hover/click

    #Text for display
    def draw_text(self, window):
        text_colour = self.hover_colour if self.hovering else self.ori_colour 
        text_surface = self.font.render(self.text, True, text_colour) #self.font.render turns text into an image
        rect = text_surface.get_rect(topleft=(self.x, self.y)) #get_rect() creates a transparent rectangle which is the same size as the text
        window.blit(text_surface, rect)
        #topleft = .. sets the clickable area to match the text's position.

    def gets_clicked(self): #make text clickable
        if self.hovering and pygame.mouse.get_pressed()[0]: #check if left mouse button is pressed
            global action_pile #read the variable further up
            global all_cards
            print(action_pile)
            print(all_cards.get(self.text))
            print(self.text)
            action_pile = all_cards.pop(self.text, action_pile) 
            return True
            
    def get_text(self):
        return self.text
    
#==================================================== PLAYER CLASS ==========================================================================
class Player:
    def __init__(self, player_txt, action):
        self.player_txt = player_txt
        self.action = action 

#===================================================== BUTTON CLASS ========================================================================
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
        button_text = font_3.render(self.text, True, (255, 255, 255)) #(255, 255, 255) ---> text colour
        button_rect = pygame.Rect((self.x, self.y),(127, 37)) #length and width of rectangle
        pygame.draw.rect(window, (144, 238, 144) if button_hover else (29,45,10), button_rect, border_radius = 10)

        #colour and rounded border of rectangle
        window.blit(button_text, (self.x +10, self.y +10))

        
    #mouse click detection
    def gets_clicked(self): #make button clickable
        mouse_position = pygame.mouse.get_pos() #gets current position of the mouse
        if self.rect.collidepoint(mouse_position): #check if mouse is over the button (rect area)
            if pygame.mouse.get_pressed()[0]: #check if left mouse button is pressed
                print("Click")
                return True


#============================================= GAME VARIABLES II =================================================
#Game Buttons
gameplay_button = TheButton("End turn", 900,  700, True)
Next_button = TheButton("NEXT", 900, 700, True)
previous_button = TheButton("Previous <", -5, 700, True )
ready_button = TheButton("Play Game", 430, 450, True)
other_buttons = {"Start": TheButton("Start Game", 430, 380, True), 
                 "resume": TheButton("Resume", 430, 300, True), 
                 "Menu": TheButton("Main Menu", 430, 360, True) }
option_button = TheButton("Options", 900, 700, True)

#Action cards text for display
actions_text = [
        Clickable_text("Hacker", font_1, White, Orange, 290, 580),
        Clickable_text("Sick Leave", font_1, White, Orange, 290, 600),
        Clickable_text("U turn", font_1, White, Orange, 290, 620),
        Clickable_text("The Spell", font_1, White, Orange, 290, 640),
        Clickable_text("Shuffle", font_1, White, Orange, 290, 660),
        Clickable_text("Reveal", font_1, White, Orange, 290, 680),
        Clickable_text("Beat", font_1, White, Orange, 290, 700),
        Clickable_text("Beg You", font_1, White, Orange, 290, 720),
        Clickable_text("No Chance", font_1, White, Orange, 290, 740),
        Clickable_text("Mirror", font_1, White, Orange, 290, 760)
        ]

#Character Cards text for display
character_text = [
        Clickable_text("Ice King", font_1, White, Orange, 670, 600),
        Clickable_text("Bimo", font_1, White,Orange, 670, 620),
        Clickable_text("Finn", font_1, White, Orange, 670, 640),
        Clickable_text("Jack", font_1, White, Orange, 670, 660),
        Clickable_text("Bubblegum", font_1, White, Orange, 670, 680),
        Clickable_text("Lumpy", font_1, White, Orange, 670, 700)
        ]
all_text = [*actions_text, *character_text] #Merge all text together



#====================================================== INTIALISE GAME MODE ==========================================================

#current game mode 
game_status = "menu"
instruction_page = 1
current_player = 0 #Player1 = 0 ; Player2 = 1, Player3 = 2

#======================================================= DRAWINGS ON SCREEN ============================================================

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
            previous_button.draw()
          
        #ready to play (screen before main gameplay) 
        elif instruction_page == 3:
            window.blit(ready2play_img, (0,0))
            ready_button.draw()
            previous_button.draw()

    #=============== MAIN GAMEPLAY INTERFACE =================
    elif game_status == "playing":

        #background image 
        window.blit(background_img, (0,0)) 



        #player's image
        window.blit(player1, (-50, 260))
        window.blit(player2, (400, -40))
        window.blit(player3, (800, 260))


        #shield image
        window.blit(extra_shield_img, (470, 575) )


        #player's text
        player_colour = [Dark_Green if i == current_player else Black for i in range(3)]
        #render text into inmage for blitting later
        player1_text = font_2.render("Player 1", Black, player_colour[0]) 
        player2_text = font_2.render("Player 2", Black, player_colour[1])
        player3_text = font_2.render("Player 3", Black, player_colour[2])
        #display text with their positions on interface
        window.blit(player1_text, (40, 350))
        window.blit(player2_text, (470, 56))
        window.blit(player3_text, (855, 355))
        

        #Drawing "End Turn" button 
        gameplay_button.draw()
        

        #grouped all cards 
        all_cards = {**main_cards, **action_cards, **character_cards} #Merge all card dictionaries together **


        #Display each card on the screen
        current_position = [330, 250] #fixed position for all cards
        for name, image in all_cards.items(): #items(), lopping dict
            window.blit(image, current_position)
            current_position = [current_position[0] + 2, current_position[1]] #position of the deck of cards, +2 means the gap between cards
        
        if action_pile is not None:
            window.blit(action_pile, (560, 250))
    
        #Display each card text on screen
        for text in actions_text + character_text:
            text.position()
            text.draw_text(window)



    #============================== PAUSING INTERFACE ==========================
    elif game_status == "paused":
            window.blit(paused_img, (0,0)) #add background image when pausing
            other_buttons["resume"].draw()
            other_buttons["Menu"].draw()


    #============================== WINNER INTERFACE ==========================
    elif game_status == "result":
            window.blit(result_img, (0,0))

#===================================== DUMMY FUNCTIONS================================================

def draw_cards():
    print("Drawing card")

def end_turn():
    print("Ending turn")
    ''
    ''

def use_card():
    print("Using ")

def shuffle_deck():
    print("Shuffling cards")

def card_to_box():
    print("Haha")


#=================================================== MAIN GAME LOOP ====================================================================================================


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
            elif instruction_page == 2: 
                if Next_button.gets_clicked():
                    button_sf.play()
                    pygame.time.delay(300)
                    instruction_page = 3
                elif previous_button.gets_clicked():
                    button_sf.play()
                    pygame.time.delay(300)
                    instruction_page = 1
            
            #ready to play (page before actual gameplay) 
            elif instruction_page == 3:
                if previous_button.gets_clicked():
                    button_sf.play()
                    pygame.time.delay(300)
                    instruction_page = 2
                elif ready_button.gets_clicked():
                    button_sf.play()
                    pygame.time.delay(300)
                    fade_transition(1000, 800, White, "playing")
                    game_status = "playing"
                    
        
    #=============== MAIN GAMEPLAY SCREEN =================
        elif game_status == "playing":
            
            #Switching to next player
            if gameplay_button.gets_clicked():
                current_player += 1 #increment 1
                if current_player > 2:
                    current_player = 0 #loops back to fist player so player1 --> player 2 ---> player 3 ----> player 1

            #grouped all cards 
            all_cards = {**main_cards, **action_cards, **character_cards} #Merge all card dictionaries together **

            #Display each card on the screen
            current_position = [700,700] #fixed position for all cards
            for name, image in all_cards.items(): #items(), lopping dict
                window.blit(image, current_position)
                current_position = [current_position[0] + 2, current_position[1]] #position of the deck of cards, +2 means the gap between cards

            for text in all_text:
                if text.gets_clicked():
                    text_sf.play()

            if gameplay_button.gets_clicked():
                print("Click")

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                if shield_rect.collidepoint(mouse_position):
                    print("Shield used!")
            

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














