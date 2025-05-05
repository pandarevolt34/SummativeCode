#CS Python Project

import random

# ID: 5676233
''' Class for Cards:
initializing class; variable instances:
    card_name: stores the name of each card (e.g. "Shield", "You're in trouble")
    card_type: stores the type of the card (e.g. action card, or character card)
    card_description: stores a brief description of each card to guide the user
    index: stores the position of each card in the deck 
    '''

class Card:
    def __init__(self, card_name, card_type, card_description, index = -1):
        self.card_name = card_name
        self.card_type = card_type
        self.card_description = card_description
        self.index = index

class Trouble(Card):
    """Class representing the "You're in Trouble" card which eliminates a player, given they don't have the shield"""
    def __init__(self, index = -1):
        super().__init__("You're in Trouble", "Trouble", " ", index)

class Shield(Card):
    """Class representing "The Shield" card which protects the player from the trouble card"""
    def __init__(self, index = -1):
        super().__init__("The Shield", "Shield", " ", index)

''' Class for CharacterCard:
initializing class by inheriting from class Card; variable instances:
    character_number: assigns numbers to each character card
    index: stores the position of each card
    
    names: assigns character card names to numbers
    description: a brief description of each card to be displayed on the cards
    '''

class CharacterCard(Card):
    def __init__(self, character_number, index = -1):
        names = {
            1: "Ice King",
            2: "BMO",
            3: "Finn",
            4: "Jack",
            5: "Bubblegum",
            6: "Lumpy"
        }
        super().__init__(
            card_name = names[character_number],
            card_type = "character",
            card_description = "", # no descriptions for character cards
            index = index
        )
        self.character_number = character_number
# ID: 5676233

# ID: 5676233
''' Class for ActionCard
initializing class by inheriting from class Card, then creating subclasses for each action card
by inheriting from ActionCard class...
    10 Action Cards; each contributes to prevent from picking the "You're in trouble" losing card:
SickLeave, UTurn, Hacker, TheSpell, Shuffle, Reveal, BeatIt, BegYou, NoChance, and Mirror
'''
class ActionCard(Card):
    def __init__(self, card_name, card_type, card_description, index = -1):
        # inheriting attributes from parent class Card
        super().__init__(card_name, card_type, card_description, index)
        self.used = False

    def perform_action(self, game, current_player):
        raise NotImplementedError   # implementation will be added

class SickLeave(ActionCard):
    def __init__(self, index = -1):
        # inheriting attributes from parent class Card
        super().__init__("Sick Leave", "Action", "End your turn without drawing a card", index)

    def perform_action(self, game, current_player):
        print(f"{current_player.name} used Sick Leave")
        return True

class UTurn(ActionCard):
    def __init__(self, index = -1):
        # inheriting attributes from parent class Card
        super().__init__("U Turn", "Action", "Reverse the direction of the game", index)

    def perform_action(self, game, current_player):
        game.turn_direction *= -1 # turns the game direction to be -1 (anticlockwise)
        print(f"{current_player.name} used U Turn - Direction reversed.")
        return True

class Hacker(ActionCard):
    def __init__(self, index = -1):
        # inheriting attributes from parent class Card
        super().__init__("Hacker", "Action", "Take a card from a random position in the deck", index)

    def perform_action(self, game, current_player):
        card = game.deck.red_black_tree.hacker_action() # picks a random card from the deck
        current_player.player_cards.append(card) # appends the random card to the player's cards
        return True

class TheSpell(ActionCard):
    def __init__(self, index = -1):
        # inheriting attributes from parent class Card
        super().__init__("The Spell", "Action", "Peek at the top 3 cards in the deck", index)

    def perform_action(self, game, current_player): # NEEDS FIXING TO CONSIDER BOT PLAYERS
        top_cards = game.deck.red_black_tree.the_spell_action()
        if top_cards is None:
            return None
        print("Top 3 cards:")
        for i in top_cards:
            print(i.card_name)
        return False

class Shuffle(ActionCard):
    def __init__(self, index = -1):
        # inheriting attributes from parent class Card
        super().__init__("Shuffle", "Action", "Shuffle the deck", index)

    def perform_action(self, game, current_player):
        game.deck.red_black_tree.shuffle_action()
        print("The deck is shuffled")
        return False

