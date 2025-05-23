# CS Python Project

from Redblacktree import RedBlackTree
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
    def __init__(self, card_name, card_type, card_description, index=-1):
        self.card_name = card_name
        self.card_type = card_type
        self.card_description = card_description
        self.index = index


class Trouble(Card):
    """Class representing the "You're in Trouble" card which eliminates a player, given they don't have the shield"""

    def __init__(self, index=-1):
        super().__init__("You're in Trouble", "Trouble", " ", index)


class Shield(Card):
    """Class representing "The Shield" card which protects the player from the trouble card"""

    def __init__(self, index=-1):
        super().__init__("The Shield", "Shield", " ", index)


''' Class for CharacterCard:
initializing class by inheriting from class Card; variable instances:
    character_number: assigns numbers to each character card
    index: stores the position of each card
    
    names: assigns character card names to numbers
    description: a brief description of each card to be displayed on the cards
    '''


class CharacterCard(Card):
    def __init__(self, character_number, index=-1):
        names = {
            1: "Ice King",
            2: "BMO",
            3: "Finn",
            4: "Jake",
            5: "Bubblegum",
            6: "Lumpy"
        }
        super().__init__(
            card_name=names[character_number],
            card_type="character",
            card_description="",  # no descriptions for character cards
            index=index
        )
        self.character_number = character_number


# ID: 5676233, 5674312
''' Class for ActionCard
initializing class by inheriting from class Card, then creating subclasses for each action card
by inheriting from ActionCard class...
    9 Action Cards; each contributes to prevent from picking the "You're in trouble" losing card:
SickLeave, UTurn, Hacker, TheSpell, Shuffle, Reveal, BeatIt, BegYou, and Mirror
'''


class ActionCard(Card):
    def __init__(self, card_name, card_type, card_description, index=-1):
        # inheriting attributes from parent class Card
        super().__init__(card_name, card_type, card_description, index)
        self.used = False

    def perform_action(self, game, current_player):
        raise NotImplementedError  # implementation will be added


class SickLeave(ActionCard):
    """Class representing "Sick Leave" card which ends a player's turn without drawing a card"""

    def __init__(self, index=-1):
        # inheriting attributes from parent class Card
        super().__init__("Sick Leave", "Action", "End your turn without drawing a card", index)

    def perform_action(self, game, current_player):
        print(f"{current_player.player_name} used Sick Leave")
        return True


class UTurn(ActionCard):
    """Class representing "U Turn" card which reverses the direction of the game"""

    def __init__(self, index=-1):
        # inheriting attributes from parent class Card
        super().__init__("U Turn", "Action", "Reverse the direction of the game", index)

    def perform_action(self, game, current_player):
        game.turn_direction *= -1  # turns the game direction to be -1 (anticlockwise)
        print(f"{current_player.player_name} used U Turn - Direction reversed.")
        return True


class Hacker(ActionCard):
    """Class representing "Hacker" card which draws a card from a random position in the deck"""

    def __init__(self, index=-1):
        # inheriting attributes from parent class Card
        super().__init__("Hacker", "Action", "Take a card from a random position in the deck", index)

    def perform_action(self, game, current_player):
        print(f"{current_player.player_name} used Hacker!")
        card = game.deck.red_black_tree.hacker_action()  # picks a random card from the deck
        if card:
            game.deck.num_of_cards -= 1
            if card.card_name == "You're in Trouble":
                game.manage_trouble_card(current_player)
            else:
                current_player.player_cards.append(card)  # appends the random card to the player's cards
                if card.card_name == "The Shield":
                    current_player.has_shield.append(card)
            return True
        return False


class TheSpell(ActionCard):
    """Class representing "The Spell" card which allows a player to peek at the top 3 cards in the deck"""

    def __init__(self, index=-1):
        # inheriting attributes from parent class Card
        super().__init__("The Spell", "Action", "Peek at the top 3 cards in the deck", index)

    def perform_action(self, game, current_player):
        print(f"{current_player.player_name} used TheSpell")
        top_cards = game.deck.red_black_tree.the_spell_action()
        if top_cards is None:
            return False
        print("Top 3 cards:")
        for i in top_cards:
            print(i.card_name)
        return True


