# Student ID: 5676187
import pygame
import random
import main

from main import ActionCard, Card, GameHandling

pygame.init()

# ============================================================ GAME VARIABLES I =============================================================================================
# the font function for interface#Adjust font size
font_1 = pygame.font.SysFont("None", 25)
font_2 = pygame.font.SysFont("None", 40)
font_3 = pygame.font.SysFont("None", 30)

# setting the size of game window
window = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("You're in trouble")  # sets the title at the top of the window

# Background Images
background_img = pygame.transform.scale(pygame.image.load("Gameplay Backg 2.png"), (1000, 800))
instruction1_img = pygame.transform.scale(pygame.image.load("Instruction 1.png"), (1000, 800))
instruction2_img = pygame.transform.scale(pygame.image.load("Instruction 2.png"), (1000, 800))
ready2play_img = pygame.transform.scale(pygame.image.load("press to start.png"), (1000, 800))
menu_img = pygame.transform.scale(pygame.image.load("menu image.png"), (1000, 800))
paused_img = pygame.transform.scale(pygame.image.load("paused image.jpg"), (1000, 800))
option_img = pygame.transform.scale(pygame.image.load("Background Image.png"), (1000, 800))
humanwins_img = pygame.transform.scale(pygame.image.load("human wins.png"), (1000, 800))
botwins_img = pygame.transform.scale(pygame.image.load("bot wins.png"), (1000, 800))

# Main Gameplay image
BOT1_img = pygame.transform.scale(pygame.image.load("vertical left.png").convert_alpha(), (250,200)) #width and height both 200
BOT2_img = pygame.transform.scale(pygame.image.load("horizontal.png").convert_alpha(), (250,200)) #width and height both 200
BOT3_img = pygame.transform.scale(pygame.image.load("vertical right.png").convert_alpha(), (250,200)) #width and height both 200


# Define colours for drawing purpose
Dark_Green = (0, 100, 0)
Light_Green = (144, 238, 144)
Black = (0, 0, 0)
White = (255, 255, 255)
Dark_Blue = (0, 0, 139)
Light_Blue = (173, 216, 230)
Orange = (255, 165, 0)
Gray = (128, 128, 128)
Red = (255, 0, 0)

# ======================== TEXT TO CLASS MAPPING =========================================
card_text_to_class = {
    # action cards
    "Hacker": main.Hacker,
    "Sick Leave": main.SickLeave,
    "U Turn": main.UTurn,
    "The Spell": main.TheSpell,
    "Shuffle": main.Shuffle,
    "Reveal": main.Reveal,
    "Beat It": main.BeatIt,
    "Beg You": main.BegYou,
    "Mirror": main.Mirror,

    # main card
    "You're in Trouble": main.Trouble,
    "The Shield": main.Shield,

    # character cards
}

# LOAD IMAGES + IMAGE SIZES AND POSITIONS:
# e.g. image size (150, 240)
# 1. Main Cards
main_cards = {
    "The Shield": pygame.transform.scale(pygame.image.load("shield.png").convert_alpha(), (150, 240)),
    "You're in Trouble": pygame.transform.scale(pygame.image.load("trouble.png").convert_alpha(), (150, 240)),
}

# an extra shield that will be displayed next to the screen
extra_shield_img = pygame.transform.scale(pygame.image.load("shield.png").convert_alpha(), (100, 160))
shield_rect = extra_shield_img.get_rect(topleft=(470, 575))