class Reveal(ActionCard):
    def __init__(self, index = -1):
        # inheriting attributes from parent class Card
        super().__init__("Reveal", "Action", "Reveal the top 3 cards to all players", index)
        ### NOTE: THIS SHOULD APPEAR TO ALL PLAYERS; NOT LIKE THE SPELL

    def perform_action(self, game, current_player): # FIX THIS LIKE THE SPELL
        top_cards = game.deck.red_black_tree.the_spell_action()
        if top_cards is None:
            return None
        print("Top 3 cards:")
        for i in top_cards:
            print(i.card_name)
        return False

class BeatIt(ActionCard):
    def __init__(self, index = -1):
        # inheriting attributes from parent class Card
        super().__init__("Beat It", "Action", "Avoid drawing a card, and force the next player to play two consecutive turns", index)

    def perform_action(self, game, current_player):
        target_player = game.players[(game.current_player_index + game.turn_direction) % len(game.players)]
        game.special_effects.append(("double_turn", target_player))
        print(f"{target_player.name} should play twice")
        return True

class BegYou(ActionCard):
    def __init__(self, index = -1):
        # inheriting attributes from parent class Card
        super().__init__("Beg You", "Action", "Ask a any player to give you a card of their choice", index)

    def perform_action(self, game, current_player):
        target_player = random.choice([p for p in game.players if p != current_player]) # picks a random player to perform the card's action on
        if target_player.player_cards:
            card = random.choice(target_player.player_cards) # taking a random card from the player's cards
            target_player.player_cards.remove(card) # removes that card from the target player's cards
            current_player.player_cards.append(card) # adds that card to the player who played the action card
        return True

class NoChance(ActionCard):
    def __init__(self, index = -1):
        # inheriting attributes from parent class Card
        super().__init__("No Chance", "Action", "Block action cards from other players", index)

    def perform_action(self, game, current_player):
        print(f"{current_player.name} played No Chance")
        current_player.has_block = True # indicates that the player has a ready block response
        return True


class Mirror(ActionCard):
    def __init__(self, index = -1):
        # inheriting attributes from parent class Card
        super().__init__("Mirror", "Action", "Copy the last played action card", index)

    def perform_action(self, game, current_player):
        if not game.last_played_action_card and game.last_played_action_card.card_name not in ["Mirror", "You're in Trouble"]: # error handling
            print("No action card to mirror.")
            return False

        last_card = game.last_played_action_card
        print(f"Mirroring {last_card.card_name}")

        try:
            # create instances of the same card type
            new_card = type(last_card)(index=-1) # using -1 as a temporary index
            result = new_card.perform_action(game, current_player)

            if result:
                return True
            return False

        except Exception as e:
            print(f"Mirror failed: {str(e)}")
            return False
# ID: 5676233

# ID: 5676233
''' Player class description:
initializing class; parameters:
    player_name: stores the name of players
    
    player_cards: a list which stores the cards in players' hand
    has_shield: initializes a flag to track if player has shield for protection or not (also useful in implementing bots)
    character_counts: keeps track of the amount of character cards with each player for usage of special combinations (see in class CharacterCard)
    '''

class Player:
    def __init__(self, player_name):
        self.player_name = player_name
        self.player_cards = []
        self.has_shield = False
        self.character_counts = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0}
        self.has_block = False
# ID: 5676233

# ID: 5674312
from Redblacktree import RedBlackTree

''' Class for CardDeck:
this class represents the deck that plays the role between the players and the red black tree which stores the cards
initializing class; variable instances:
    red_black_tree: stores the cards in the red black tree structure
    counter: keeps track of how many cards have been removed so far
    '''