class Shuffle(ActionCard):
    """Class representing "Shuffle" card which shuffles the deck"""

    def __init__(self, index=-1):
        # inheriting attributes from parent class Card
        super().__init__("Shuffle", "Action", "Shuffle the deck", index)

    def perform_action(self, game, current_player):
        print(f"{current_player.player_name} used Shuffle - The deck is shuffled")
        game.deck.red_black_tree.shuffle_action()
        return True


class Reveal(ActionCard):
    """Class representing "Reveal" card which allows all players to see the top 3 cards of the deck"""

    def __init__(self, index=-1):
        # inheriting attributes from parent class Card
        super().__init__("Reveal", "Action", "Reveal the top 3 cards to all players", index)

    def perform_action(self, game, current_player):
        print(f"{current_player.player_name} used Reveal!")
        top_cards = game.deck.red_black_tree.the_spell_action()
        if top_cards is None:
            return False
        print("Top 3 cards:")
        for i in top_cards:
            print(i.card_name)
        return True


class BeatIt(ActionCard):
    """Class representing "Beat It" card which skips the player's turn and makes the next player play twice"""

    def __init__(self, index=-1):
        # inheriting attributes from parent class Card
        super().__init__("Beat It", "Action",
                         "Avoid drawing a card, and force the next player to play two consecutive turns", index)

    def perform_action(self, game, current_player):
        temporary_index = (game.current_player_index + game.turn_direction) % len(game.players)
        target_player = game.players[temporary_index]
        while target_player in game.losers or target_player == current_player:  # prevent target from being player or loser
            temporary_index = (temporary_index + game.turn_direction) % len(game.players)
            target_player = game.players[temporary_index]
        card = game.deck.draw_a_card()
        if card:
            print(f"{target_player.player_name} has taken an extra card from the deck")
            if card.card_name == "You're in Trouble":  # handles drawing a trouble card case from manage_trouble_card function
                game.manage_trouble_card(target_player)
            else:
                target_player.player_cards.append(card)  # adds the card to the player's cards
                if card.card_name == "The Shield":
                    target_player.has_shield.append(card)
            return True


class BegYou(ActionCard):
    """Class representing "Beg You" card which gives the player a random card in the hand of another player"""

    def __init__(self, index=-1):
        # inheriting attributes from parent class Card
        super().__init__("Beg You", "Action", "A random player will give you a random card of theirs", index)

    def perform_action(self, game, current_player):
        print(f"{current_player.player_name} used Beg You!")
        available_players = []  # picks a random player to perform the card's action on
        for i in game.players:
            if i not in game.losers and i is not current_player:
                available_players.append(i)
        target_player = random.choice(available_players)
        if target_player.player_cards:
            card = random.choice(target_player.player_cards)  # taking a random card from the player's cards
            target_player.player_cards.remove(card)  # removes that card from the target player's cards
            current_player.player_cards.append(card)  # adds that card to the player who played the action card
            if card.card_name == "The Shield":
                target_player.has_shield.remove(card)
                current_player.has_shield.append(card)
        else:
            print(f"{target_player.player_name} has no cards therefore Beg You affect is cancelled!")
        return True


class Mirror(ActionCard):
    """Class representing "The Shield" card which mirrors the last action card if possible"""

    def __init__(self, index=-1):
        # inheriting attributes from parent class Card
        super().__init__("Mirror", "Action", "Copy the last played action card", index)

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
            result = last_card.perform_action(game, current_player)
            game.discard_card_pile.append(last_card)
            return result

        except Exception as e:
            print(f"Mirror failed: {str(e)}")
            return False


# ID: 5676233, 5674312

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
        self.has_shield = []
        self.character_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
        '''self.has_block = False'''


# ID: 5676233

# ID: 5674312

''' Class for CardDeck:
this class represents the deck that plays the role between the players and the red black tree which stores the cards
initializing class; variable instances:
    red_black_tree: stores the cards in the red black tree structure
    counter: increases as trouble cards and shields are added to the deck
    num_of_cards: keeps track of how many cards are left in the deck
    '''