# 2. Action Cards
action_cards = {
    "Sick Leave": pygame.transform.scale(pygame.image.load("sickleave.png").convert_alpha(), (150, 240)),
    "U Turn": pygame.transform.scale(pygame.image.load("uturn.png").convert_alpha(), (150, 240)),
    "Hacker": pygame.transform.scale(pygame.image.load("Hacker.png").convert_alpha(), (150, 240)),
    "The Spell": pygame.transform.scale(pygame.image.load("spell.png").convert_alpha(), (150, 240)),
    "Shuffle": pygame.transform.scale(pygame.image.load("shuffle.png").convert_alpha(), (150, 240)),
    "Reveal": pygame.transform.scale(pygame.image.load("reveal.png").convert_alpha(), (150, 240)),
    "Beat It": pygame.transform.scale(pygame.image.load("Beat.png").convert_alpha(), (150, 240)),
    "Beg You": pygame.transform.scale(pygame.image.load("Beg.png").convert_alpha(), (150, 240)),
    ###"No Chance" : pygame.transform.scale(pygame.image.load("nochance.png").convert_alpha(), (150, 240)),
    "Mirror": pygame.transform.scale(pygame.image.load("Mirror.png").convert_alpha(), (150, 240))
}
# 3. Character Cards
character_cards = {
    "Ice King": pygame.transform.scale(pygame.image.load("char1.png").convert_alpha(), (150, 240)),
    "BMO": pygame.transform.scale(pygame.image.load("char2.png").convert_alpha(), (150, 240)),
    "Finn": pygame.transform.scale(pygame.image.load("char3.png").convert_alpha(), (150, 240)),
    "Jake": pygame.transform.scale(pygame.image.load("char4.png").convert_alpha(), (150, 240)),
    "Bubblegum": pygame.transform.scale(pygame.image.load("char5.png").convert_alpha(), (150, 240)),
    "Lumpy": pygame.transform.scale(pygame.image.load("char6.png").convert_alpha(), (150, 240)),
}

card_list = []


# ======================================================== GAME EFFECTS =============================================================

# 1. Sound effects
button_sf = pygame.mixer.Sound("button click.mp3")
text_sf = pygame.mixer.Sound("text sound (2).mp3")
shield_sf = pygame.mixer.Sound("shield.mp3")


# 2. Fade transition effect between screens
def fade_transition(width, height, colour, next_screen):
    fade = pygame.Surface((width, height))
    fade.fill(colour)
    # alpha means opacity of the window

    # Fade-in effect
    for alpha in range(0, 255):
        fade.set_alpha(alpha)
        draw_window()
        window.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(3)

    # transitioning to next screen [mid-fade] (from chatgpt)
    global game_status
    game_status = next_screen

    # Fade-out effect (solid green to transparent)
    for alpha in range(255, 0, -1):
        fade.set_alpha(alpha)
        draw_window()
        window.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(3)


# ======================================================== CARD CLASS ===========================================================

class Cards:
    def __init__(self, name, image, card_positions):
        self.name = name
        self.image = image
        self.card_positions = card_positions

    def draw(self, window):
        window.blit(self.image, self.card_positions)


# ========================================================= CLICKABLE TEXT CLASS ====================================================

# action = None means that if no action is provided, it defaults to None

class Clickable_text:
    def __init__(self, text, font, ori_colour, hover_colour, x, y, gets_clicked=None):
        self.text = text.split(' ×')[0]
        self.font = font
        self.ori_colour = ori_colour
        self.hover_colour = hover_colour
        self.x = x
        self.y = y
        self.active = True
        self.hovering = False
        self.rect = None
        self.update_rect()


    def update_rect(self):
        display_text = self.get_display_text()
        # renders the text as an image using the font and colour, and gets a transparent rectangle that is the size of the rendered text and places it at the position (self.x, self.y)
        self.rect = self.font.render(display_text, True, self.ori_colour).get_rect(topleft=(self.x, self.y))

    def get_display_text(self):
        if hasattr(self, "count"):
            return f"{self.text} ×{self.count}" if self.count > 0 else self.text
        return self.text

    def position(self):
        if not self.active:
            self.hovering = False
            return

        mouse_position = pygame.mouse.get_pos()  # gets current position of the mouse
        self.hovering = self.rect.collidepoint(mouse_position)  # check if mouse is over the button (rect area)

    # collidepoint(...) check hover/click

    # Text for display
    def draw_text(self, window):
        color = Gray if not self.active else (self.hover_colour if self.hovering else self.ori_colour)
        text_surface = self.font.render(self.get_display_text(), True, color)
        window.blit(text_surface, (self.x, self.y))
        self.update_rect()  # Ensure rect stays in sync

    def gets_clicked(self):  # make text clickable
        if not self.active:
            return False

        mouse_position = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_position) and pygame.mouse.get_pressed()[0]:
            # Get the base card name (without the count)
            card_name = self.text.split(' ×')[0]

            # Get the corresponding card image
            all_cards = {**main_cards, **action_cards, **character_cards}
            if card_name in all_cards:
                global action_pile
                action_pile = all_cards[card_name]
                return True
        return False

    def set_active(self, active):
        self.active = active
        self.update_rect()

    def get_text(self):
        return self.text


