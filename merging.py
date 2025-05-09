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

# Main Gameplay image
player_ver_left = pygame.transform.scale(pygame.image.load("vertical left.png").convert_alpha(),
                                         (250, 200))  # width and height both 200
player_hori_mid = pygame.transform.scale(pygame.image.load("horizontal.png").convert_alpha(),
                                         (250, 200))  # width and height both 200
player_ver_right = pygame.transform.scale(pygame.image.load("vertical right.png").convert_alpha(),
                                          (250, 200))  # width and height both 200

# Define colours for drawing purpose
Dark_Green = (0, 100, 0)
Light_Green = (144, 238, 144)
Black = (0, 0, 0)
White = (255, 255, 255)
Dark_Blue = (0, 0, 139)
Light_Blue = (173, 216, 230)
Orange = (255, 165, 0)
Gray = (128, 128, 128)


# =================================================== FROM MAIN.PY ============================================================================
class Trouble(Card):
    """Class representing the "You're in Trouble" card which eliminates a player, given they don't have the shield"""

    def __init__(self, index=-1):
        super().__init__("You're in Trouble", "Trouble", " ", index)
        self.image = main_cards["trouble"]


class Shield(Card):
    """Class representing "The Shield" card which protects the player from the trouble card"""

    def __init__(self, index=-1):
        super().__init__("The Shield", "Shield", " ", index)
        self.image = main_cards["shield"]


class SickLeave(ActionCard):
    def __init__(self, index=-1):
        # inheriting attributes from parent class Card
        super().__init__("Sick Leave", "Action", "End your turn without drawing a card", index)
        self.image = action_cards["Sick Leave"]

    def perform_action(self, game, current_player):
        print(f"{current_player.player_name} used Sick Leave")
        return True


class UTurn(ActionCard):
    def __init__(self, index=-1):
        # inheriting attributes from parent class Card
        super().__init__("U Turn", "Action", "Reverse the direction of the game", index)
        self.image = action_cards["U Turn"]

    def perform_action(self, game, current_player):
        game.turn_direction *= -1  # turns the game direction to be -1 (anticlockwise)
        print(f"{current_player.player_name} used U Turn - Direction reversed.")
        return True


class Hacker(ActionCard):
    def __init__(self, index=-1):
        # inheriting attributes from parent class Card
        super().__init__("Hacker", "Action", "Take a card from a random position in the deck", index)
        self.image = action_cards["Hacker"]

    def perform_action(self, game, current_player):
        print(f"{current_player.player_name} used Hacker!")
        card = game.deck.red_black_tree.hacker_action()  # picks a random card from the deck
        current_player.player_cards.append(card)  # appends the random card to the player's cards
        return True


class TheSpell(ActionCard):
    def __init__(self, index=-1):
        # inheriting attributes from parent class Card
        super().__init__("The Spell", "Action", "Peek at the top 3 cards in the deck", index)
        self.image = action_cards["The Spell"]

    def perform_action(self, game, current_player):  # NEEDS FIXING TO CONSIDER BOT PLAYERS
        print(f"{current_player.player_name} used TheSpell")
        top_cards = game.deck.red_black_tree.the_spell_action()
        if top_cards is None:
            return False
        if game.current_player_index == 0:
            print("Top 3 cards:")
            for i in top_cards:
                print(i.card_name)
        return True


class Shuffle(ActionCard):
    def __init__(self, index=-1):
        # inheriting attributes from parent class Card
        super().__init__("Shuffle", "Action", "Shuffle the deck", index)
        self.image = action_cards["Shuffle"]

    def perform_action(self, game, current_player):
        print(f"{current_player.player_name} used Shuffle - The deck is shuffled")
        game.deck.red_black_tree.shuffle_action()
        return True