class CardDeck:
    def __init__(self):
        # the stack of cards
        self.red_black_tree = RedBlackTree()
        self.counter = 1
        self.num_of_cards = 0

    def fisher_yates_shuffle(self):
        """shuffles an array with numbers from 1 to 61 using fisher_yates_algorithm"""
        arr = []
        for i in range(61):  # originally 66 but now 61
            # multiply by 100 so that we can insert more cards in the tree later depending on query
            arr.append(i * 100)
        for i in range(len(arr) - 1, 0, -1):
            # select a random index from 0 to i
            index = random.randint(0, i)
            # swap card stored at index with card stored at i
            arr[index], arr[i] = arr[i], arr[index]
        return arr

    def initialize_cards(self):
        """initializes cards and links them with a random index"""
        array_of_cards = []  # will store the cards in a randomized order
        num_of_inserted_cards = 0  # keeps track of how many cards have been inserted so far
        array_of_cards_indexes = self.fisher_yates_shuffle()
        for i in range(1, 7):
            for j in range(4):
                card = CharacterCard(i, array_of_cards_indexes[num_of_inserted_cards])
                num_of_inserted_cards += 1
                array_of_cards.append(card)
        for i in range(4):
            card = SickLeave()
            card.index = array_of_cards_indexes[num_of_inserted_cards]  # link card with a random index
            num_of_inserted_cards += 1
            array_of_cards.append(card)
        for i in range(4):
            card = UTurn()
            card.index = array_of_cards_indexes[num_of_inserted_cards]  # link card with a random index
            num_of_inserted_cards += 1
            array_of_cards.append(card)
        for i in range(4):
            card = Hacker()
            card.index = array_of_cards_indexes[num_of_inserted_cards]  # link card with a random index
            num_of_inserted_cards += 1
            array_of_cards.append(card)
        for i in range(5):
            card = TheSpell()
            card.index = array_of_cards_indexes[num_of_inserted_cards]  # link card with a random index
            num_of_inserted_cards += 1
            array_of_cards.append(card)
        for i in range(4):
            card = Shuffle()
            card.index = array_of_cards_indexes[num_of_inserted_cards]  # link card with a random index
            num_of_inserted_cards += 1
            array_of_cards.append(card)
        for i in range(4):
            card = Reveal()
            card.index = array_of_cards_indexes[num_of_inserted_cards]  # link card with a random index
            num_of_inserted_cards += 1
            array_of_cards.append(card)
        for i in range(4):
            card = BeatIt()
            card.index = array_of_cards_indexes[num_of_inserted_cards]  # link card with a random index
            num_of_inserted_cards += 1
            array_of_cards.append(card)
        for i in range(4):
            card = BegYou()
            card.index = array_of_cards_indexes[num_of_inserted_cards]  # link card with a random index
            num_of_inserted_cards += 1
            array_of_cards.append(card)
        for i in range(4):
            card = Mirror()
            card.index = array_of_cards_indexes[num_of_inserted_cards]  # link card with a random index
            num_of_inserted_cards += 1
            array_of_cards.append(card)
        self.num_of_cards = num_of_inserted_cards  # store number of cards in the deck so far
        return array_of_cards

    def initialize_trouble_shield_cards(self, num_of_players):
        """adds You're in Trouble cards and The Shield cards into the deck"""
        for i in range(num_of_players - 1):
            card = Trouble()
            card.index = random.randint(1, (
                    61 - num_of_players * 5))  # select a random integer between 1 and the number of cards in the deck
            card.index *= 100
            card.index += self.counter  # add the counter so that card can be sandwiched between 2 other cards
            self.counter += 1  # increase counter to eliminate possibility of equal indexes
            self.num_of_cards += 1
            self.red_black_tree.insert_card(card)  # insert card into red black tree
        for i in range(7 - num_of_players):
            card = Shield()  # repeat for shield cards
            card.index = random.randint(1, (60 - num_of_players * 5))
            card.index *= 100
            card.index += self.counter
            self.counter += 1
            self.num_of_cards += 1
            self.red_black_tree.insert_card(card)
        pass

    def initialize_deck(self):
        """inserts action and character cards with random indexes into the red-black tree"""
        randomized_cards = self.initialize_cards()  # randomized_cards is a list of card objects with randomized indexes
        for i in range(len(randomized_cards)):
            self.red_black_tree.insert_card(randomized_cards[i])

    def add_trouble_card_back(self):
        """inserts a trouble card back into the deck"""
        card = Trouble()
        card.index = random.randint(1, self.num_of_cards + 1)
        card.index *= 100
        card.index += self.counter
        self.num_of_cards += 1
        self.counter += 1
        self.red_black_tree.insert_card(card)

    def draw_a_card(self):
        """draws a card from the top of the deck"""
        node = self.red_black_tree.find_largest_node()  # holds the node with the greatest index
        if node == self.red_black_tree.nil:
            return None
        card = node.card  # take card data
        self.red_black_tree.delete(node)  # delete node
        self.num_of_cards -= 1  # decrease number of cards currently in the deck
        return card