# ==================================================== PLAYER CLASS ==========================================================================
class Player:
    def __init__(self, player_txt, action):
        self.player_txt = player_txt
        self.action = action

    # ===================================================== BUTTON CLASS ========================================================================


class TheButton:
    def __init__(self, text, x, y, activated):
        self.text = text
        self.x = x  # position x
        self.y = y  # position y
        self.activated = activated  # to see whether button is enabled
        self.rect = pygame.Rect((self.x, self.y),
                                (80, 37))  # pygame.Rect object that shows the clicklable area of the button
        self.hover_rect = pygame.Rect((self.x, self.y), (80, 37))

    # draw button
    def draw(self):
        # hover effect
        mouse_pos = pygame.mouse.get_pos()
        button_hover = self.rect.collidepoint(mouse_pos)  # detects mouse click

        # the buttons
        button_text = font_3.render(self.text, True, (255, 255, 255))  # (255, 255, 255) ---> text colour
        button_rect = pygame.Rect((self.x, self.y), (127, 37))  # length and width of rectangle
        pygame.draw.rect(window, (144, 238, 144) if button_hover else (29, 45, 10), button_rect, border_radius=10)

        # colour and rounded border of rectangle
        window.blit(button_text, (self.x + 10, self.y + 10))

    # mouse click detection
    def gets_clicked(self):  # make button clickable
        mouse_position = pygame.mouse.get_pos()  # gets current position of the mouse
        if self.rect.collidepoint(mouse_position):  # check if mouse is over the button (rect area)
            if pygame.mouse.get_pressed()[0]:  # check if left mouse button is pressed
                print("Click")
                return True

# ===================================================== COMBO BUTTON CLASS ==================================================================
class ComboButton:
    def __init__(self, text, x, y):
        self.text = text
        self.x = x
        self.y = y
        self.visible = False
        self.activated = False
        self.rect = pygame.Rect((self.x, self.y), (23, 23))
        self.hover_rect = pygame.Rect((self.x, self.y), (23, 23))

    def draw(self):
        if not self.visible:
            return

        mouse_pos = pygame.mouse.get_pos()
        button_hover = self.rect.collidepoint(mouse_pos)

        button_color = Light_Green if (self.activated and button_hover) else (
            Gray if not self.activated else (29, 45, 10))
        text_color = Black if (self.activated and button_hover) else White

        button_rect = pygame.Rect((self.x, self.y), (25, 25))
        pygame.draw.rect(window, button_color, button_rect, border_radius=5)
        button_text = font_1.render(self.text, True, text_color)
        window.blit(button_text, (self.x + 2, self.y + 2))

    def gets_clicked(self):
        if not self.visible or not self.activated:
            return False
        return self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]

# ============================================= GAME VARIABLES II =================================================
# Game Buttons
end_turn_button = TheButton("End turn", 890, 700, True)
play_card_button = TheButton("Play card", 890, 655, True)
Next_button = TheButton("> Next", 900, 700, True)
previous_button = TheButton("Previous <", -5, 700, True)
ready_button = TheButton("Play Game", 430, 450, True)
other_buttons = {"Start": TheButton("Start Game", 430, 380, True),
                 "resume": TheButton("Resume", 430, 300, True),
                 "Menu": TheButton("Main Menu", 430, 360, True)}
option_button = {"2P": TheButton("2 Players", 390, 300, True),
                 "3P": TheButton("3 Players", 390, 360, True),
                 "4P": TheButton("4 Players", 390, 420, True)
                 }

# combo buttons
combo_buttons = {
    "iceking_2": ComboButton("T2", 640, 600),
    "iceking_3": ComboButton("T3", 610, 600),
    "bmo_2": ComboButton("T2", 640, 620),
    "bmo_3": ComboButton("T3", 610, 620),
    "finn_2": ComboButton("T2", 640, 640),
    "finn_3": ComboButton("T3", 610, 640),
    "jake_2": ComboButton("T2", 640, 660),
    "jake_3": ComboButton("T3", 610, 660),
    "bubblegum_2": ComboButton("T2", 640, 680),
    "bubblegum_3": ComboButton("T3", 610, 680),
    "lumpy_2": ComboButton("T2", 640, 700),
    "lumpy_3": ComboButton("T3", 610, 700),
    "full_set": ComboButton("Set", 650, 750)
}