class Reveal(ActionCard):
    def __init__(self, index=-1):
        # inheriting attributes from parent class Card
        super().__init__("Reveal", "Action", "Reveal the top 3 cards to all players", index)
        self.image = action_cards["Reveal"]
        ### NOTE: THIS SHOULD APPEAR TO ALL PLAYERS; NOT LIKE THE SPELL

    def perform_action(self, game, current_player):  # FIX THIS LIKE THE SPELL
        print(f"{current_player.player_name} used Reveal!")
        top_cards = game.deck.red_black_tree.the_spell_action()
        if top_cards is None:
            return False
        print("Top 3 cards:")
        for i in top_cards:
            print(i.card_name)
        return True


class BeatIt(ActionCard):
    def __init__(self, index=-1):
        # inheriting attributes from parent class Card
        super().__init__("Beat It", "Action",
                         "Avoid drawing a card, and force the next player to play two consecutive turns", index)
        self.image = action_cards["Beat It"]

    def perform_action(self, game, current_player):
        target_player = game.players[(game.current_player_index + game.turn_direction) % len(game.players)]
        print(f"{target_player.player_name} has taken an extra card from the deck")
        game.end_turn(target_player)
        return True


class BegYou(ActionCard):
    def __init__(self, index=-1):
        # inheriting attributes from parent class Card
        super().__init__("Beg You", "Action", "A random player will give you a random card of theirs", index)
        self.image = action_cards["Beg You"]

    def perform_action(self, game, current_player):
        print(f"{current_player.player_name} used Beg You!")
        available_players = []  # picks a random player to perform the card's action on
        for i in game.players:
            if game.losers.get(i) is None and i != current_player:
                available_players.append(i)
        target_player = random.choice(available_players)
        if target_player.player_cards:
            card = random.choice(target_player.player_cards)  # taking a random card from the player's cards
            target_player.player_cards.remove(card)  # removes that card from the target player's cards
            current_player.player_cards.append(card)  # adds that card to the player who played the action card
        else:
            print(f"{target_player.player_name} has no cards therefore Beg You affect is cancelled!")
        return True


class Mirror(ActionCard):
    def __init__(self, index=-1):
        # inheriting attributes from parent class Card
        super().__init__("Mirror", "Action", "Copy the last played action card", index)
        self.image = action_cards["Mirror"]

    def perform_action(self, game, current_player):
        if game.last_played_action_card.card_name == "null":  # error handling
            print("No action card to mirror.")
            return False
        elif game.last_played_action_card.card_name == "Mirror":
            print("Can't mirror a mirror.")
            return False
        last_card = game.last_played_action_card
        print(f"Mirroring {last_card.card_name}")

        try:
            # create instances of the same card type
            new_card = type(last_card)(index=-1)  # using -1 as a temporary index
            result = new_card.perform_action(game, current_player)
            if result:
                return True
            return False
        except Exception as e:
            print(f"Mirror failed: {str(e)}")
            return False


# ======================== TEXT TO CLASS MAPPING =========================================
card_text_to_class = {
    # action cards
    "Hacker": Hacker,
    "Sick Leave": SickLeave,
    "U Turn": UTurn,
    "The Spell": TheSpell,
    "Shuffle": Shuffle,
    "Reveal": Reveal,
    "Beat It": BeatIt,
    "Beg You": BegYou,
    "Mirror": Mirror,

    # main card
    "trouble": Trouble,
    "shield": Shield,

    # character cards
}

# LOAD IMAGES + IMAGE SIZES AND POSITIONS:
# e.g. image size (150, 240)
# 1. Main Cards
main_cards = {
    "shield": pygame.transform.scale(pygame.image.load("shield.png").convert_alpha(), (150, 240)),
    "trouble": pygame.transform.scale(pygame.image.load("trouble.png").convert_alpha(), (150, 240)),
}

# an extra shield that will be displayed next to the screen
extra_shield_img = pygame.transform.scale(pygame.image.load("shield.png").convert_alpha(), (100, 160))
shield_rect = extra_shield_img.get_rect(topleft=(470, 575))

