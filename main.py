#CS Python Project

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
''' Card class description:
initializing class; parameters:
    card_name: 
    card_type:
    card_description:
    index:
    '''
class Card:
    def __init__(self, card_name, card_type, card_description, index = -1):
        self.card_name = card_name
        self.card_type = card_type
        self.card_description = card_description
        self.index = index

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
        self.nil = RedBlackNode(Card("null","null","null"))
        self.nil.red = False
        self.nil.left = None
        self.nil.right = None
        self.root = self.nil
