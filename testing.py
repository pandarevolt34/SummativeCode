from main import RedBlackTree
from main import Card

red_black_tree = RedBlackTree()
card = Card("null","null","null",1)
red_black_tree.insert_card(card)
card2 = Card("null","null","null",2)
red_black_tree.insert_card(card2)
card3 = Card("null","null","null",3)
red_black_tree.insert_card(card3)
card4 = Card("null","null","null",4)
red_black_tree.insert_card(card4)
red_black_tree.testing_func_for_traversing_tree()