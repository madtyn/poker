"""
Created on 26 feb. 2017

@author: madtyn
"""
# TODO - Every I/O should be through an object/class which will be replace by a GUI
# TODO - Every player could be remote or local, as well as human or machine,
# TODO     a proxy player could be an adapter to both

import random
import sys
from operator import itemgetter

from martintc.poker.model.diceset import DiceSet
from martintc.poker.model.players import Robot, Players
from martintc.poker.model.status import Status
from martintc.poker.view.languages import selectLanguage
from martintc.poker.view.ui import output

lang = selectLanguage()

if lang:
    lang.install()  # Makes _() available as builtin
else:
    sys.exit(0)


# noinspection PyUnresolvedReferences
def main():
    """
    Main function
    """

    player_names = ['Matt', 'Alice', 'Kevin', 'Natalie', 'John', 'Jennifer']
    NUM_PLAYERS = 5
    output(_('Liar poker game'))
    output(_('Initializing players'))
    players = Players([Robot(x, lives=1) for x in player_names[:NUM_PLAYERS]])
    status = Status(players)

    initial = True
    keep_on = True
    dice_to_tell = None

    while keep_on:

        # Only when initial turn
        if initial:
            minimum = DiceSet.ABSOLUTE_MINIMUM
            dice_to_tell = minimum
        else:
            # Player vs player mechanism
            # Now action is given to next player
            # Changing mechanism
            current_player = status.change_player()
            rejected = not current_player.accepts()

            initial = rejected

            if rejected:
                # We proceed to decide winner
                output(_('Player {0.name} rejects!').format(status.current_player()))

                # The current player has rejected so,
                if real_dice < dice_to_tell:
                    # If it's a lie, he wins. Previous player loses
                    loser = status.prevPlayer()
                else:
                    # It was real. Current player loses
                    loser = status.current_player()
                status.loses(loser)
                if status.winner():
                    output(_('And the winner is {.name}').format(status.winner()))
                    sys.exit(0)

            else:
                # We initialize the next lying round
                output(_('Player {0.name} accepts').format(status.current_player()))
                minimum = dice_to_tell
                minimum.show()
                real_dice.restore()
                output(_('Minimum is {!r}').format(minimum))

        output(_('We start another turn again'))

        # TODO Player should estimate straight away if the current dice can be surpassed with these dice
        # TODO Also, the player could use the advantage of hidden dice
        # impossibleWithRealDice = real_dice.surpassProb() == 0
        # impossibleWithVisibleDice = real_dice.surpassProb(len(real_dice.available_dice())) == 0
        # if impossibleWithRealDice or impossibleWithRealDice:
        #     status.surrenders(status.current_player())

        # We throw dice
        if initial:
            real_dice = DiceSet()
            # TODO If we have surpassed the minimum with the initial throw,
            # TODO we will lie at least with the real values. So we update minimum
            # if real_dice > minimum:
            #     minimum = inferior
        else:
            under_minimum = real_dice <= minimum
            while under_minimum and real_dice.numUses() > 0:
                for face, freq in sorted(list(real_dice.frequencies().items()), key=itemgetter(1, 0)):
                    for d in real_dice:
                        if d.val == face and d.numUses:
                            d.throw()
                            real_dice.sort()  # TODO Every time a die is thrown, the diceset should be AUTO-sorted
                        if real_dice > minimum:
                            under_minimum = False
                            break
                    if not under_minimum:
                        break

        output(_('Player {0.name} has thrown {1!r}').format(status.current_player(), real_dice))
        initial = False

        # TODO Show / hide
        # output(_('Player {0.name} hides/shows some dice').format(status.current_player()))
        # showDice(realDice)
        output(_('Players can see now {0!s} of {0!r}').format(real_dice))

        lying = status.current_player().decide_to_lie(minimum, real_dice)
        if lying:
            dice_to_tell = real_dice.lie()  # This should be higher than real_dice

        if dice_to_tell and dice_to_tell > minimum:
            output(_('Player {.name} does not give up and says {!r}').format(status.current_player(), dice_to_tell))
        else:
            status.surrenders(status.current_player())

        keep_on = input(_('Press Enter to continue or type 0 to leave: '))
        keep_on = (keep_on.strip() != '0')
        # We make all start again for whoever the current_player is


def showDice(dice):
    # While there are more than 3 hidden dice
    MAX_HIDDEN_DICE = 3
    attempts = 0
    while len(dice.hidden_dice()) > MAX_HIDDEN_DICE:
        output('before {!r}'.format(dice))
        __ = [die.show() for die in dice if die.hidden and random.choice([True, False])]
        output('after {!r}'.format(dice))
        attempts += 1
        if attempts >= 30:
            # It has no sense hiding dice
            break


if __name__ == '__main__':
    main()


def challenges(self, lier, believer):
    pass
