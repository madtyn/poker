"""
Created on 18 feb. 2017

@author: madtyn
"""
from copy import deepcopy
from itertools import product, repeat
from fractions import Fraction
from collections import Counter
from operator import itemgetter

from martintc.poker.model.die import Die
from martintc.poker.model.hand import Hand
from martintc.poker.model.utils import compFunc


class DiceSet(object):
    '''
    This class represents a specific move from one player
    gathering the values from different dice to sum up an only value
    for the whole move.
    '''

    def __init__(self, inputList=None, throw=True, length=5):
        '''
        Constructor
        :param inputList: if provided, the list of numeric values for this diceset
        :param throw: if True generates a random diceset by throwing all its dice
        :param length: the length of the diceset, 5 by default
        '''
        if inputList:
            self.dice = [elem if isinstance(elem, Die) else Die(elem) for elem in inputList[:length]]
        elif throw:
            self.dice = [Die(throw=throw) for _ in range(length)]
        else:
            self.dice = []
        self.dice.sort()

    def lie(self, fear=0.75, needToLie=True):
        #TODO list
        '''
        -Devuelve una nueva jugada estrictamente superior, pero el objetivo es que mienta con una probabilidad creible
        y que sea ajustable segun la dificultad
        Hay que tener en cuenta que puede cambiar según los dados tirados, solo habría que mentir sobre los dados tirados Y ocultos
        Tambien hay que tener en cuenta que la posibilidad de superar podria ser unica
        '''
        # probs = float(self.surpassProb())  # Estima la dificultad de superar
        # distance = None  # TODO
        # Comparar la diferencia entre self.dice y la maxima puntuacion que se puede sacar tirando dados ocultos

        # Iniciamos el dado en el minimo posible para superarlo
        dice = DiceSet([Die(min(Die.FACES)) if d.hidden else deepcopy(d) for d in self.dice])
        while dice <= self:  # or (probs - dice.surpassProb()) > fear:  # TODO
            dice = DiceSet([d.lie() if d.hidden else deepcopy(d) for d in self.dice])
            # Tipificar la jugada/mentira entre 0 y 1 para obtener un coeficiente de "credibilidad" (+ diferencia hacia arriba, + dificil)
            # Si es necesaria, mas dificil aun
        return dice

    def surpassProb(self, numDice=None):
        '''
        Calculates the exact probability for surpassing this diceset's value
        with the exact number of 'numDice' dice.

        Example: If numDice = 3, this explores the probability to surpass this diceset
        with all the 3-dice combinations
        '''
        favorableCases = 0
        cases = 0
        '''
        We obtain as many times FACES(=[NRJQKA]) as number of dice (=numDice) in this diceset.
        For numDice=5 dice, it would be 5 lists [NRJQKA], [NRJQKA],...x2..., [NRJQKA]

        Then we do a cartesian product
        (with FACESxFACES it would get all pairs (N,N) (N,R)..(N,A), (R,N),..,(A,A) )
        (with FACESxFACESxFACES it would get all tuples (N,N,N) (N,N,R)..(N,N,A),..,(N,A,A),(R,N,N),..,(A,A,A) )

        So we have now all cases ready for being converted to list and used

        '''
        if not numDice:
            numDice = len(self.dice)
        n_FACES = repeat(Die.FACES, numDice)
        allCases = [DiceSet(list(elem)) for elem in product(*n_FACES)]
        for case in allCases:
            cases += 1
            if case > self:
                favorableCases += 1

        return Fraction(favorableCases, cases)

    def hand(self):
        '''
        Returns the poker hand from these dice
        '''
        numberEqualFaces = sorted(list(self.frequencies().values()), reverse=True)
        return Hand.getHand(numberEqualFaces)

    def frequencies(self, letter=False):
        '''
        Gets a dict counting the faces and the number of faces in these dice.

        :param letter: if True, it returns the letters/faces, if not numbers are returned
        '''
        return Counter([d.getLetter() if letter else d.val for d in self.dice])

    def availableDice(self):
        return DiceSet([deepcopy(d) for d in self.dice if d.numUses > 0])

    def notAvailableDice(self):
        return DiceSet([deepcopy(d) for d in self.dice if d.numUses == 0])

    def visibleDice(self):
        return DiceSet([deepcopy(d) for d in self.dice if not d.hidden])

    def hiddenDice(self):
        return DiceSet([deepcopy(d) for d in self.dice if not d.hidden])

    def sort(self):
        '''
        Sorts the dice from left to right, minor values to max ones
        '''
        self.dice.sort()

    def show(self):
        '''
        Shows the dice
        '''
        for die in self.dice:
            die.show()

    def hide(self):
        '''
        Hides the dice
        '''
        for die in self.dice:
            die.hide()

    def restore(self):
        '''
        Restores the numbers of uses of these dice
        '''
        for die in self.dice:
            die.restore()

    def reset(self):
        '''
        Resets the dice to None
        '''
        for die in self.dice:
            die.reset()

    def test(self):
        '''
        Tests the dice
        '''
        for die in self.dice:
            die.test()

    # PRIVATE API FUNCTIONS

    def __iter__(self):
        '''
        Returns itself as an iterator
        '''
        self.index = -1
        return self

    def __next__(self):
        '''
        Returns next die in the iteration or stops
        '''
        self.index += 1
        if self.index >= len(self.dice):
            self.index = -1
            raise StopIteration
        return self.dice[self.index]

    # OPERATOR FUNCTIONS
    def __contains__(self, dieObj):
        '''
        Check if dieObj is contained in this diceset. Used by 'in' operator

        :param dieObj: the die to check
        '''
        if isinstance(dieObj, Die):
            return dieObj in self.dice

    def __add__(self, other):
        '''
        Returns a new diceset as the addition between dicesets, which would be:

        [1,1] + [3,4] == [1,1,3,4]
        [N,N] + [J,Q] == [N,N,J,Q]

        :param other: the other diceset
        '''
        dset = DiceSet(deepcopy(self.dice) + deepcopy(other.dice))
        return dset

    def __sub__(self, other):
        '''
        Returns a new diceset with these dice and with the dice in other removed

        [1,1,3,3,4] - [1,3,4] == [1,3]

        :param other: the other diceset
        '''
        _dice = deepcopy(self.dice)
        _other = deepcopy(other)

        if isinstance(_other, Die):
            _other = DiceSet([_other])

        if isinstance(_other, DiceSet):
            [_dice.remove(die) for die in _other.dice if die in _dice]

            dset = DiceSet(_dice)
            return dset

    def __truediv__(self, other):
        '''
        Returns a new diceset with these dice and all the dice in other removed

        [1,1,3,3,4] / [1,3,4] == []

        :param other: the other diceset
        '''
        dset = DiceSet([deepcopy(d) for d in self.dice if d not in other.dice])
        return dset

    def __mul__(self, other):
        '''
        Returns a new diceset

        [1,2] * 3  == [1,2,1,2,1,2]
                       1   2   3

        :param other: an integer
        '''
        if isinstance(other, int):
            dset = DiceSet(deepcopy(self.dice) * other)
            return dset
        else:
            return NotImplemented

    # SORTING FUNCTIONS
    @compFunc
    def __cmp__(self, other):
        '''
        Compares two diceset looking at its dice's faces/points
        :param other: the other object to compare with
        '''
        li1 = list(self.frequencies().items())
        li1 = sorted(li1, key=itemgetter(1, 0), reverse=True)

        li2 = list(other.frequencies().items())
        li2 = sorted(li2, key=itemgetter(1, 0), reverse=True)

        length = min(len(li1), len(li2))
        for x, y in zip(li1, li2):
            if x[1] - y[1] != 0:
                return x[1] - y[1]
            elif x[0] - y[0] != 0:
                return x[0] - y[0]
            length -= 1

        return 0

    @compFunc
    def __eq__(self, other):
        '''
        When using the operator (==), compares if this diceset is equal to another one
        :param other: the other diceset to compare with
        '''
        return self.hand() == other.hand() and self.__cmp__(other) == 0

    @compFunc
    def __ne__(self, other):
        '''
        When using the operator (!=), compares if this diceset is different to another one
        :param other: the other diceset to compare with
        '''
        return not self.__eq__(other)

    @compFunc
    def __ge__(self, other):
        '''
        When using the operator (>=), compares if this diceset is greater or equal than another one
        :param other: the other diceset to compare with
        '''
        if self.hand() == other.hand():
            return self.__cmp__(other) >= 0
        else:
            return self.hand() >= other.hand()

    @compFunc
    def __gt__(self, other):
        '''
        When using the operator (>), compares if this diceset is greater than another one
        :param other: the other diceset to compare with
        '''
        if self.hand() == other.hand():
            return self.__cmp__(other) > 0
        else:
            return self.hand() > other.hand()

    @compFunc
    def __le__(self, other):
        '''
        When using the operator (<=), compares if this diceset is less than another one
        :param other: the other diceset to compare with
        '''
        if self.hand() == other.hand():
            return self.__cmp__(other) <= 0
        else:
            return self.hand() <= other.hand()

    @compFunc
    def __lt__(self, other):
        '''
        When using the operator (<), compares if this diceset is less than another one
        :param other: the other diceset to compare with
        '''
        if self.hand() == other.hand():
            return self.__cmp__(other) < 0
        else:
            return self.hand() < other.hand()

    def __len__(self):
        '''
        Returns the length of dice in this combination
        '''
        return len(self.dice)

    def __repr__(self, *args, **kwargs):
        '''
        Unambiguous string representation for this object,
        useful for logging or debugging purposes
        '''
        freqs = {}
        for k, v in self.frequencies(letter=True).items():
            freqs[k] = v
        return '[{}] {}'.format(','.join([repr(die) for die in self.dice]), freqs)

    def __str__(self, *args, **kwargs):
        '''
        Nice readable representation for this object, useful for
        showing in the app
        '''
        return '{} [{}]'.format(self.hand().name, ','.join([str(die) for die in self.dice]))

