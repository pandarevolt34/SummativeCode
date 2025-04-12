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
            index = index
        )
        self.character_number = character_number

# ID: 5676233
''' Class for ActionCard
initializing class by inheriting from class Card, then creating subclasses for each action card
by inheriting from ActionCard class...
    10 Action Cards; each contributes to prevent from picking the "You're in trouble" losing card:
SickLeave, UTurn, Hacker, TheSpell, Shuffle, Reveal, BeatIt, BegYou, NoChance, and Mirror
'''
class ActionCard(Card):
    def __init__(self, card_name, card_type, card_description, index = -1):
        super().__init__(card_name, card_type, card_description, index)
        self.used = False

    def perform_action(self, game, current_player):
        raise NotImplementedError   # implenentation will be added

class SickLeave(ActionCard):
    def __init__(self, index = -1):
        super().__init__("Sick Leave", "Action", "End your turn without drawing a card", index)

    def perform_action(self, game, current_player):
        print(f"{current_player.name} used Sick Leave")

class UTurn(ActionCard):
    def __init__(self, index = -1):
        super().__init__("U Turn", "Action", "Reverse the direction of the game", index)

    def perform_action(self, game, current_player):
        game.turn_direction *= -1
        print(f"{current_player.name} used U Turn - Direction reversed.")
# ID: 5676233



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

    def search(self, index):
        node = self.root
        # search for node
        while node != self.nil:
            if node.card.index == index:
                return node
            elif node.card.index < index:
                node = node.right
            else:
                node = node.left
        return None

    def delete(self, index):
        node_to_be_deleted = self.search(index)
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
        cnt = 1
        cnt2 = 0
        while not q.empty():
            node = q.get()
            print(node.card.index, end=" ")
            if node.red:
                print("RED", end= " - ")
            else:
                print("BLACK", end= " - ")
            cnt2 += 1
            if cnt2 == cnt:
                cnt *= 2
                cnt2 = 0
                print()
            if node != self.nil:
                q.put(node.left)
                q.put(node.right)
        '''
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
            '''
# to be continued
# ID 5674312