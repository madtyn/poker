import random
from martintc.poker.model.utils import Utils

'''
Created on 18 feb. 2017

@author: madtyn
'''

class Die(object):
    '''
    This is the class which will simulate a die.
    It can hold a value. It can be hidden or not. Etc...
    '''
    # This makes the number to letter conversion
    LETTERS = {1:'N', 2:'R', 3:'J', 4:'Q', 5:'K', 6:'A'}
    
    # The inverse dict, for reverse conversion (letter to number)
    NUMBERS = Utils.reverseDict(LETTERS)
    
    # FACES = [1,2,3,4,5,6]
    FACES = sorted(LETTERS.keys())

    def __init__(self, value=None, throw=True, hide=True):
        '''
        Constructor
        
        :param throw: if True, it assigns a random value to this Die
        :param hide: if True, it hides this die and sets its hidden status to True
        :param value: 
        '''
        if value:
            self.val = value
        elif throw:
            self.throw()
        else:
            self.val = None
        self.hidden = hide
        
    def throw(self):
        '''
        Generates a random number from the list [1,2,3,4,5,6]
        '''
        self.val = random.choice(Die.FACES) 
        return self.val
    
    def getLetter(self):
        '''
        Converts the numeric value received as parameter to the letter in the die
        '''
        return Die.LETTERS.get(self.val, 'E')
    
    def hide(self):
        '''
        Hides the die's value from the players
        '''
        self.hidden = True
    
    def show(self):
        '''
        Shows the die's value to the players
        '''
        self.hidden = False
    
    def test(self):
        if self.val and self.val not in Die.FACES:
            raise ValueError('Die value out of bounds: {}'.fomat(self.val))
        
    # SORTING FUNCTIONS 
    def __eq__(self, other):
        '''
        When using the operator (==), compares if this die's value is equal to another one
        :param other: the other die to compare with
        '''
        return self.val == other.val
    
    def __ne__(self, other):
        '''
        When using the operator (!=), compares if this die's value is different to another one
        :param other: the other die to compare with
        '''
        return not self.__eq__(other)
    
    def __ge__(self, other):
        '''
        When using the operator (>=), compares if this die's value is greater or equal than another one
        :param other: the other die to compare with
        '''
        return self.val >= other.val
    
    def __gt__(self, other):
        '''
        When using the operator (>), compares if this die's value is greater than another one
        :param other: the other die to compare with
        '''
        return self.val > other.val
    
    def __le__(self, other):
        '''
        When using the operator (<=), compares if this die's value is less than another one
        :param other: the other die to compare with
        '''
        return self.val <= other.val

    def __lt__(self, other):
        '''
        When using the operator (<), compares if this die's value is less than another one
        :param other: the other die to compare with
        '''
        return self.val < other.val
    
    def __repr__(self, *args, **kwargs):
        '''
        Unambiguous string representation for this object, 
        useful for logging or debugging purposes
        '''
        return '{0!s}'.format(self.val)
    
    def __str__(self, *args, **kwargs):
        '''
        Nice representation for this object, 
        useful for showing in the app
        '''
        return self.getLetter()

if __name__ == "__main__":
    dice = [Die() for _ in range(5)]
    print('dice = {0!r}'.format([str(d) for d in dice]))
    dice.sort()
    print('sorted dice = {0!r}'.format([str(d) for d in dice]))