# ID 5674312

# ID: 5676233, 5674312
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


class GameHandling:
    def __init__(self):
        self.players = []
        self.losers = {}
        self.current_player_index = 0  # initializing the index of the current player
        self.discard_card_pile = []  # initializing an empty list to store the played cards
        self.last_played_action_card = ActionCard("null", "null", "null")  # last played action card for mirror
        self.deck = CardDeck()  # creating CardDeck instance; making CardDeck a property of Game
        self.turn_direction = 1  # sets the direction to 1 for clockwise and -1 for anticlockwise
        self.game_over = False

    def players_setup(self, num_players, human_name="Player1"):
        """Sets the players with a human player and a chosen number of bots"""
        # getting player names
        self.players = [Player(human_name)]
        bot_names = ["CPU1", "CPU2", "CPU3"]

        # Add bot players
        for i in range(num_players - 1):
            self.players.append(Player(bot_names[i]))

    def initialize_game(self):
        """Initialize the game with card deck and deal appropriate cards to players"""
        self.deck.initialize_deck()  ### NOTE: IMPLEMENT A FUNCTION THAT GETS THE INITIAL DECK WITHOUT TROUBLE AND SHIELD CARDS
        # # dealing 5 cards to each player from initialized deck
        for player in self.players:
            for i in range(5):
                card = self.deck.draw_a_card()
                if card:
                    player.player_cards.append(card)

        self.deck.initialize_trouble_shield_cards(len(self.players))  # add the trouble and shield cards

        # give each player 1 shield card
        for player in self.players:
            shield_card = Shield()
            player.player_cards.append(shield_card)
            player.has_shield.append(shield_card)

        # ID: 5676233

    def manage_trouble_card(self, player):
        """Manages the effects of drawing a trouble card"""
        if len(player.has_shield) != 0:
            print(f"{player.player_name} has The Shield. You are safe!")
            # removes the shield card if player got trouble card (to cancel out the effect)
            card = player.has_shield[-1]
            self.discard_card_pile.append(card)
            player.player_cards.remove(card)
            player.has_shield.remove(card)
            self.deck.add_trouble_card_back()
        else:
            print(f"{player.player_name} You're in Trouble and therefore out of the game!")
            self.losers[player] = True  # remove a player if they don't have a shield card

    def manage_character_cards(self, player, card):  # MOST LIKELY ISNT BEING USED, REMOVE PLEASE
        """Manage all possible character cards combinations and effects"""
        # update character counter when a character card is played
        player.character_counts[card.character_number] += 1
        self.check_character_combinations(player)

    def check_character_combinations(self, player):  # MOST LIKELY ISNT BEING USED, REMOVE PLEASE
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
        if combo_type == 2:  # 2 of the same character card
            target = next((p for p in self.players if p != player and p.player_cards and p not in self.losers),
                          None)  # NOTE: will change to letting the player chose the target (later in interface)
            if not target:
                return
            if target.player_cards:
                given_card = random.choice(
                    target.player_cards)  # NOTE: will change random choice to target player choice; target chooses a card to give (later in interface)
                target.player_cards.remove(given_card)  # removing card from target player's cards
                player.player_cards.append(given_card)  # adding card to player's cards
                if given_card.card_name == "The Shield":
                    target.has_shield.remove(given_card)
                    player.has_shield.append(given_card)
                print(f"{player.player_name} took a random card from {target.player_name}!")

        elif combo_type == 3:  # 3 of the same character card
            top_cards = self.deck.red_black_tree.the_spell_action()
            if top_cards is None:
                return False

            print("Top 3 cards:")
            for i in top_cards:
                print(i.card_name)

            if self.current_player_index == 0:
                while True:
                    try:
                        card_choice = int(input("Which card do you want to take: "))
                        if 1 <= card_choice <= len(top_cards):
                            chosen_card = top_cards[card_choice - 1]
                            node_of_chosen_card = self.deck.red_black_tree.find_node(chosen_card)
                            self.deck.red_black_tree.delete(node_of_chosen_card)
                            self.deck.num_of_cards -= 1
                            if chosen_card.card_name == "You're in Trouble":
                                self.manage_trouble_card(player)
                                break
                            player.player_cards.append(chosen_card)
                            if chosen_card.card_name == "The Shield":
                                player.has_shield.append(chosen_card)
                            print(f"Player 1 took a took a card using combo 3")
                            break
                        else:
                            print(f"Enter a number between 1-{len(top_cards)}")
                    except ValueError:
                        print("Enter a valid number.")

            else:  # handling bot player
                chosen_card = random.choice(top_cards)
                node_of_chosen_card = self.deck.red_black_tree.find_node(chosen_card)
                self.deck.red_black_tree.delete(node_of_chosen_card)
                self.deck.num_of_cards -= 1
                player.player_cards.append(chosen_card)
                print(f"{player.player_name} took a took a card using combo 3")

            return True

    def activate_full_set_combo(self, player):
        """Activate special character cards combinations effects"""
        cards = {
            # shield card
            "The Shield": lambda: Shield(),

            # action cards
            "Sick Leave": lambda: SickLeave(),
            "U Turn": lambda: UTurn(),
            "Hacker": lambda: Hacker(),
            "The Spell": lambda: TheSpell(),
            "Shuffle": lambda: Shuffle(),
            "Reveal": lambda: Reveal(),
            "Beat It": lambda: BeatIt(),
            "Beg You": lambda: BegYou(),
            "Mirror": lambda: Mirror(),

            # character cards
            "Ice King": lambda: CharacterCard(1),
            "BMO": lambda: CharacterCard(2),
            "Finn": lambda: CharacterCard(3),
            "Jake": lambda: CharacterCard(4),
            "Bubblegum": lambda: CharacterCard(5),
            "Lumpy": lambda: CharacterCard(6),
        }

        if self.current_player_index == 0:
            print("Cards: ")
            for i, card_name in enumerate(cards.keys(), 1):
                print(f"{i}: {card_name}")

            while True:
                try:
                    choice = int(input("Which card do you want to take: "))
                    if 1 <= choice <= len(cards.keys()):
                        card_name = list(cards.keys())[choice - 1]
                        new_card = cards[card_name]()
                        player.player_cards.append(new_card)

                        if card_name == "The Shield":
                            player.has_shield.append(new_card)
                        print(f"{card_name} was added to your hand")
                        break
                    else:
                        print(f"Enter a number between 1-{len(cards)}")
                except ValueError:
                    print("Enter a valid number.")

        else:  # handling bot
            useful_cards = [
                "The Shield",
                "Hacker",
                "The Spell",
                "Mirror",
                "Shuffle"
            ]

            available_cards = [card for card in useful_cards if card in useful_cards]
            chosen_card_name = random.choice(available_cards) if available_cards else random.choice(
                list(useful_cards.keys()))

            new_card = cards[chosen_card_name]()
            player.player_cards.append(new_card)

            if chosen_card_name == "The Shield":
                player.has_shield.append(new_card)
            print(f"{chosen_card_name} was added to {player.player_name}'s hand")

    # ID: 5676233

    # 5674312

    def handle_bot_turn(self, bot, cards_used=[]):
        """ function allowing the bot to make decisions in the game """
        """
        # debug: for testing game functionality without bot
        self.end_turn()
        return None
        """
        cards_available = {}  # dictionary for cards so that we can see which cards are available
        for i in bot.player_cards:  # iterate through bot's cards
            cards_available[i.card_name] = i  # if bot has card, store in dictionary

        if "U Turn" in cards_available:  # if U Turn is within the bots cards
            card = cards_available["U Turn"]
            if card.perform_action(self, bot):  # if action returns True then it was played
                bot.player_cards.remove(card)  # remove the card
                self.last_played_action_card = card  # set as last action card
                self.discard_card_pile.append(card)  # add card to pile
                cards_used.append(card)  # store in array to output in interface

        revealing_card_used = False  # so we don't repeat reveal after the spell
        if "The Spell" in cards_available:
            revealing_card_used = True
            card = cards_available["The Spell"]
            if card.perform_action(self, bot):
                bot.player_cards.remove(card)
                self.last_played_action_card = card
                self.discard_card_pile.append(card)
                cards_used.append(card)

        if "Beg You" in cards_available:
            card = cards_available["Beg You"]
            if card.perform_action(self, bot):
                bot.player_cards.remove(card)
                self.last_played_action_card = card
                self.discard_card_pile.append(card)
                cards_used.append(card)

        if "Reveal" in cards_available:
            if revealing_card_used is False:
                revealing_card_used = True
                card = cards_available["Reveal"]
                if card.perform_action(self, bot):
                    bot.player_cards.remove(card)
                    self.last_played_action_card = card
                    self.discard_card_pile.append(card)
                    cards_used.append(card)

        if "Mirror" in cards_available:
            if self.deck.num_of_cards >= 50:  # if 50 or more cards in the deck
                if self.last_played_action_card.card_name == "Beat It":  # o
                    card = self.last_played_action_card
                    if card.perform_action(self, bot):
                        card = cards_available["Mirror"]
                        bot.player_cards.remove(card)
                        self.last_played_action_card = card
                        self.discard_card_pile.append(card)
                        cards_used.append(card)
                        return
            elif self.deck.num_of_cards >= 35:
                if (self.last_played_action_card.card_name == "Beat It"
                        or self.last_played_action_card.card_name == "Sick Leave"):
                    card = self.last_played_action_card
                    if card.perform_action(self, bot):
                        card = cards_available["Mirror"]
                        bot.player_cards.remove(card)
                        self.last_played_action_card = card
                        self.discard_card_pile.append(card)
                        cards_used.append(card)
                        return
            elif self.deck.num_of_cards >= 20:
                if (self.last_played_action_card.card_name == "Beat It"
                        or self.last_played_action_card.card_name == "Sick Leave"
                        or self.last_played_action_card.card_name == "Shuffle"):
                    card = self.last_played_action_card
                    if card.perform_action(self, bot):
                        leave = False
                        if (self.last_played_action_card.card_name == "Beat It"
                                or self.last_played_action_card.card_name == "Sick Leave"):
                            leave = True
                        card = cards_available["Mirror"]
                        bot.player_cards.remove(card)
                        self.last_played_action_card = card
                        self.discard_card_pile.append(card)
                        cards_used.append(card)
                        if leave is True:
                            return
            else:
                if self.last_played_action_card.card_name != "null":
                    card = self.last_played_action_card
                    if card.perform_action(self, bot):
                        leave = False
                        if (self.last_played_action_card.card_name == "Beat It" or
                                self.last_played_action_card.card_name == "Sick Leave"):
                            leave = True
                        card = cards_available["Mirror"]
                        bot.player_cards.remove(card)
                        self.last_played_action_card = card
                        self.discard_card_pile.append(card)
                        cards_used.append(card)
                        if leave is True:
                            return

        if "Hacker" in cards_available:
            if self.deck.num_of_cards > 20:
                card = cards_available["Hacker"]
                if card.perform_action(self, bot):
                    bot.player_cards.remove(card)
                    self.last_played_action_card = card
                    self.discard_card_pile.append(card)
                    cards_used.append(card)

        if "Sick Leave" in cards_available:
            if self.deck.num_of_cards <= 20:
                card = cards_available["Sick Leave"]
                if card.perform_action(self, bot):
                    bot.player_cards.remove(card)
                    self.last_played_action_card = card
                    self.discard_card_pile.append(card)
                    cards_used.append(card)
                    return

        if "Shuffle" in cards_available:
            chance = random.randint(1, 100)
            if chance <= 20:
                card = cards_available["Shuffle"]
                if card.perform_action(self, bot):
                    bot.player_cards.remove(card)
                    self.last_played_action_card = card
                    self.discard_card_pile.append(card)
                    cards_used.append(card)

        if "Beat It" in cards_available:
            chance = random.randint(1, 100)
            if chance <= 20 or self.deck.num_of_cards <= 30:
                card = cards_available["Beat It"]
                if card.perform_action(self, bot):
                    bot.player_cards.remove(card)
                    self.last_played_action_card = card
                    self.discard_card_pile.append(card)
                    cards_used.append(card)
                    return
        self.end_turn()

    def next_player_turn(self):
        """Move on to the next player's turn"""
        self.current_player_index = (self.current_player_index + self.turn_direction) % len(
            self.players)  # move to next player

        current_player = self.players[self.current_player_index]
        current_player.character_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0,
                                           6: 0}  # reset character counter at the start of turn
        # NOTE: character counter tracker needs modification

    def play_selected_card(self, wanted_card_name: str) -> None:  # implemented validation and annotation
        """checks if card is in a players hand and plays it"""
        current_player = self.players[self.current_player_index]
        card = None
        for i in current_player.player_cards:
            if i.card_name == wanted_card_name:
                card = i
        if card is None:
            return None
        if card.card_type == "Action":
            if card.perform_action(self, current_player):
                current_player.player_cards.remove(card)
                self.discard_card_pile.append(card)
                self.last_played_action_card = card
                if (card.card_name == "Sick Leave" or card.card_name == "Beat It" or
                        (card.card_name == "Mirror" and (self.discard_card_pile[-2].card_name == "Sick Leave"
                                                         or self.discard_card_pile[-2].card_name == "Beat It"))):
                    self.next_player_turn()

    def end_turn(self):
        """Draw a card from the deck to end turn and progress to next player"""
        print(self.deck.num_of_cards)
        player = self.players[self.current_player_index]
        card = self.deck.draw_a_card()
        if card:
            self.discard_card_pile.append(card)
            if card.card_name == "You're in Trouble":  # handles drawing a trouble card case from manage_trouble_card function
                self.manage_trouble_card(player)
            else:
                player.player_cards.append(card)  # adds the card to the player's cards
                if card.card_name == "The Shield":
                    player.has_shield.append(card)

    def check_winner(self):
        """identifies winner if available"""
        if len(self.losers) == len(self.players) - 1:
            for i in self.players:
                if i not in self.losers:
                    return i.player_name
        return None

    # 5674312

    # 5676233, main loop was used before merging - now outdated

    def main_loop(self):
        """Main loop of the game which controls the flow of the game"""
        self.game_over = False
        current_player = self.players[self.current_player_index]

        while not self.game_over:
            if current_player in self.losers:  # current player is not playing
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

                    try:
                        choice = int(input("Enter your choice: "))  # get player's choices
                        if choice == 1:  # option 1 to play a card
                            if not current_player.player_cards:
                                print("No cards to play!")
                                continue  # skip back to the choices display

                            print("Pick a card to play:")  # re-display the player's hand with description of cards
                            for i, card in enumerate(current_player.player_cards):
                                print(f"{i + 1}. {card.card_name}: {card.card_description}")

                            try:
                                chosen_card = int(input("Choose a card: ")) - 1
                                if 0 <= chosen_card < len(current_player.player_cards):
                                    card = current_player.player_cards[chosen_card]
                                    # handling the 'no chance' card; check if another player is blocking

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
                                        print(f"Card played: {card.card_name}")

                                    else:  # for other card types; like the shield
                                        print("This card cannot be played directly")
                                else:
                                    print("Card does not exist!")  # validation checks
                            except ValueError:
                                print("Enter a valid number.")

                        elif choice == 2:  # option 2 to end turn
                            self.end_turn()
                            turn_ended = True  # exit the player turn loop

                        else:  # if input is not 1 or 2
                            print("Enter 1 or 2:")

                    except ValueError:
                        print("Enter a valid number.")
            else:  # handle bot scenario
                self.handle_bot_turn(current_player)
                # move on to next player while game is still ongoing
            if not self.game_over:
                self.next_player_turn()
                current_player = self.players[self.current_player_index]  # update current player


# ID: 5676233

'''
game = GameHandling()
game.players_setup(2)
game.initialize_game()
game.main_loop()
'''