# Action cards text for display
actions_text = [
    Clickable_text("Hacker", font_1, White, Orange, 290, 580),
    Clickable_text("Sick Leave", font_1, White, Orange, 290, 600),
    Clickable_text("U Turn", font_1, White, Orange, 290, 620),
    Clickable_text("The Spell", font_1, White, Orange, 290, 640),
    Clickable_text("Shuffle", font_1, White, Orange, 290, 660),
    Clickable_text("Reveal", font_1, White, Orange, 290, 680),
    Clickable_text("Beat It", font_1, White, Orange, 290, 700),
    Clickable_text("Beg You", font_1, White, Orange, 290, 720),
    ###Clickable_text("No Chance", font_1, White, Orange, 290, 740),
    Clickable_text("Mirror", font_1, White, Orange, 290, 740)
]

# Character Cards text for display
character_text = [
    Clickable_text("Ice King", font_1, White, Orange, 670, 600),
    Clickable_text("BMO", font_1, White, Orange, 670, 620),
    Clickable_text("Finn", font_1, White, Orange, 670, 640),
    Clickable_text("Jake", font_1, White, Orange, 670, 660),
    Clickable_text("Bubblegum", font_1, White, Orange, 670, 680),
    Clickable_text("Lumpy", font_1, White, Orange, 670, 700)
]
all_text = [*actions_text, *character_text]  # Merge all text together



def create_card_text_objects(player):
    # Get card counts from the player
    card_counts = {}
    for card in player.player_cards:
        card_name = card.card_name
        card_counts[card_name] = card_counts.get(card_name, 0) + 1

    # Define all possible card names and their positions
    card_definitions = {
        # Action cards
        "Hacker": (290, 580),
        "Sick Leave": (290, 600),
        "U turn": (290, 620),
        "The Spell": (290, 640),
        "Shuffle": (290, 660),
        "Reveal": (290, 680),
        "Beat It": (290, 700),
        "Beg You": (290, 720),
        "Mirror": (290, 740),

        # Character cards
        "Ice King": (670, 600),
        "BMO": (670, 620),
        "Finn": (670, 640),
        "Jake": (670, 660),
        "Bubblegum": (670, 680),
        "Lumpy": (670, 700)
    }

    # Create Clickable_text objects with counts
    for text in actions_text + character_text:
        base_name = text.text
        count = card_counts.get(base_name, 0)
        text.count = count
        text.set_active(count > 0)
        text.update_rect()

    return actions_text + character_text

def update_combo_button(player):
    # counting how many of each character the player has
    char_count = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0
    }

    for card in player.player_cards:
        if card.card_name == "Ice King":
            char_count[1] += 1
        elif card.card_name == "BMO":
            char_count[2] += 1
        elif card.card_name == "Finn":
            char_count[3] += 1
        elif card.card_name == "Jake":
            char_count[4] += 1
        elif card.card_name == "Bubblegum":
            char_count[5] += 1
        elif card.card_name == "Lumpy":
            char_count[6] += 1

    # reset all buttons at first
    for button in combo_buttons.values():
        button.activated = False
        button.visible = False

    if game.current_player_index == 0 and interactivity_enabled:
        # positioning each button next to it's respective card
        y = {
            1: 600,
            2: 620,
            3: 640,
            4: 660,
            5: 680,
            6: 700
        }

        for char_num in range(1, 7):
            count = char_count[char_num]
            prefix = ["iceking", "bmo", "finn", "jake", "bubblegum", "lumpy"][char_num - 1]

            if count >= 2:
                button = combo_buttons[f"{prefix}_2"]
                button.activated = True
                button.visible = True
                button.y = y[char_num]

                if count >= 3:
                    button = combo_buttons[f"{prefix}_3"]
                    button.activated = True
                    button.visible = True
                    button.y = y[char_num] + 20

            if all(count >= 1 for count in char_count.values()):
                combo_buttons["full_set"].activated = True
                combo_buttons["full_set"].visible = True

