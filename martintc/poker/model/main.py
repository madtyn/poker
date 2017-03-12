'''
Created on 26 feb. 2017

@author: madtyn
'''
from martintc.poker.model.diceset import DiceSet
import random

if __name__ == '__main__':
    numPlayers = 3
    print('Liar poker game')
    print('Initializing players')
    players = ['p{}'.format(x + 1) for x in range(numPlayers)]
    currentPlayer = 0
    dice = DiceSet()
    print('Player {} has thrown {!s}'.format(players[currentPlayer], dice))
    print('Player {} hides/shows some dice'.format(players[currentPlayer]))
    print('Player {} says {!s}'.format(players[currentPlayer], dice.hand()))
    _ = [die.show() for die in dice if random.choice([True, False])]
    print('{!r}'.format(dice))
