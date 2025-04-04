#CS Python Project

# ID: 5674312
class FenwickTree:  # the stack of cards template
    def __init__(self):  # initializing class
        self.tree = []  # will store the stack so that we can operate adding and removing cards in log(n) time
        self.powers_of_2 = [0]*7301

    def initiate_powers_of_2(self):  # store powers of 2 in a list
        for i in range(26):
            self.powers_of_2.append(2 ** i)  # powers_of_2[index] = 2 ^ index

    def add_card_position_to_tree(self, card):  # Adds card to the tree structure
        index = card.index # take the index of the card in the array
        while index <= 7300:
            self.tree[index] += 1 # add presence of the number
            index += index & (-index) # set largest OFF binary bit to ON

    def remove_top_card_from_tree(self, card):
        # to be continued
        return