def handle_combo_button_click():
    current_player = game.players[game.current_player_index]

    for button_id, button in combo_buttons.items():
        if button.gets_clicked():
            # mapping button prefixes to char numbers
            char_mapping = {
                "iceking": 1,
                "bmo": 2,
                "finn": 3,
                "jake": 4,
                "bubblegum": 5,
                "lumpy": 6
            }

            if button_id.endswith("_2"):
                # extract character prefix; e.g. "finn" from "finn_2"
                char_prefix = button_id.split("_")[0]
                char_num = char_mapping[char_prefix]
                char_name = ["Ice King", "BMO", "Finn", "Jake", "Bubblegum", "Lumpy"][char_num - 1]

                # removing 2 of the played char from player's hand; effect of type 2 combo
                removed = 0
                for card in current_player.player_cards[:]:
                    if card.card_name == char_name and removed < 2:
                        current_player.player_cards.remove(card)
                        current_player.character_counts[char_num] -= 1
                        removed += 1
                        if removed == 2:
                            break
                game.activate_char_combo(current_player, char_num, 2)

            elif button_id.endswith("_3"):
                char_prefix = button_id.split("_")[0]
                char_num = char_mapping[char_prefix]
                char_name = ["Ice King", "BMO", "Finn", "Jake", "Bubblegum", "Lumpy"][char_num - 1]

                # removing 3 of the played char from player's hand; effect of type 3 combo
                removed = 0
                for card in current_player.player_cards[:]:
                    if card.card_name == char_name and removed < 3:
                        current_player.player_cards.remove(card)
                        current_player.character_counts[char_num] -= 1
                        removed += 1
                        if removed == 3:
                            break
                game.activate_char_combo(current_player, char_num, 3)

            elif button_id == "full_set":
                # removing 1 of each character from player's hand; effect of full set combo
                for char_num in range(1, 7):
                    for card in current_player.player_cards[:]:
                        if card.card_name == ["Ice King", "BMO", "Finn", "Jake", "Bubblegum", "Lumpy"][char_num - 1]:
                            current_player.player_cards.remove(card)
                            current_player.character_counts[char_num] -= 1
                            break

                game.activate_full_set_combo(current_player)

text_1 = font_1.render("Press SPACE key to pause", True, Dark_Green)
text_2 = font_2.render("Select players:", True, Black)

# ====================================================== INITIALISE GAME MODE ==========================================================

# current game mode
game = main.GameHandling()
game_status = "menu"
instruction_page = 1
current_player_id = 0  # Player1 = 0 ; Player2 = 1, Player3 = 2
action_pile = None
num_players = 0
youre_in_trouble_trig = 0
previous_shield_value = 0
start_time_trouble_with_shield = 0
start_time_trouble_no_shield = 0
top_3_cards = []
start_time_top_3_cards = 0
start_time_cards = 0
current_time = 0
human_player_index = 0
global user_won
user_won = False
interactivity_enabled = True

def enable_interactivity():
    global interactivity_enabled
    interactivity_enabled = True

def disable_interactivity():
    global interactivity_enabled
    interactivity_enabled = False

def print_trouble_card_with_shield():
    #create an overlay message
    overlay = pygame.Surface ((725, 100))
    overlay.set_alpha(300)
    overlay.fill(Black)
    message = "YOU'RE IN TROUBLE, but you are safe with a shield!"

    msg_surface = font_2.render(message, True, White)
    window.blit(overlay, (140, 320))
    window.blit(msg_surface, (150, 350))

def print_trouble_card_no_shield():
    #create an overlay message
    overlay = pygame.Surface ((800, 100))
    overlay.set_alpha(300)
    overlay.fill(Black)
    message = "YOU'RE IN TROUBLE AND HAVE NO SHIELD. YOU LOSE!"

    msg_surface = font_2.render(message, True, Red)
    window.blit(overlay, (140, 320))
    window.blit(msg_surface, (150, 350))

