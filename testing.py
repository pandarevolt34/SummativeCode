from main import RedBlackTree
from main import Card

red_black_tree = RedBlackTree()
for i in range(1, 13):
    card = Card("null","null","null", i)
    red_black_tree.insert_card(card)
red_black_tree.testing_func_for_traversing_tree()
print()
for i in range(6, 13):
    red_black_tree.delete(i)
red_black_tree.testing_func_for_traversing_tree()