class CardDeck:
    def __init__(self):
        # the stack of cards
        self.red_black_tree = RedBlackTree()
        self.counter = 0

    def fisher_yates_shuffle(self, arr):
        # loop from starting from len(arr)-1 down to 0
        for i in range(len(arr)-1, 0, -1):
            # select a random index from 0 to i
            index = random.randint(0, i)
            # swap card stored at index with card stored at i
            arr[index], arr[i] = arr[i], arr[index]

    def initialize_cards(self, num_of_players):
        # will store an array of random indexes
        array_of_cards_indexes = []
        # will store the cards in a randomized order
        array_of_cards = []
        num_of_inserted_cards = 0
        for i in range(72):
            # multiply by 100 so that we can insert more cards in the tree later depending on query
            array_of_cards_indexes.append(i*100)
        # randomize indexes
        self.fisher_yates_shuffle(array_of_cards_indexes)
        for i in range(1, 7):
            for j in range(4):
                card = CharacterCard(i, array_of_cards_indexes[num_of_inserted_cards])
                num_of_inserted_cards += 1
                array_of_cards.append(card)
        for i in range(4):
            card = SickLeave()
            # link card with a random index
            card.index = array_of_cards_indexes[num_of_inserted_cards]
            num_of_inserted_cards += 1
            array_of_cards.append(card)
        for i in range(4):
            card = UTurn()
            card.index = array_of_cards_indexes[num_of_inserted_cards]
            num_of_inserted_cards += 1
            array_of_cards.append(card)
        for i in range(4):
            card = Hacker()
            card.index = array_of_cards_indexes[num_of_inserted_cards]
            num_of_inserted_cards += 1
            array_of_cards.append(card)
        for i in range(5):
            card = TheSpell()
            card.index = array_of_cards_indexes[num_of_inserted_cards]
            num_of_inserted_cards += 1
            array_of_cards.append(card)
        for i in range(4):
            card = Shuffle()
            card.index = array_of_cards_indexes[num_of_inserted_cards]
            num_of_inserted_cards += 1
            array_of_cards.append(card)
        for i in range(4):
            card = Reveal()
            card.index = array_of_cards_indexes[num_of_inserted_cards]
            num_of_inserted_cards += 1
            array_of_cards.append(card)
        for i in range(4):
            card = BeatIt()
            card.index = array_of_cards_indexes[num_of_inserted_cards]
            num_of_inserted_cards += 1
            array_of_cards.append(card)
        for i in range(4):
            card = BegYou()
            card.index = array_of_cards_indexes[num_of_inserted_cards]
            num_of_inserted_cards += 1
            array_of_cards.append(card)
        for i in range(5):
            card = NoChance()
            card.index = array_of_cards_indexes[num_of_inserted_cards]
            num_of_inserted_cards += 1
            array_of_cards.append(card)
        for i in range(4):
            card = Mirror()
            card.index = array_of_cards_indexes[num_of_inserted_cards]
            num_of_inserted_cards += 1
            array_of_cards.append(card)
        for i in range(num_of_players - 1):
            card = Trouble()
            card.index = array_of_cards_indexes[num_of_inserted_cards]
            num_of_inserted_cards += 1
            array_of_cards.append(card)
        for i in range(7 - num_of_players):
            card = Shield()
            card.index = array_of_cards_indexes[num_of_inserted_cards]
            num_of_inserted_cards += 1
            array_of_cards.append(card)
        return array_of_cards

    def initialize_deck(self, num_of_players):
        # randomized_cards is a list of card objects in a randomized order
        randomized_cards = self.initialize_cards(num_of_players)
        for i in range(len(randomized_cards)):
            # insert
            self.red_black_tree.insert_card(randomized_cards[i])

    def draw_a_card(self):
        # find card at the top of the deck
        node = self.red_black_tree.find_largest_node()
        if node is self.red_black_tree.nil:
            return None
        # take card data
        card = node.card
        # delete node
        self.red_black_tree.delete(node)
        self.counter += 1
        return card
# ID 5674312

# ID: 5676233
'''Class for Hand
this class manages cards in player's hand; playing cards from hand and storing cards in hand

'''