# 2. Action Cards
action_cards = {
    "Sick Leave": pygame.transform.scale(pygame.image.load("sickleave.png").convert_alpha(), (150, 240)),
    "U turn": pygame.transform.scale(pygame.image.load("uturn.png").convert_alpha(), (150, 240)),
    "Hacker": pygame.transform.scale(pygame.image.load("hacker.png").convert_alpha(), (150, 240)),
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
        self.text = text
        self.font = font
        self.ori_colour = ori_colour
        self.hover_colour = hover_colour
        self.x = x
        self.y = y
        self.hovering = False
        self.rect = self.font.render(self.text, True, self.ori_colour).get_rect(topleft=(self.x, self.y))
        # renders the text as an image using the font and colour, and gets a transparent rectangle that is the size of the rendered text and places it at the position (self.x, self.y)

    def position(self):
        mouse_position = pygame.mouse.get_pos()  # gets current position of the mouse
        self.hovering = self.rect.collidepoint(mouse_position)  # check if mouse is over the button (rect area)

    # collidepoint(...) check hover/click

    # Text for display
    def draw_text(self, window):
        text_colour = self.hover_colour if self.hovering else self.ori_colour
        text_surface = self.font.render(self.text, True, text_colour)  # self.font.render turns text into an image
        rect = text_surface.get_rect(
            topleft=(self.x, self.y))  # get_rect() creates a transparent rectangle which is the same size as the text
        window.blit(text_surface, rect)
        # topleft = .. sets the clickable area to match the text's position.

    def gets_clicked(self):  # make text clickable
        if self.hovering and pygame.mouse.get_pressed()[0]:  # check if left mouse button is pressed
            global action_pile  # read the variable further up
            global all_cards
            print(action_pile)
            print(all_cards.get(self.text))  # print the card images associated with the text
            print(self.text)
            action_pile = all_cards.pop(self.text, action_pile)

            if not interactivity_enable:
                return False

            card_name = self.text.split(' x')[0]
            if card_name in card_text_to_class:
                card_class = card_text_to_class[card_name]
                new_card = card_class()

                if hasattr(new_card, "perform_action"):
                    game = main.GameHandling()
                    initial = game.initialize_game()
                    game.players.append(main.Player("Player"))
                    new_card.perform_action(game, game.players[0])
                    return True
                print("No action...")
                return False
            print("Incorrect card name...")
            return False

            # print(action_pile)
            # print("hello")   # ADD THE FUNCTIONS OF THE CARDS HERE
            # game = main.Game()
            # game.players.append(main.Player("Diana"))
            # game.initialize_game()
            # action_card = main.Hacker
            # print("access this?")
            # action_card.perform_action(action_card, game, game.players[0])
            # print("accessed")
            # print(all_cards.get(self.text))
            # print(self.text)
            # action_pile = all_cards.pop(self.text, action_pile)
            # return True

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
        if not interactivity_enable:
            return False

        mouse_position = pygame.mouse.get_pos()  # gets current position of the mouse
        if self.rect.collidepoint(mouse_position):  # check if mouse is over the button (rect area)
            if pygame.mouse.get_pressed()[0]:  # check if left mouse button is pressed
                print("Click")
                return True


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

# Action cards text for display
actions_text = [
    Clickable_text("Hacker", font_1, White, Orange, 290, 580),
    Clickable_text("Sick Leave", font_1, White, Orange, 290, 600),
    Clickable_text("U turn", font_1, White, Orange, 290, 620),
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
    card_counts = player.count_card_occurrences()

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
        ###"No Chance": (290, 740),
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
    all_text = []
    for card_name, (x, y) in card_definitions.items():
        count = card_counts.get(card_name, 0)
        display_text = f"{card_name} x{count}" if count > 0 else f"{card_name} x0"
        text_obj = Clickable_text(display_text, font_1,
                                  White if count > 0 else Gray,  # Gray out if count is 0
                                  Orange, x, y)
        all_text.append(text_obj)

    return all_text


text_1 = font_1.render("Press SPACE key to pause", True, Dark_Green)
text_2 = font_2.render("Select players:", True, Black)

# ====================================================== INTIALISE GAME MODE ==========================================================

# current game mode
game_status = "menu"
instruction_page = 1
current_player = 0  # Player1 = 0 ; Player2 = 1, Player3 = 2
action_pile = None
num_players = 0
interactivity_enable = True

def enable_interactivity():
    global interactivity_enabled
    interactivity_enabled = True
    print("button enabled")

def disable_interactivity():
    global interactivity_enabled
    interactivity_enabled = False
    print("button disabled")


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

        # background image
        window.blit(background_img, (0, 0))

        # text_image ---> Press Space Key to Pause
        window.blit(text_1, (780, 20))

        # player's text
        player_colour = [Dark_Green if i == current_player else Black for i in range(num_players)]

        # display text with their positions on interface
        if num_players == 2:
            window.blit(player_hori_mid, (400, -40))
            player1_text = font_2.render("Player 1", Black, player_colour[0])
            window.blit(player1_text, (470, 56))

        if num_players == 3:
            window.blit(player_ver_left, (-50, 260))
            window.blit(player_ver_right, (800, 260))
            player1_text = font_2.render("Player 1", True, player_colour[0])
            player2_text = font_2.render("Player 2", True, player_colour[1])
            window.blit(player1_text, (40, 350))
            window.blit(player2_text, (855, 355))

        if num_players == 4:
            window.blit(player_ver_left, (-50, 260))
            window.blit(player_hori_mid, (400, -40))
            window.blit(player_ver_right, (800, 260))
            player1_text = font_2.render("Player 1", True, player_colour[0])
            player2_text = font_2.render("Player 2", True, player_colour[1])
            player3_text = font_2.render("Player 3", True, player_colour[2])
            window.blit(player1_text, (40, 350))
            window.blit(player2_text, (470, 55))
            window.blit(player3_text, (855, 355))

        # shield image
        if current_player == 0:
            window.blit(extra_shield_img, (470, 575))

        # Drawing "End Turn" button
        if current_player == 0:
            end_turn_button.draw()

        # drawing "Play a card" button
        play_card_button.draw()

        # grouped all cards
        all_cards = {**main_cards, **action_cards, **character_cards}  # Merge all card dictionaries together **

        # Display each card on the screen
        current_position = [330, 250]  # fixed position for all cards
        for name, image in all_cards.items():  # items(), lopping dict
            window.blit(image, current_position)
            current_position = [current_position[0] + 2,
                                current_position[1]]  # position of the deck of cards, +2 means the gap between cards

        if action_pile is not None:
            window.blit(action_pile, (560, 250))

        # Display each card text on screen
        if current_player == 0:
            for text in actions_text + character_text:
                text.position()
                text.draw_text(window)



    # ============================== PAUSING INTERFACE ==========================
    elif game_status == "paused":
        window.blit(paused_img, (0, 0))  # add background image when pausing
        other_buttons["resume"].draw()
        other_buttons["Menu"].draw()


    # ============================== WINNER INTERFACE ==========================
    elif game_status == "result":
        window.blit(result_img, (0, 0))


# ===================================== DUMMY FUNCTIONS================================================

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


# =================================================== MAIN GAME LOOP ====================================================================================================


game_running = True
game = GameHandling()
while game_running:  # start the loop - keep going while the game is on
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
                game.players_setup(2, "Player1")
                num_players = 2
                current_player = 0
                fade_transition(1000, 800, White, "playing")
                game.initialize_game()
                game_status = "playing"

            elif option_button["3P"].gets_clicked():
                button_sf.play()
                pygame.time.delay(300)
                game.players_setup(3, "Player1")
                num_players = 3
                current_player = 0
                fade_transition(1000, 800, White, "playing")
                game.initialize_game()
                game_status = "playing"

            elif option_button["4P"].gets_clicked():
                button_sf.play()
                pygame.time.delay(300)
                game.players_setup(4, "Player1")
                num_players = 4
                current_player = 0
                fade_transition(1000, 800, White, "playing")
                game.initialize_game()
                game_status = "playing"



        # =============== MAIN GAMEPLAY SCREEN =================
        elif game_status == "playing":
            #game.main_loop()

            # Switching to next player   ### End turn functionality here ###
            if end_turn_button.gets_clicked():
                game.end_turn(current_player)
                current_player += 1  # increment 1
                if current_player >= num_players:
                    current_player = 0  # loops back to fist player so player1 --> player 2 ---> player 3 ----> player 1

            # grouped all cards
            all_cards = {**main_cards, **action_cards, **character_cards}  # Merge all card dictionaries together **

            # Display each card on the screen
            current_position = [700, 700]  # fixed position for all cards
            for name, image in all_cards.items():  # items(), lopping dict
                window.blit(image, current_position)
                current_position = [current_position[0] + 2, current_position[
                    1]]  # position of the deck of cards, +2 means the gap between cards

            for text in all_text:
                if text.gets_clicked():
                    text_sf.play()

            if end_turn_button.gets_clicked():
                print("end turn")
                player = main.Player("Player 1")
                print(player)
                game = main.GameHandling()
                print(game)

                game.end_turn(player)
                game.next_player_turn() ###############
                print("end turn2")

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                if shield_rect.collidepoint(mouse_position):
                    print("Shield used!")
                    shield_sf.play()
                    action_pile = main_cards["shield"]


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

        # =============== WINNER INTERFACE ====================
        elif game_status == "result":
            window.blit(result_img, (0, 0))

    draw_window()
    pygame.display.update()


# pygame.quit()


def main_loop(self):
    """Main loop of the game which controls the flow of the game"""
    self.game_over = False
    current_player = self.players[self.current_player_index]

    while not self.game_over:
        # 5674312
        if self.losers.get(current_player) is not None:  # current player is not playing
            number_of_losers = 0
            winner = None  # will store a player who is still in the game
            for i in self.players:  # iterate over the 2 to 4 players
                if self.losers.get(i) is not None:  # if player is a loser
                    number_of_losers += 1
                else:
                    winner = i  # player isn't a loser, if player is alone then the player is the winner
            if number_of_losers == len(self.players) - 1:  # player is alone
                self.game_over = True
                print(f"{winner.player_name} is the winner!")
            self.next_player_turn()
            current_player = self.players[self.current_player_index]  # update current player
            continue
        # 5674312
        # start the game
        print(f"{current_player.player_name}'s turn!")
        if self.current_player_index == 0:
            ### HANDLE IN INTERFACE
            print("Cards in hand:")
            for i, card in enumerate(current_player.player_cards):
                print(f"{i + 1}. {card.card_name}")  # displaying player's hand

            # player turn loop
            turn_ended = False
            while not turn_ended and not self.game_over:
                # display choices to the player
                print("1: Play a card")
                print("2: End turn")

                if play_card_button.gets_clicked():  # option 1 to play a card
                    if not current_player.player_cards:
                        print("No cards to play!")
                    else:
                        # display cards in interface
                        for i, card in enumerate(current_player.player_cards):
                            print(f"{i + 1}. {card.card_name}: {card.card_description}")

                        chosen_card = card_gets_selected()  # replace this with the function that already exists in the ui

                        if 0 <= chosen_card < len(current_player.player_cards):
                            card = current_player.player_cards[chosen_card]

                            # manage different card types
                            if card.card_type == "Action":
                                if card.perform_action(self, current_player):
                                    current_player.player_cards.remove(card)
                                    self.discard_card_pile.append(card)
                                    self.last_played_action_card = card
                                    if card.card_name == "Sick Leave":
                                        turn_ended = True

                            elif card.card_type == "Character":
                                self.manage_character_cards(current_player, card)
                                current_player.player_cards.remove(card)
                                self.discard_card_pile.append(card)

                            else:  # for other card types; like the shield
                                print("This card cannot be played directly")
                        else:
                            print("Card does not exist!")


                elif end_turn_button.gets_clicked():  # option 2 to end turn
                    self.end_turn(current_player)
                    self.next_player_turn()
                    turn_ended = True  # exit the player turn loop




        else:  # handle bot scenario
            self.handle_bot_turn(current_player)
            # move on to next player while game is still ongoing
        if not self.game_over:
            self.next_player_turn()
            current_player = self.players[self.current_player_index]  # update current player


#game = GameHandling()
#game.players_setup()
#game.initialize_game()
#game.main_loop()
pygame.quit()


