'''
Created on 26 feb. 2017

@author: madtyn
'''
import random
import sys



from martintc.poker.model.diceset import DiceSet

from gettext import translation

OPTS = [
        {'code':'0',  'desc':'(ó_ò)'},
        {'code':'en', 'desc':'English'},
        {'code':'es', 'desc':'Español'}
        ]

for idx, option in enumerate(OPTS):
    print('{} {}'.format(idx, option['desc']))

idxSelected = None
while not isinstance(idxSelected, int) or not (0 < idxSelected < len(OPTS)) :
    try:
        idxSelected = int(input('=> : '))
    except ValueError:
        pass

if not idxSelected:
    sys.exit(0)

locale = OPTS[idxSelected]['code']
lang = translation('poker', '/home/madtyn/PycharmProjects/poker/resources/locale', languages=[locale])
lang.install()


def main():
    '''
    Main function
    '''
    MINIMUM = DiceSet([1, 2, 3, 4, 5])

    NUM_PLAYERS = 3
    print(_('Liar poker game'))
    print(_('Initializing players'))
    players = ['p{}'.format(x + 1) for x in range(NUM_PLAYERS)]

    currentPlayer = 0

    # Only when initial round
    minimum = MINIMUM
    realDice = DiceSet()
    print(_('Player {} has initially thrown {!r}').format(players[currentPlayer], realDice))
    # Only when initial round


    impossibleWithRealDice = realDice.surpassProb() == 0
    impossibleWithVisibleDice = realDice.surpassProb(len(realDice.availableDice())) == 0

    if impossibleWithRealDice or impossibleWithRealDice:
        surrender(players[currentPlayer])

    print(_('Player {} hides/shows some dice').format(players[currentPlayer]))
    showDice(realDice)
    print(_('Players can see now {0!s} of {0!r}').format(realDice))

    diceToTell = realDice
    falseDice = realDice.lie() # This should be higher than realDice

    lying = decideToLie()
    if lying:
        diceToTell = falseDice.lie()
    diceToTell.show()

    print(_('Player {} does not give up and says {!s}').format(players[currentPlayer], diceToTell))
    input(_('Press key to continue'))

    # Now action is given to next player
    # Changing mechanism
    previousPlayer = currentPlayer
    currentPlayer = (currentPlayer + 1) % len(players)

    # Player vs player mechanism
    accepted = accepts()
    if accepted:
        print(_('Player {} accepts').format(players[currentPlayer]))
        minimum = diceToTell
    else:
        print(_('Player {} rejects!').format(players[currentPlayer]))
        if realDice < diceToTell  or realDice < minimum:
            loser = currentPlayer
        else:
            loser = previousPlayer
        print(_('Player {} loses one life').format(players[loser]))
        loserStillAlive = True
        if loserStillAlive:
            currentPlayer = loser

        # We make all start again for whoever the currentPlayer is

    print(_('We start another round again'))


def accepts():
    # TODO In human players this asks for believing or not the play hand offered
    # TODO in computer players
    return random.choice([True, False])


def surrender(player):
    print(_('Player {} surrenders!').format(player))
    sys.exit(0)


def showDice(dice):
    # While there are more than 3 hidden dice
    MAX_HIDDEN_DICE = 3
    while( len(dice.hiddenDice()) > MAX_HIDDEN_DICE):
        _ = [die.show() for die in dice if random.choice([True, False])]

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