if __name__ == "__main__":
    # Constructor testing
    print('{!r}'.format(DiceSet()))
    print('{!r}'.format(DiceSet(length=3)))
    print('{!r}'.format(DiceSet(throw=False)))
    print('{!r}'.format(DiceSet(throw=False, length=2)))
    print('{!r}'.format(DiceSet([2, 3, 3, 6])))
    print('{!r}'.format(DiceSet([5, 5, 5, 4, 4], length=4)))
    print('{!r}'.format(DiceSet([2, 2, 2, 6, 6], False)))
    print('{!r}'.format(DiceSet([1, 1, 1, 4, 4], False, 4)))
    print(DiceSet([4, 4]).surpassProb())

    for i in range(10):
        diceset = DiceSet()
        print(diceset, ' ', diceset.surpassProb())

    # Comparison testing
    dicesets = [DiceSet() for _ in range(10)]
    dicesets = [d for d in dicesets if d.hand() > Hand.PAIR]
    for d in dicesets:
        print('{!r} '.format(d))

    for i in range(len(dicesets) - 1):
        x = dicesets[i]
        y = dicesets[i + 1]
        if x == y:
            print('{} == {}'.format(x, y))
        elif x > y:
            print('{} > {}'.format(x, y))
        else:
            print('{} < {}'.format(x, y))
