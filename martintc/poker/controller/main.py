'''
Created on 26 feb. 2017

@author: madtyn
'''
# TODO - Every I/O should be through an object/class which will be replace by a GUI
# TODO - Every player could be remote or local, as well as human or machine,
# TODO     a proxy player could be an adapter to both

import random
import sys

from martintc.poker.model.diceset import DiceSet
from martintc.poker.view.languages import selectLanguage
from martintc.poker.view.ui import output

lang = selectLanguage()

if lang:
    lang.install()
else:
    sys.exit(0)

# noinspection PyUnresolvedReferences
def main():
    '''
    Main function
    '''
    MINIMUM = DiceSet([1, 2, 3, 4, 5])

    NUM_PLAYERS = 3
    output(_('Liar poker game'))
    output(_('Initializing players'))
    players = ['p{}'.format(x + 1) for x in range(NUM_PLAYERS)]

    currentPlayer = 0
    initial = True
    keepOn = True

    while(keepOn):
        output(_('We start another round again'))
        # Only when initial round
        if initial:
            minimum = MINIMUM
            realDice = DiceSet()
            output(_('Player {} has initially thrown {!r}').format(players[currentPlayer], realDice))
        else:
            # Player vs player mechanism
            # Now action is given to next player
            # Changing mechanism
            previousPlayer = currentPlayer
            currentPlayer = (currentPlayer + 1) % len(players)
            accepted = accepts()
            if accepted:
                initial = False
                output(_('Player {} accepts').format(players[currentPlayer]))
                minimum = diceToTell
            else:
                output(_('Player {} rejects!').format(players[currentPlayer]))

                initial = True
                if realDice < diceToTell or realDice < minimum:
                    loser = currentPlayer
                else:
                    loser = previousPlayer
                output(_('Player {} loses one life').format(players[loser]))
                loserStillAlive = True # TODO Will change depending on number of lifes
                if loserStillAlive:
                    currentPlayer = loser


        impossibleWithRealDice = realDice.surpassProb() == 0
        impossibleWithVisibleDice = realDice.surpassProb(len(realDice.available_dice())) == 0

        if impossibleWithRealDice or impossibleWithRealDice:
            surrender(players[currentPlayer])

        output(_('Player {} hides/shows some dice').format(players[currentPlayer]))
        showDice(realDice)
        output(_('Players can see now {0!s} of {0!r}').format(realDice))

        diceToTell = realDice
        falseDice = realDice.lie() # This should be higher than realDice

        lying = decideToLie()
        if lying:
            diceToTell = falseDice.lie()
        diceToTell.show()

        output(_('Player {} does not give up and says {!s}').format(players[currentPlayer], diceToTell))
        keepOn = input(_('Press Enter to continue or type 0 to leave: '))
        keepOn = (keepOn.strip() != '0')
        # We make all start again for whoever the currentPlayer is


def accepts():
    # TODO In human players this asks for believing or not the play hand offered
    # TODO in computer players
    return random.choice([True, False])


def surrender(player):
    output(_('Player {} surrenders!').format(player))
    sys.exit(0)


def showDice(dice):
    # While there are more than 3 hidden dice
    MAX_HIDDEN_DICE = 3
    while(len(dice.hidden_dice()) > MAX_HIDDEN_DICE):
        output('before {!r}'.format(dice))
        _ = [die.show() for die in dice if die.hidden and random.choice([True, False])]
        output('after {!r}'.format(dice))

def decideToLie(actualDiceset=None):
    """
    Decides if the player's going to lie or not
    :return: True if the player is going to lie, False if not
    """
    # TODO This decission should be complex, it should be different for machines and human players
    # TODO In computer players, this should involve:
    # 1.- Firstly and IMPORTANT, if it's possible to lie with the visible dice
    # 2.- If the actual dice the player knows for sure are higher than needed, it should be PROBABLY false
    # 3.- If the actual dice are not enough for overpassing, the harder it is to overpass, the more PROBABLY is the lie
    # TODO In humans, this just should ask for confirmation to lie
    return random.choice([True, False])


if __name__ == '__main__':
    main()
