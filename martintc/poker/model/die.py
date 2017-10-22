import random
from martintc.poker.model.utils import compFunc, reverseDict
from martintc.poker.model.errors import NotAllowedError

'''
Created on 18 feb. 2017

@author: madtyn
'''


class Die(object):
    """
    This is the class which will simulate a die.
    It can hold a value. It can be hidden or not. Etc...
    """
    # This makes the number to letter conversion
    LETTERS = {1: 'N', 2: 'R', 3: 'J', 4: 'Q', 5: 'K', 6: 'A'}

    # The inverse dict, for reverse conversion (letter to number)
    NUMBERS = reverseDict(LETTERS)

    # FACES = [1,2,3,4,5,6]
    FACES = sorted(LETTERS.keys())

    def __init__(self, value=False, throw=True, hide=True, numUses=1):
        """
        Constructor

        :param throw: if True, it assigns a random value to this Die
        :param hide: if True, it hides this die and sets its hidden status to True
        :param value: the internal value
        """
        self.numUses = numUses
        self.hidden = hide

        if value or value is None:
            self.val = value
        elif throw:
            self.throw()
        else:
            self.val = None
            # It doesn't make sense to hide a None value
            self.hidden = False

    def throw(self):
        """
        Generates a random number from the list [1,2,3,4,5,6]
        """
        if self.numUses:
            self.val = random.choice(Die.FACES)
            self.numUses -= 1
            return self.val
        raise NotAllowedError('El dado {} ha agotado sus tiradas'.format(self))

    def lie(self):
        """
        Returns a new Die with value equal or higher than this one
        :return: a new instance of Die
        """
        return Die(value=random.choice([x for x in Die.FACES if x >= self.val]), hide=True, numUses=0)

    def restore(self, numUses=1):
        """
        It restores the number of uses of the die
        :param numUses: the new numeric value for the number of uses allowed
        """
        self.numUses = numUses

    def getLetter(self):
        """
        Converts the numeric value received as parameter to the letter in the die
        :returns the numeric value for this die's value or 'E' if it has no value
        """
        return Die.LETTERS.get(self.val, 'E')

    def hide(self):
        """
        Hides the die's value from the __players
        """
        self.hidden = True

    def show(self):
        """
        Shows the die's value to the __players
        """
        self.hidden = False

    def reset(self):
        """
        Resets this die to None
        """
        self = None

    def test(self):
        """
        Tests this die
        """
        if self.val and self.val not in Die.FACES:
            raise ValueError('Die value out of bounds: {}'.format(self.val))

    # SORTING FUNCTIONS
    @compFunc
    def __eq__(self, other):
        """
        When using the operator (==), compares if this die's value is equal to another one
        :param other: the other die to compare with
        """
        return self.val == other.val

    @compFunc
    def __ne__(self, other):
        """
        When using the operator (!=), compares if this die's value is different to another one
        :param other: the other die to compare with
        """
        return not self.__eq__(other)

    @compFunc
    def __ge__(self, other):
        """
        When using the operator (>=), compares if this die's value is greater or equal than another one
        :param other: the other die to compare with
        """
        return self.val >= other.val

    @compFunc
    def __gt__(self, other):
        """
        When using the operator (>), compares if this die's value is greater than another one
        :param other: the other die to compare with
        """
        return self.val > other.val

    @compFunc
    def __le__(self, other):
        """
        When using the operator (<=), compares if this die's value is less than another one
        :param other: the other die to compare with
        """
        return self.val <= other.val

    @compFunc
    def __lt__(self, other):
        """
        When using the operator (<), compares if this die's value is less than another one
        :param other: the other die to compare with
        """
        return self.val < other.val

    def __repr__(self, *args, **kwargs):
        """
        Unambiguous string representation for this object,
        useful for logging or debugging purposes
        """
        return '{0!s}{1}'.format(self.val or '_', '?' if self.hidden else '')

    def __str__(self, *args, **kwargs):
        """
        Nice representation for this object,
        useful for showing in the app
        """
        return (self.getLetter() if self.val and not self.hidden else '?')


if __name__ == "__main__":
    print(Die())
    print(Die(hide=False))
    print(Die(throw=False))
    print(Die(throw=False, hide=False))
    print(Die(3))
    print(Die(4, hide=False))
    print(Die(5, False))
    print(Die(6, False, hide=False))
    print(Die(6, False, False))
    dice = [Die() for _ in range(5)]
    print('dice = {0!r}'.format([str(d) for d in dice]))
    print('dice = {0!r}'.format([repr(d) for d in dice]))
    dice.sort()
    print('sorted dice = {0!r}'.format([str(d) for d in dice]))
    print('sorted dice = {0!r}'.format([repr(d) for d in dice]))
    print('lying dice = {0!r}'.format([repr(d.lie()) for d in dice]))