class Hand:
    def __init__(self, player_names):
        self.players = [Player(name) for name in player_names]
        self.last_played_action_card = None
        self.discard_card_pile = []  # initializing an empty list to store the played cards
        self.game_over = False
        self.deck = CardDeck()


    def end_turn(self, player): ### NOTE TO GROUP: changed draw_card to be 'End Turn' functionality
        """Draw a card from the deck to end turn and progress to next player"""
        player.has_block = False # Reset unused 'no chance' block states
        card = self.deck.draw_a_card()
        if card:
            player.player_cards.append(card)  # adds the card to the player's cards

            if card.card_name == "You're in Trouble":  # handles drawing a trouble card case from manage_trouble_card function
                self.manage_trouble_card(player)
            return card
        # NOTE FROM RAYAN: The return ends the function and it won't reach this line
        self.current_player_index = (self.current_player_index + 1) % len(self.players) # move to next player

    def manage_trouble_card(self, player):
        """Manages the effects of drawing a trouble card"""
        if player.has_shield:
            print(f"{player.player_name} has The Shield. You are safe!")
            # removes the shield card if player got trouble card (to cancel out the effect)
            player.has_shield = False # Note: implement a check for multiple shields
        else:
            print(f"{player.player_name} You're in Trouble and therefore out of the game!")
            self.players.remove(player) # remove a player if they don't have a shield card

            # check for winning case if only one player remains
            if len(self.players) == 1:
                self.game_over = True # declares game over
                print(f"{self.players[0].player_name} is the winner!")

    def player_plays_card(self, player, card_index):   ### NOTE TO GROUP: This function may be removed (duplication in main loop)
        """Play a card from the player's cards in hand"""
        # make sure the card index is within the cards in player's cards
        if 0 <= card_index < len(player.player_cards):
            card = player.player_cards[card_index]  # get the card object from the player's cards

            if card.card_type == "Action":  # manage action cards
                proceed = card.perform_action(self, player)  # gets whether the action card was done or not

                if proceed:
                    self.last_played_action_card = card  # overwrite (update) the last played action card
                    player.player_cards.pop(card_index)  # remove the played card from player's cards
                    self.discard_card_pile.append(card)  # add the card to the played card pile
                return proceed

            elif card.card_type == "Character":  # manage character card
                self.manage_character_cards(player, card)  # process specific character effects and combinations
                player.player_cards.pop(card_index)  # remove the played card from player's cards
                self.discard_card_pile.append(card)  # add the card to the played card pile
                return True
        return False

    def manage_character_cards(self, player, card):
        """Manage all possible character cards combinations and effects"""
        # update character counter when a character card is played
        player.character_counts[card.character_number] += 1
        self.check_character_combinations(player)

    def check_character_combinations(self, player):
        """Checks for the appropriate character cards combinations and proceed with suitable actions"""
        for char_num, count in player.character_counts.items():
            if count == 2:  # check for 2 of the same character card
                self.activate_char_combo(player, char_num, 2)
            elif count == 3:  # check for 3 of the same character card
                self.activate_char_combo(player, char_num, 3)

        if all(count >= 1 for count in
               player.character_counts.values()):  # check for a full set; 1 of each 6 character cards
            self.activate_full_set_combo(player)

    def activate_char_combo(self, player, char_num, combo_type):
        """Activates character cards combinations effects"""
        target = next((p for p in self.players if p != player and p.player_cards),
                      None)  # NOTE: will change to letting the player chose the target (later in interface)
        if not target:
            return

        if any(card.card_name == "No Chance" for card in
               target.player_cards):  # check for cancelling effect with 'No Chance'
            print(f"{target.player_name} blocked your character combination with 'No Chance!'")

        if combo_type == 2:  # 2 of the same character card
            if target.player_cards:
                given_card = random.choice(
                    target.player_cards)  # NOTE: will change random choice to target player choice; target chooses a card to give (later in interface)
                target.player_cards.remove(given_card)  # removing card from target player's cards
                player.player_cards.append(given_card)  # adding card to player's cards
                print(f"{target.player_name} gave {player.name} a card!")

        elif combo_type == 3:  # 3 of the same character card
            if target.player_cards:
                stolen_card = random.choice(target.player_cards)  # takes a random card from target player
                target.player_cards.remove(stolen_card)  # removing card from target player's cards
                player.player_cards.append(stolen_card)  # adding card to player's cards
                print(f"{player.name} took a random card from {target.player_name}!")

    def activate_full_set_combo(self, player):
        """Activate special character cards combinations effects"""
        # find the target player; NOTE: will change to letting the player chose the target (later in interface)
        target = next((p for p in self.players if p != player and p.player_cards), None)
        if not target:
            return

        # check for cancelling effect with 'No Chance'
        if any(card.card_name == "No Chance" for card in target.player_cards):
            print(f"{target.player_name} blocked your character combination with 'No Chance!'")
            return

        # player names a card to request from target player
        # NOTE: will change to let player chose (later in interface)
        chosen_card_name = random.choice([c.card_name for c in target.player_cards]) if target.player_cards else None

        for card in target.player_cards:
            if card.card_name == chosen_card_name:
                target.player_cards.remove(card)
                player.player_cards.append(card)
                print(f"{player.name} took {card.card_name} from {target.player_name}!")
                break
            else:
                print(f"{target.player_name} does not have {chosen_card_name}!")
