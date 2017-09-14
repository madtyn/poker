'''
Created on 26 feb. 2017

@author: madtyn
'''
import random

from martintc.poker.model.diceset import DiceSet


def main():
    '''
    Main function
    '''
    numPlayers = 3
    print('Liar poker game')
    print('Initializing players')
    players = ['p{}'.format(x + 1) for x in range(numPlayers)]
    currentPlayer = 0
    dice = DiceSet()
    print('Player {} has thrown {!r}'.format(players[currentPlayer], dice))

    print('Player {} hides/shows some dice'.format(players[currentPlayer]))
    _ = [die.show() for die in dice if random.choice([True, False])]

    print('Players can see now {0!s} of {0!r}'.format(dice))
    print('Player does not give up {} says {!s}'.format(players[currentPlayer], dice.hand()))
    print()


if __name__ == '__main__':
    main()