def display_top_3_cards(top_3_cards):
    all_cards = {**main_cards, **action_cards, **character_cards}

    positions = [(250, 100), (420, 100), (590, 100)] #position of top 3 cards
    overlay = pygame.Surface ((510, 320))
    overlay.set_alpha(200)
    overlay.fill(Black)
    message = "TOP 3 CARDS:"

    msg_surface = font_2.render(message, True, White)
    window.blit(overlay, (240, 50))
    window.blit(msg_surface, (245, 60))

    for i, card in enumerate(top_3_cards):
        card_name = card.card_name

        if card_name in all_cards:
            window.blit(all_cards[card_name], positions[i])

show_top3_cards = False
top3_cards_to_display = []

#In main loop
#if card_name in ["The Spell", "Reveal"]:


# ======================================================= DRAWINGS ON SCREEN ============================================================

# The function below basically groups all the drawings in one place
# makes code more organised, better for reuse purpose, and avoid repetition
# This function will be reused in the main game loop

def draw_window():
    # =============== MENU SCREEN =================
    if game_status == "menu":
        window.blit(menu_img, (0, 0))  # add background image for menu
        other_buttons["Start"].draw()

    # ================ INSTRUCTION SCREEN =================
    elif game_status == "instruction":

        # Instruction page 1
        if instruction_page == 1:
            window.blit(instruction1_img, (0, 0))
            Next_button.draw()

        # Instruction page 2
        elif instruction_page == 2:
            window.blit(instruction2_img, (0, 0))
            Next_button.draw()
            previous_button.draw()

        elif instruction_page == 3:
            window.blit(ready2play_img, (0, 0))
            ready_button.draw()
            previous_button.draw()


    # ================= READY 2 PLAY SCREEN ============
    elif game_status == "Start Game":
        window.blit(ready2play_img, (0, 0))
        ready_button.draw()
        previous_button.draw()

    # ================ OPTION SCREEN =================
    elif game_status == "select player":
        window.blit(option_img, (0, 0))
        window.blit(text_2, (355, 250))

        for button in option_button.values():
            button.draw()

    # ================ GAMEPLAY SCREEN ===============
    elif game_status == "playing":
        window.blit(background_img, (0, 0)) # background image
        window.blit(text_1, (780, 20)) # text_image ---> Press Space Key to Pause

        # player's text
        player_colour = [Orange if i == current_player_id else Black for i in range(num_players)]

        # displaying combo buttons when appropriate
        if interactivity_enabled:
            update_combo_button(game.players[current_player_id])
            for button in combo_buttons.values():
                if button.visible:
                    button.draw()

        # display text with their positions on interface
        if num_players == 2:
            window.blit(BOT2_img, (400, -40))

            human_player_text = font_2.render("You", True, player_colour[0])
            bot1_text = font_2.render("BOT", True, player_colour[1])

            window.blit(bot1_text, (470, 56))
            window.blit(human_player_text, (470, 400))

        if num_players == 3:
            window.blit(BOT1_img, (-50, 260))
            window.blit(BOT3_img, (800, 260))

            human_player_text = font_2.render("You", True, player_colour[0])
            bot1_text = font_2.render("BOT 1", True, player_colour[1])
            bot2_text = font_2.render("BOT 2", True, player_colour[2])

            window.blit(human_player_text, (470, 400))
            window.blit(bot1_text, (40, 350))
            window.blit(bot2_text, (855, 355))

        if num_players == 4:
            window.blit(BOT1_img, (-50, 260))
            window.blit(BOT2_img, (400, -40))
            window.blit(BOT3_img, (800, 260))

            human_player_text = font_2.render("You", True, player_colour[0])
            bot1_text = font_2.render("BOT 1", True, player_colour[1])
            bot2_text = font_2.render("BOT 2", True, player_colour[2])
            bot3_text = font_2.render("BOT 3", True, player_colour[3])

            window.blit(human_player_text, (490, 550))
            window.blit(bot1_text, (40, 350))
            window.blit(bot2_text, (470, 55))
            window.blit(bot3_text, (855, 355))

        # shield image
        num_of_shields = len(game.players[human_player_index].has_shield)
        if num_of_shields != 0:
            window.blit(extra_shield_img, (470, 575))
            shield_message = f"x {num_of_shields}"
            rendered_shield_message = font_2.render(shield_message, True, Orange)
            window.blit(rendered_shield_message, (500, 745))

        # Drawing "End Turn" button
        if interactivity_enabled is True:
            end_turn_button.draw()

        # grouped all cards
        all_cards = {**main_cards, **action_cards, **character_cards}  # Merge all card dictionaries together **
        current_position = [330, 250]  # fixed position for all cards

        for name, image in all_cards.items():  # items(), lopping dict
            window.blit(image, current_position)
            current_position = [current_position[0] + 2, current_position[1]]  # position of the deck of cards, +2 means the gap between cards

        if action_pile is not None: #and current_player_id == human_player_index:
            window.blit(action_pile, (560, 250))

        # Display each card text on screen
        if interactivity_enabled is True:
            for text in create_card_text_objects(game.players[current_player_id]):
                text.position()
                text.draw_text(window)
            for text in actions_text + character_text:
                text.position()
                text.draw_text(window)

            # drawing all combo buttons; they handle their own visibility
            for button in combo_buttons.values():
                button.draw()

        global previous_shield_value, start_time_trouble_with_shield, start_time_trouble_no_shield, youre_in_trouble_trig
        if previous_shield_value == num_of_shields + 1:
            previous_shield_value = num_of_shields
            start_time_trouble_with_shield = current_time
        else:
            previous_shield_value = num_of_shields

        if game.players[human_player_index] in game.losers and youre_in_trouble_trig == 0:
            start_time_trouble_no_shield = current_time
            youre_in_trouble_trig = 1


        if current_time - start_time_trouble_with_shield < 2:
            print_trouble_card_with_shield()
        elif current_time - start_time_trouble_no_shield < 2:
            print_trouble_card_no_shield()

        if current_time - start_time_top_3_cards < 2:
            display_top_3_cards(top_3_cards)

    # ============================== PAUSING INTERFACE ==========================
    elif game_status == "paused":
        window.blit(paused_img, (0, 0))  # add background image when pausing
        other_buttons["resume"].draw()
        other_buttons["Menu"].draw()

    # ============================== WINNER INTERFACE ==========================
    elif game_status == "result":
        if user_won is True:
            window.blit(humanwins_img, (0, 0))
        elif user_won is False:
            window.blit(botwins_img, (0,0))

