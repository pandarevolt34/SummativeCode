#CS Python Project

import random
# ID: 5674312
class FenwickTree:  # the stack of cards template
    def __init__(self):  # initializing class
        self.tree = []  # will store the stack so that we can operate adding and removing cards in log(n) time
        self.powers_of_2 = [0]*7301
        self.number_of_cards = 72

    def initiate_powers_of_2(self):  # store powers of 2 in a list
        for i in range(26):
            self.powers_of_2.append(2 ** i)  # powers_of_2[index] = 2 ^ index

    def add_card_position_to_tree(self, card):  # Adds card to the tree structure
        index = card.index # take the index of the card in the array
        while index <= 7300:
            self.tree[index] += 1 # add presence of the number
            index += index & (-index) # set largest OFF binary bit to ON

    def remove_top_card_from_tree(self):
        # to be continued
        return

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
            index = index)

''' Player class description:
initializing class; parameters:
    player_name:
    '''

class Player:
    def __init__(self, player_name):
        self.player_name = player_name
        self.player_cards = []
# ID: 5676233

# ID: 5674312
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
class RedBlackTree:
    def __init__(self):
        self.nil = RedBlackNode(Card("null","null","null")) #initialize first node
        self.nil.red = False # set nil node as black
        self.nil.left = None # set empty left subtree
        self.nil.right = None # set empty right subtree
        self.root = self.nil # set starting nil root

    def insert_card(self, card):
        red_black_node = RedBlackNode(card) # create new node
        red_black_node.parent = None
        red_black_node.left = self.nil
        red_black_node.right = self.nil
        red_black_node.red = True

        current_node = self.root # start binary search: to be compared with new node
        parent_node = None
        while current_node != self.nil:
            parent_node = current_node # when while loop ends, we will have the parent of the new node
            # compare the index of new node with index of current node
            if red_black_node.card.index < current_node.card.index: # go down left subtree
                current_node = current_node.left
            elif red_black_node.card.index > current_node.card.index: # go down right subtree
                current_node = current_node.right

        current_node.parent = parent_node
        if parent_node is None: # first card in tree
            self.root = current_node # set as current root
        elif current_node.card.index < parent_node.card.index: # set node as left subtree of parent
            parent_node.left = current_node
        elif current_node.card.index > parent_node.card.index: # set node as right subtree of parent
            parent_node.right = current_node

        self.fix_tree_insert(red_black_node)

    def fix_tree_insert(self, new_node):
        # if the new node's parent is black then we don't need to fix and re root the subtree
        # if it is red, we need to fix since the new node will be taking the color red
        # if the parent is red, then it also has a parent since the root is black
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