from main import RedBlackTree
from main import Card
'''Test:
Purpose: 
Method used:
'''
red_black_tree = RedBlackTree()
for i in range(1, 13):
    card = Card("null","null","null", i)
    red_black_tree.insert_card(card)
red_black_tree.testing_func_for_traversing_tree()
print()
for i in range(6, 13):
    red_black_tree.delete(i)
red_black_tree.testing_func_for_traversing_tree()

'''Testing result and action taken:
    Results: 
    Action taken: 
    '''





'''Test: Mirror on Mirror prevention in action cards
Purpose: avoid potential infinite mirror chain - game crash
Method used: checking error handling using try-except
'''
from main import Mirror
from main import Player
from main import Game

def test_mirror_on_mirror():
    game = Game()  # Game class implementation in progress...
    player1 = Player("Player 1")
    player2 = Player("Player 2")
    game.players = [player1, player2]

    # Create mirror cards
    mirror1 = Mirror(index=1)
    mirror2 = Mirror(index=2)

    # Set up a scenario where a mirror would try to copy another mirror
    game.last_played_action_card = mirror2
    player1.player_cards.append(mirror1)

    # Test the mirror effect for errors usin try-except
    # To be continued...

'''Testing result and action taken:
    Results: 
    Action taken: 
    '''
