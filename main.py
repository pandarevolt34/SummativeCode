#CS Python Project

import random

from queue import Queue

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

        red_black_node.parent = parent_node
        if parent_node is None: # first card in tree
            self.root = red_black_node # set as current root
        elif red_black_node.card.index < parent_node.card.index: # set node as left subtree of parent
            parent_node.left = red_black_node
        elif red_black_node.card.index > parent_node.card.index: # set node as right subtree of parent
            parent_node.right = red_black_node

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

    def testing_func_for_traversing_tree(self):
        node = self.root
        print("Output path from root to left farthest node")
        while node != self.nil:
            print(node.card.index)
            if node.red is True:
                print("RED")
            else:
                print("BLACK")
            node = node.left
        node = self.root
        print("Output path from root to right farthest node")
        while node!= self.nil:
            print(node.card.index)
            if node.red is True:
                print("RED")
            else:
                print("BLACK")
            node = node.right
# to be continued
# ID 5674312