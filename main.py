#CS Python Project

import random
from queue import Queue

from interface import all_cards     # main: line 490 - interface: line 146 (variable name )

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
            1: "A",
            2: "B",
            3: "C",
            4: "D",
            5: "E"
        }
        descriptions = {
            1: "Collect 2: Take a random card from another player",
            2: "Collect 3: Name a specific card to take from another player",
            3: "Collect 5: Take any card from the stack of played cards",
            4: "Special abilities when collected in combinations",
            5: "Complete set gives powerful effect"
        }
        super().__init__(
            card_name = names[character_number],
            card_type = "character",
            card_description = descriptions[character_number],
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
        super().__init__("Hacker", "Action", "Pick a card from any position in the deck", index)

    def perform_action(self, game, current_player):
        if game.deck:
            card = random.choice(game.deck) # picks a random card from the deck
            game.deck.remove(card) # removes the random card from the deck
            current_player.player_cards.append(card) # appends the random card to the player's cards
        return True

class TheSpell(ActionCard):
    def __init__(self, index = -1):
        # inheriting attributes from parent class Card
        super().__init__("The Spell", "Action", "Peek at the top 3 cards in the deck", index)

    def perform_action(self, game, current_player):
        print(f"Top three cards: {[c.card_name for c in game.deck[:3]]}") # gets the top 3 cards and includes them in a list to display to the player by using list comprehension
        return False

class Shuffle(ActionCard):
    def __init__(self, index = -1):
        # inheriting attributes from parent class Card
        super().__init__("Shuffle", "Action", "Shuffle the deck", index)

    def perform_action(self, game, current_player):
        random.shuffle(game.deck)    ### NOTE TO GROUP: IMPLEMENT A SHUFFLING ALGORITHM (AS WELL AS IN THE MAIN LOOP)
        print("The deck is shuffled")
        return False

class Reveal(ActionCard):
    def __init__(self, index = -1):
        # inheriting attributes from parent class Card
        super().__init__("Reveal", "Action", "Reveal the top 3 cards to all players", index)
        ### NOTE: THIS SHOULD APPEAR TO ALL PLAYERS; NOT LIKE THE SPELL

    def perform_action(self, game, current_player):
        print(f"Cards revealed: {[c.card_name for c in game.deck[:3]]}") # gets the top 3 cards and includes them in a list to display to the player by using list comprehension
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
        super().__init__("No Chance", "Action", "Block action or character cards from other players", index)

    def perform_action(self, game, current_player):
        print(f"{current_player.name} played No Chance")
        ### NOTE TO GROUP: REJECTION FUNCTION WILL BE ADDED HERE DURING IMPLEMENTATION IN THE MAIN LOOP
        return False

class Mirror(ActionCard):
    def __init__(self, index = -1):
        # inheriting attributes from parent class Card
        super().__init__("No Chance", "Action", "Copy the last played action card", index)

    def perform_action(self, game, current_player):
        if game.last_played_action_card and game.last_played_action_card.card_name not in ["Mirror", "You're in Trouble"]: # error handling
            print(f"Mirroring {game.last_played_action_card.card_name}")
            ### NOTE TO GROUP: COPYING FUNCTION WILL BE ADDED HERE DURING IMPLEMENTATION IN THE MAIN LOOP
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
        self.character_counts = {1:0, 2:0, 3:0, 4:0, 5:0}
# ID: 5676233

# ID: 5674312
''' Class for RedBlackNode:
initializing class; variable instances:
    red: is False when node is black, and True when node is red
    parent: stores the parent node of the instance
    card: stores the card data and the index in the stack
    left: stores the left child node
    right: stores the right child node 
    '''
class RedBlackNode:
    def __init__(self, card):
        self.red = False
        self.parent = None
        self.card = card
        self.left = None
        self.right = None


# red black tree will represent the stack of cards
# using the red black tree data structure, we can remove the top card in O(log(n))
# using the red black tree data structure, we can insert a card into any position in the stack in O(log(n))
''' Class for RedBlackTree:
initializing class; variable instances:
    nil: empty node (also used as leaf nodes for the tree)
    root: root node
    '''
class RedBlackTree:
    def __init__(self):
        self.nil = RedBlackNode(Card("null","null","null")) #initialize first node
        self.root = self.nil # set starting nil root

    #insert

    def insert_card(self, card):
        red_black_node = RedBlackNode(card) # create new node
        red_black_node.parent = None
        red_black_node.left = self.nil
        red_black_node.right = self.nil
        red_black_node.red = True

        current_node = self.root # binary search: to be compared with new node
        parent_node = None
        while current_node != self.nil:
            parent_node = current_node # when while loop ends, we will have the parent of the new node
            # compare the index of new node with index of current node
            if red_black_node.card.index < current_node.card.index: # go down left subtree
                current_node = current_node.left
            elif red_black_node.card.index > current_node.card.index: # go down right subtree
                current_node = current_node.right

        red_black_node.parent = parent_node
        if parent_node is None: # first card in tree
            self.root = red_black_node # set as current root
        elif red_black_node.card.index < parent_node.card.index: # set node as left subtree of parent
            parent_node.left = red_black_node
        elif red_black_node.card.index > parent_node.card.index: # set node as right subtree of parent
            parent_node.right = red_black_node

        self.fix_tree_insert(red_black_node)

    def fix_tree_insert(self, new_node):
        while new_node != self.root and new_node.parent.red is True:
            if new_node.parent == new_node.parent.parent.right: # check if new node's parent is to the right of new node's parent-parent
                u = new_node.parent.parent.left # parent is to the right and u is to the left of the subtree of the parent-parent
                if u.red is True: # if u.red is True then it has a value, if not, it is nil
                    # set parent of new node and it's sibling (u) as black
                    u.red = False
                    new_node.parent.red = False
                    new_node.parent.parent.red = True # set parent of parent as red
                    new_node = new_node.parent.parent # jump to parent-parent for next iteration where rotation will happen
                else:
                    if new_node == new_node.parent.left:
                        new_node = new_node.parent
                        self.rotate_right(new_node)
                    new_node.parent.red = False
                    new_node.parent.parent.red = True
                    self.rotate_left(new_node.parent.parent) # re-balancing the tree to keep colors in order
            else:
                u = new_node.parent.parent.right # parent of new node is to the left, 'u' will take the right node of the parent-parent
                if u.red is True: # if u.red is True then it has a value, if not, it is nil
                    u.red = False
                    new_node.parent.red = False
                    new_node.parent.parent.red = True # set parent of parent as red
                    new_node = new_node.parent.parent
                else:
                    if new_node == new_node.parent.right:
                        new_node = new_node.parent
                        self.rotate_left(new_node)
                    new_node.parent.red = False
                    new_node.parent.parent.red = True
                    self.rotate_right(new_node.parent.parent)
        self.root.red = False

    def rotate_left(self, u):
        v = u.right # right child of u, to be shifted closer to root, u will be shifted further away from root
        u.right = v.left # assign left child of v to right child of u
        if v.left != self.nil:
            v.left.parent = u # set parent of previous left child of v to u, since it is now the right child of u
        v.parent = u.parent # bringing v closer to the root by assigning its parent as u's parent
        if u.parent is None: # no parent means u is the root
            self.root = v # set v as root as u is shifted below the root
        elif u.parent.left == u: # u was a left child
            u.parent.left = v # set v as the left child of u's previous parent
        else: # u was right child
            u.parent.right = v # set v as the right child of u's previous parent
        v.left = u
        u.parent = v

    def rotate_right(self, u):
        v = u.left # left child of u, to be shifted closer to the root, u will be shifted further away from root
        u.left = v.right # assign right child of v
        if v.right != self.nil:
            v.right.parent = u # set parent of previous right child of v to u, since it is now the left child of u
        v.parent = u.parent # bringing v closer to the root by assigning its parent as u's parent
        if u.parent is None:
            self.root = v # set v as root
        elif u.parent.right == u: # u was a left child
            u.parent.right = v # set v as the left child of u's previous parent
        else:
            u.parent.left = v # set v as the right child of u's previous parent
        v.right = u
        u.parent = v

    # delete

    def shift_nodes(self, old, new):
        if old.parent is None: # if old node was root, set new node as root
            self.root = new
        elif old.parent.left == old: # if old node was left child, set new node as left child instead
            old.parent.left = new
        else: # if old parent as right child, set new node as right child instead
            old.parent.right = new
        new.parent = old.parent # set new node's parent as old node's parent

    def minimum(self, node): # find minimum index within subtree with node as its root
        current_node = node
        minimum_node = node
        while current_node != self.nil: # continue down the left path of the subtree
            minimum_node = current_node
            current_node = current_node.left
        return minimum_node

    def find_largest_node(self):
        # we only delete a node when we remove the top card from the deck, so we search for the card with the largest index
        node = self.root
        largest_node = self.root
        while node != self.nil:
            largest_node = node
            # keep going down the path on the right
            node = node.right
        return largest_node

    def delete(self, node_to_be_deleted):
        y = node_to_be_deleted
        y_original_color = node_to_be_deleted.red # store color of node
        if node_to_be_deleted.left == self.nil: # if left child is nil, shift right child in place of node
            x = node_to_be_deleted.right
            self.shift_nodes(node_to_be_deleted, node_to_be_deleted.right)
        elif node_to_be_deleted.right == self.nil: # if right child is nil, shift left child in place of node
            x = node_to_be_deleted.left
            self.shift_nodes(node_to_be_deleted, node_to_be_deleted.left)
        else:
            y = self.minimum(node_to_be_deleted.right) # y is the minimum node from right subtree of node_to_be_deleted
            y_original_color = y.red # keep track of y's color
            x = y.right
            if y.parent == node_to_be_deleted:
                x.parent = y
            else:
                self.shift_nodes(y, y.right) # replace minimum node with nil
                y.right = node_to_be_deleted.right # set y's right child as the right child of node_to_be_deleted
                y.right.parent = y # set parent of right child of node_to_be_deleted to y
            self.shift_nodes(node_to_be_deleted, y) # replacing deleted node with y
            y.left = node_to_be_deleted.left
            y.left.parent = y
            y.red = node_to_be_deleted.red

        if y_original_color is False: # bring balance back to tree
            self.delete_fixup(x)

    def delete_fixup(self, x):
        while x!= self.root and x.red is False: # while x is black and not the root of the tree
            if x == x.parent.left: # when x is a left child
                w = x.parent.right # w is x's sibling, AKA the right child of x's parent
                # case 1, when w is red:
                if w.red is True:
                    w.red = False # set w as black
                    x.parent.red = True # set parent of x and w to red
                    self.rotate_left(x.parent)
                    w = x.parent.right # set w to x's new sibling
                # case 2, when w, and its children are black
                if w.left.red is False and w.right.red is False:
                    w.red = True
                    x = x.parent # preparation for next iteration
                else:
                    # case 3, when w is black, w left child is red, and w right child is black
                    if w.right.red is False:
                        w.left.red = False # now both children are black
                        w.red = True # set w as red
                        self.rotate_right(w)
                        w = x.parent.right # set w to x's new sibling
                    #case 4 will automatically be done after case 3
                    # case 4, when w is black, w left child is black, and w right child is red
                    w.red = x.parent.red
                    x.parent.red = False
                    w.right.red = False
                    self.rotate_left(x.parent)
                    x = self.root
            else: # when x is a right child
                w = x.parent.left # w is x's sibling, AKA the left child of x's parent
                #case 1
                if w.red is True:
                    w.red = False
                    x.parent.red = True
                    self.rotate_right(x.parent)
                    w = x.parent.left # set w to x's new sibling
                #case 2
                if w.left.red is False and w.right.red is False:
                    w.red = True
                    x = x.parent
                else:
                    #case 3
                    if w.left.red is False:
                        w.right.red = False
                        w.red = True
                        self.rotate_left(w)
                        w = x.parent.left
                    #case 4
                    w.red = x.parent.red
                    x.parent.red = False
                    w.left.red = False
                    self.rotate_right(x.parent)
                    x = self.root
        x.red = False

    def testing_func_for_traversing_tree(self):
        node = self.root
        q = Queue()
        q.put(node)
        while not q.empty():
            node = q.get()
            if node == self.nil:
                continue
            print(node.card.index, end=" ")
            if node.red:
                print("RED", end= " - ")
            else:
                print("BLACK", end= " - ")
            print("children: ", node.left.card.index, " ", node.right.card.index)
            q.put(node.left)
            q.put(node.right)

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

    def initialize_cards(self):
        # will store an array of random indexes
        array_of_cards_indexes = []
        # will store the cards in a randomized order
        array_of_cards = []
        num_of_inserted_cards = 0
        for i in range(42):
            # multiply by 100 so that we can insert more cards in the tree later depending on query
            array_of_cards_indexes.append(i*100)
        # randomize indexes
        self.fisher_yates_shuffle(array_of_cards_indexes)
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
        return array_of_cards

    def initialize_deck(self):
        # randomized_cards is a list of card objects in a randomized order
        randomized_cards = self.initialize_cards()
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
        return card
# ID 5674312

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
        self.current_player = 0 # initializing the index of the current player
        self.deck = CardDeck()
        self.turn_direction = 1 # sets the direction to 1 for clockwise and -1 for anticlockwise
        self.game_over = False
        self.last_played_action_card = None
        self.discard_card_pile = [] # initializing an empty list to store the played cards
        self.initialize_game() # sets the game; card dealing, picking a player to start, card deck ready...

    def initialize_game(self):
        self.deck.initialize_deck()   ### NOTE: IMPLEMENT A FUNCTION THAT GETS THE INITIAL DECK WITHOUT TROUBLE AND SHIELD CARDS
        for player in self.players:

            for i in range(5): # dealing 5 cards to each player
                card = self.deck.draw_a_card()

                if card:
                    player.player_cards.append(card)

    def draw_card(self, player):
        card = self.deck.draw_a_card() 
        if card:
            player.player_cards.append(card) # adds the card to the player's cards

            if card.card_name == "You're in Trouble": # handles drawing a trouble card case from manage_trouble_card function
                self.manage_trouble_card(player)
            return card
        return None

    def manage_trouble_card(self, player):
        if not player.has_shield:
            print(f"{player.player_name} You're in Trouble and therefore out of the game!")
            self.players.remove(player) # remove a player if they don't have a shield card

            if len(self.players) == 1: # checks for winning case if only one player remains
                self.game_over = True # declares game over
                print(f"{self.players[0].player_name} is the winner!")

        else:
            print(f"{player.player_name} has The Shield. You are safe!")
            # removes the shield card if player got trouble card (to cancel out the effect)
            player.has_shield = False  # Note: implement a check for multiple shields

    def player_plays_card(self, player, card_index):
        # make sure the card index is within the cards in player's cards
        if 0 <= card_index < len(player.player_cards):
            card = player.player_cards[card_index] # get the card object from the player's cards

            if card.card_type == "Action": # manage action cards
                proceed = card.perform_action(self, player) # gets whether the action card was done or not

                if proceed:
                    self.last_played_action_card = card # overwrite (update) the last played action card
                    player.player_cards.pop(card_index) # remove the played card from player's cards
                    self.discard_card_pile.append(card) # add the card to the played card pile
                return proceed

            elif card.card_type == "Character": # manage character card
                self.manage_character_cards(player, card) # process specific character effects and combinations
                player.player_cards.pop(card_index) # remove the played card from player's cards
                self.discard_card_pile.append(card) # add the card to the played card pile
                return True
        return False

    def manage_character_cards(self, player, card):
        pass # to be continued

    def check_character_combinations(self, player):
        pass # to be continued

    def next_player_turn(self):
        pass # to be continued (this should be called in the "End Turn function")

# ID: 5676233

