from queue import Queue
from random import randint

import random
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
    def __init__(self, card, index = -1):
        self.red = False
        self.parent = None
        self.card = card
        self.index = index
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
        self.nil = RedBlackNode("null") #initialize first node
        self.root = self.nil # set starting nil root

    #insert

    def insert_card(self, card): # CORRECT
        red_black_node = RedBlackNode(card) # create new node
        red_black_node.index = card.index
        red_black_node.left = self.nil
        red_black_node.right = self.nil
        red_black_node.red = True

        current_node = self.root # binary search: to be compared with new node
        parent_node = None
        while current_node != self.nil:
            parent_node = current_node # when while loop ends, we will have the parent of the new node
            # compare the index of new node with index of current node
            if red_black_node.index < current_node.index: # go down left subtree
                current_node = current_node.left
            elif red_black_node.index > current_node.index: # go down right subtree
                current_node = current_node.right

        red_black_node.parent = parent_node
        if parent_node is None: # first card in tree
            self.root = red_black_node # set as current root
        elif red_black_node.index < parent_node.index: # set node as left subtree of parent
            parent_node.left = red_black_node
        elif red_black_node.index > parent_node.index: # set node as right subtree of parent
            parent_node.right = red_black_node

        self.fix_tree_insert(red_black_node)

    def fix_tree_insert(self, new_node): # CORRECT
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

    def rotate_left(self, u): # CORRECT
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

    def rotate_right(self, u): # CORRECT
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

    def shift_nodes(self, old, new): # CORRECT
        if old.parent is None: # if old node was root, set new node as root
            self.root = new
        elif old.parent.left == old: # if old node was left child, set new node as left child instead
            old.parent.left = new
        else: # if old parent as right child, set new node as right child instead
            old.parent.right = new
        new.parent = old.parent # set new node's parent as old node's parent

    def minimum(self, node): # RECURSIVE FUNC # find minimum index within subtree with node as its root
        if node.left != self.nil: # continue down the left path of the subtree
            node = self.minimum(node.left)
        return node

    def find_largest_node(self): # CORRECT
        # we only delete a node when we remove the top card from the deck, so we search for the card with the largest index
        node = self.root
        largest_node = self.root
        while node != self.nil:
            largest_node = node
            # keep going down the path on the right
            node = node.right
        return largest_node

    def delete(self, node_to_be_deleted): # CORRECT
        #print(node_to_be_deleted.index)
        #self.testing_func_for_traversing_tree()
        y = node_to_be_deleted
        y_original_color = y.red # store color of node
        # case 1
        if node_to_be_deleted.left == self.nil: # if left child is nil, shift right child in place of node
            x = node_to_be_deleted.right
            self.shift_nodes(node_to_be_deleted, node_to_be_deleted.right)
        # case 2
        elif node_to_be_deleted.right == self.nil: # if right child is nil, shift left child in place of node
            x = node_to_be_deleted.left
            self.shift_nodes(node_to_be_deleted, node_to_be_deleted.left)
        # case 3
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

    def delete_fixup(self, x): # CORRECT
        #print(x.index)
        #self.testing_func_for_traversing_tree()
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
            print(node.index, " name: ", node.card.card_name, end=" ")
            if node.red:
                print("RED", end= " - ")
            else:
                print("BLACK", end= " - ")
            print("children: ", node.left.index, " ", node.right.index)
            q.put(node.left)
            q.put(node.right)

    # FUNCTIONS FOR ACTION CARDS:
    def hacker_action(self):
        # find a random card from the deck
        node = self.root
        while node != self.nil:
            left_or_right = randint(0, 2)
            # select randomly 0 or 1
            if left_or_right == 0: # if 0 then go left
                node = node.left
            elif left_or_right == 1: # if 1 then go right
                node = node.right
            else: # if 2 then exit loop
                break
        if node == self.nil: # if it's nil then it must have a parent node containing a card
            node = node.parent
        card = node.card # store card data
        self.delete(node) # delete selected node
        return card

    def the_spell_action(self):
        node = self.find_largest_node()
        cards = []
        if node == self.root: # if largest node is the root, then there aren't 3 cards left
            return None # None AKA error
        cards.append(node.card) # 1st card

        if node.left != self.nil: # 2nd largest card is the left child of the largest card
            node2 = node.left
            while node2.right != self.nil:
                node2 = node2.right
            cards.append(node2.card) # 2nd card
            if node2.parent != node:
                node2 = node2.parent
                cards.append(node2.card) # 3rd card
            else:
                node = node.parent
                if node != self.nil:
                    cards.append(node.card)  # 3rd card
                else:
                    return None
                return cards

        else:
            node = node.parent # 2nd largest card is the parent of largest card (also isn't root so parent isn't null)
            cards.append(node.card) # 2nd card
            if node.left != self.nil:
                node2 = node.left
                while node2.right != self.nil:
                    node2 = node2.right
                cards.append(node2.card) # 3rd card
            else:
                node2 = node.parent
                if node2 != self.nil:
                    cards.append(node2.card) # 3rd card
                else:
                    return None
            return cards

    def shuffle_action(self):
        node = self.root
        while node != self.nil:
            if node.left != self.nil and node.right != self.nil:
                card_left = node.left.card
                index_card_left = node.left.index
                card_right = node.right.card
                index_card_right = node.right.index
                node.left.card = card_right
                node.left.index = index_card_left
                node.right.card = card_left
                node.right.index = index_card_right
            node = node.right