# =================================================== MAIN GAME LOOP ====================================================================================================
import time

trigger_for_bot_wait = False
played_bots_cards = []
game_running = True

while game_running:  # start the loop - keep going while the game is on
    current_time = pygame.time.get_ticks() / 1000

    for event in pygame.event.get():  # event handler
        if event.type == pygame.QUIT:  # quit game
            game_running = False  # if player click close button, the loop stops   if event.type == pygame.KEYDOWN:

        elif event.type == pygame.KEYDOWN:  # KEYDOWN = whenever keyboard is pressed
            if game_status == "playing" and event.key == pygame.K_SPACE:
                game_status = "paused"
            elif game_status == "paused" and event.key == pygame.K_SPACE:
                game_status = "playing"
        # Buttons and pictures on Display based on current games status

        # ================ MENU SCREEN =================
        if game_status == "menu" and other_buttons["Start"].gets_clicked():
            button_sf.play()
            pygame.time.delay(300)
            game_status = "instruction"


        # ================ INSTRUCTION SCREEN =================

        elif game_status == "instruction":
            # instruction page 1
            if instruction_page == 1 and Next_button.gets_clicked():
                button_sf.play()
                pygame.time.delay(300)  # delay a very small amount of time when pressing button
                instruction_page = 2

            # instruction page 2
            elif instruction_page == 2:
                if Next_button.gets_clicked():
                    button_sf.play()
                    pygame.time.delay(300)
                    instruction_page = 3
                elif previous_button.gets_clicked():
                    button_sf.play()
                    pygame.time.delay(300)
                    instruction_page = 1

            # ready to play (page before actual gameplay)
            elif instruction_page == 3:
                if previous_button.gets_clicked():
                    button_sf.play()
                    pygame.time.delay(300)
                    instruction_page = 2
                elif ready_button.gets_clicked():
                    button_sf.play()
                    pygame.time.delay(300)
                    game_status = "select player"

        # ================= READY 2 PLAY SCREEN ============
        elif game_status == "Start Game":
            button_sf.play()
            pygame.time.delay(300)
            game_status = "select player"

            # ================ OPTION SCREEN =================
        elif game_status == "select player":
            if option_button["2P"].gets_clicked():
                button_sf.play()
                pygame.time.delay(300)
                game = main.GameHandling()
                action_pile = None
                game.players_setup(2, "Player1")
                num_players = 2
                fade_transition(1000, 800, White, "playing")
                game.initialize_game()
                game_status = "playing"

            elif option_button["3P"].gets_clicked():
                button_sf.play()
                pygame.time.delay(300)
                game = main.GameHandling()
                action_pile = None
                game.players_setup(3, "Player1")
                num_players = 3
                fade_transition(1000, 800, White, "playing")
                game.initialize_game()
                game_status = "playing"

            elif option_button["4P"].gets_clicked():
                button_sf.play()
                pygame.time.delay(300)
                game = main.GameHandling()
                action_pile = None
                game.players_setup(4, "Player1")
                num_players = 4
                fade_transition(1000, 800, White, "playing")
                game.initialize_game()
                game_status = "playing"

        # ================ PLAYING SCREEN =================
        elif game_status == "playing":
            current_player = game.players[game.current_player_index]
            current_player_id = game.current_player_index
            all_cards = {**main_cards, **action_cards, **character_cards}  # Merge all card dictionaries together **

            if game.current_player_index == 0 and game.losers.get(current_player) is None:
                enable_interactivity()
                if end_turn_button.gets_clicked():  # option 2 to end turn
                    disable_interactivity()
                    game.end_turn()
                    game.next_player_turn()
                    if game.check_winner() is not None:
                        game_status = "result"

                for text in create_card_text_objects(game.players[current_player_id]):
                    if text.gets_clicked():
                        text_sf.play()
                        card_name = text.text.split(" ×")[0]

                        if card_name in all_cards:
                            action_pile = all_cards[card_name]

                        game.play_selected_card(card_name)
                        if card_name == game.last_played_action_card.card_name == "The Spell"\
                            or card_name == game.last_played_action_card.card_name == "Reveal"\
                            or (len(game.discard_card_pile) > 1
                                and (game.discard_card_pile[-2].card_name == "The Spell"
                                    or game.discard_card_pile[-2].card_name == "Reveal")
                                and card_name == game.last_played_action_card.card_name == "Mirror"):
                            top_3_cards = game.deck.red_black_tree.the_spell_action()
                            if top_3_cards:
                                start_time_top_3_cards = current_time
                        winner = game.check_winner()
                        if winner is not None:
                            game_status = "result"
                            if winner == "Player1":
                                user_won = True
                            else:
                                user_won = False
                        if current_player != game.players[game.current_player_index]:
                            disable_interactivity()

                # handling combo button clicks
                handle_combo_button_click()

            elif current_player in game.losers:
                game.next_player_turn()

            else:
                if trigger_for_bot_wait is False:
                    trigger_for_bot_wait = True
                    game.handle_bot_turn(current_player, played_bots_cards)
                    start_time_cards = current_time
                else:
                    if played_bots_cards:
                        if action_pile != all_cards[played_bots_cards[0].card_name]:
                            if played_bots_cards[0].card_name == "Reveal"\
                                    or (played_bots_cards[0].card_name == "Mirror" and action_pile == all_cards["Reveal"]):
                                top_3_cards = game.deck.red_black_tree.the_spell_action()
                                if top_3_cards:
                                    start_time_top_3_cards = current_time
                            action_pile = all_cards[played_bots_cards[0].card_name]
                            start_time_cards = current_time
                        else:
                            if current_time - start_time_cards > 1.5:
                                played_bots_cards.pop(0)
                    else:
                        if current_time - start_time_cards > 1.5:
                            game.next_player_turn()
                            trigger_for_bot_wait = False
                            winner = game.check_winner()
                            if winner is not None:
                                game_status = "result"
                                if winner == "Player1":
                                    user_won = True
                                else:
                                    user_won = False

        # ================ PAUSING INTERFACE ==================
        elif game_status == "paused":
            if other_buttons["resume"].gets_clicked():
                game_status = "playing"
                button_sf.play()
                pygame.time.delay(300)
            elif other_buttons["Menu"].gets_clicked():
                game_status = "menu"
                button_sf.play()
                pygame.time.delay(300)

    draw_window()
    pygame.display.update()
# pygame.quit()