# ID: 5676233

# ID: 5676233
'''Class for Game:
this class manages the game state and includes the main loop. Variable instances:
    player_names: stores player names 
    
    current_player: stores current player index
    self.deck = CardDeck() ; uses the CardDeck implementation 
    turn_direction: stores the current direction; 1 for clockwise and -1 for anticlockwise
    game_over: stores the game status 
    last_played_action_card: stores the last played card index
    discard_card_pile: a list to store the played cards
    '''
class Game:
    def __init__(self, player_names):
        self.players = [Player(name) for name in player_names]
        self.current_player_index = 0 # initializing the index of the current player
        self.discard_card_pile = []  # initializing an empty list to store the played cards
        self.deck = CardDeck() #creating CardDeck instance; making CardDeck a property of Game
        self.turn_direction = 1 # sets the direction to 1 for clockwise and -1 for anticlockwise
        self.initialize_game()  # sets the game; card dealing, picking a player to start, card deck ready...
        self.game_over = False
        self.hand = Hand(self) # passing game instance to Hand

    def players_setup(self):
        """Sets the players with a human player and a chosen number of bots"""
        while True:
            try:
                # asking the user for number of players
                num_of_players = int(input("Enter the number of players between 2-4: "))
                if 2 <= num_of_players <= 4:
                    break
                print("Invalid number of players! Enter a number between 2-4")
            except ValueError:
                print("Please enter a number!")

        # getting player names
        human_name = input("Enter your name: ")
        bot_name = ["CPU1", "CPU2", "CPU3"]

        # define players
        self.players = [Player(human_name)]
        for i in range(num_of_players - 1): # excluding the human player
            self.players.append(Player(bot_name[i])) # adding bots based on user's choice

    def initialize_game(self):
        """Initialize the game with card deck and deal appropriate cards to players"""
        self.deck.initialize_deck(len(self.players))   ### NOTE: IMPLEMENT A FUNCTION THAT GETS THE INITIAL DECK WITHOUT TROUBLE AND SHIELD CARDS
        # # dealing 5 cards to each player from initialized deck
        for player in self.players:
            for i in range(5):
                card = self.deck.draw_a_card()
                if card:
                    player.player_cards.append(card)

        # give each player 1 shield card
        for player in self.players:
            shield_card = Shield()
            player.player_cards.append(shield_card)
            player.has_shield = True

    '''def start_player_turn(self):
        """Starts the player's turn while handling both the human and bot turns"""
        current_player = self.players[self.current_player_index]

        if current_player.player_name.startswith("CPU"):
            self.handle_bot_turn(current_player)
        else:
            self.waiting_for_player_action = True
            self.current_player_actions = self.get_available_actions(current_player)'''

    def get_available_actions(self, player):
        """Get all the available actions for a player"""
        actions = []

        # add playable cards as actions
        for i, card in enumerate(player.player_cards): # adding a counter to each card to track count
            actions.append({
                'type': 'play_card',
                'card_index': i,
                'card_name': card.card_name,
                'card_type': card.card_type
            })

        ### NOTE: add an end turn action
        return actions

    def handle_player_action(self, action): ### NOTE TO GROUP: This function may be removed (duplication in main loop)
        """Handle all possible cases of a player's chosen action card"""
        if action['type'] == 'play_card':
            card_index = action['card_index']
            current_player = self.players[self.current_player_index]

            if 0 <= card_index < len(current_player.player_cards):
                card = current_player.player_cards[card_index]

                if card.card_type == "Action":
                    card.perform_action(self, current_player)
                elif card.card_type == "Character":
                    self.hand.manage_character_cards(current_player, card)

                # remove the played card and add it to discard pile
                current_player.player_cards.pop(card_index)
                self.discard_card_pile.append(card)

        elif action['type'] == 'end_turn':
            self.hand.end_turn()
    # ID: 5676233

    #5674312
    def handle_bot_turn(self, bot):
        pass # to be continued after bot implementation...
    #5674312

    def next_player_turn(self):
        """Move on to the next player's turn"""
        self.current_player_index = (self.current_player_index + self.turn_direction) % len(self.players) # move to next player

        current_player = self.players[self.current_player_index]
        current_player.character_counts = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0} # reset character counter at the start of turn

        print(f"{current_player.player_name}'s turn!")
        # NOTE: character counter tracker needs modification

    def main_loop(self):
        """Main loop of the game which controls the flow of the game"""
        self.game_over = False
        current_player = self.players[self.current_player_index]

        while not self.game_over:
            # start the game
            print(f"{current_player.player_name}'s turn!")

            ### HANDLE IN INTERFACE
            print("Cards in hand:")
            for i, card in enumerate(current_player.player_cards):
                print(f"{i+1}. {card.card_name}") # displaying player's hand

            # player turn loop
            turn_ended = False
            while not turn_ended and not self.game_over:
                # display choices to the player
                print("1: Play a card")
                print("2: End turn")

                try:
                    choice = int(input("Enter your choice: ")) # get player's choices
                    if choice == 1: # option 1 to play a card
                        if not current_player.player_cards:
                            print("No cards to play!")
                            continue # skip back to the choices display

                        print("Pick a card to play:") # re-display the player's hand with description of cards
                        for i, card in enumerate(current_player.player_cards):
                            print(f"{i+1}. {card.card_name}: {card.card_description}")

                        try:
                            chosen_card = int(input("Choose a card: ")) - 1
                            if 0 <= chosen_card < len(current_player.player_cards):
                                card = current_player.player_cards[chosen_card]
                                # handling the 'no chance' card; check if another player is blocking
                                if card.card_type in ["Action", "Character"]:
                                    blocked = any(p.has_block for p in self.players if p != current_player)

                                    if blocked:
                                        blocker = next(p for p in self.players if p.has_block)
                                        print(f"{blocker.player_name} blocks using 'No Chance'")
                                        blocker.has_block = False
                                        continue

                                # manage different card types
                                if card.card_type == "Action":
                                    if card.perform_action(self, current_player):
                                        current_player.player_cards.pop(chosen_card)
                                        self.discard_card_pile.append(card)
                                        self.hand.last_played_action_card = card
                                        print(f"Card played: {card.card_name}") ### NOTE TO GROUP: these print statements are just for clarification as it will be removed in the interface

                                elif card.card_type == "Character":
                                    self.hand.manage_character_cards(current_player, card)
                                    current_player.player_cards.pop(chosen_card)
                                    self.discard_card_pile.append(card)
                                    print(f"Card played: {card.card_name}")

                                else: # for other card types; like the shield
                                    print("THis card cannot be played directly")
                            else:
                                print("Card does not exist!")
                        except ValueError:
                            print("Enter a valid number.")

                    elif choice == 2: # option 2 to end turn
                        self.hand.end_turn(current_player)
                        turn_ended = True # exit the player turn loop

                    else: # if input is not 1 or 2
                        print("Enter 1 or 2:")

                except ValueError:
                    print("Enter a valid number.")

                # move on to next player while game is still ongoing
            if not self.game_over:
                self.next_player_turn()
                current_player = self.players[self.current_player_index] # update current player


# ID: 5676233


##### NOTE TO GROUP: Add docstrings + fix docstring format