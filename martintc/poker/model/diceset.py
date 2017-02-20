from martintc.poker.model.die import Die
from collections import Counter
from martintc.poker.model.pokerhand import Hand

'''
Created on 18 feb. 2017

@author: madtyn
'''

class DiceSet(object):
    '''
    This class represents a specific move from one player
    gathering the values from different dice to sum up an only value
    for the whole move.
    '''

    def __init__(self, throw=True, length=5):
        '''
        Constructor
        
        :param throw: if True generates a random diceset by throwing all its dice
        :param length: the length of the diceset, 5 by default
        '''
        if throw:
            self.dice = [Die(throw=throw) for _ in range(length)]
            self.dice.sort()
        else:
            self.dice = []

    def sort(self):
        '''
        Sorts the dice from left to right, minor values to max ones 
        '''
        self.dice.sort()
        
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
        
    def test(self):
        '''
        Tests the dice
        '''
        for die in self.dice:
            die.test()
            
    # SORTING FUNCTIONS 
    def __eq__(self, other):
        '''
        When using the operator (==), compares if this diceset is equal to another one
        :param other: the other diceset to compare with
        '''
        return self.hand() == other.hand() and self.__cmp__(other) == 0

    def __cmp__(self, other):
        '''
        Compares two diceset looking at its dice's faces/points
        :param other: the other object to compare with
        '''
        l1 = list(self.frequencies().items())
        l1= sorted(l1, key=itemgetter(1,0), reverse=True)
        
        l2 = list(other.frequencies().items())
        l2= sorted(l2, key=itemgetter(1,0), reverse=True)
        
        for x,y in zip(l1, l2):
            if x[1] < y[1]:
                return -1
            elif x[1] > y[1]:
                return 1
            elif x[0] < y[0]:
                return -1
            elif x[0] > y[0]:
                return 1
                
        return 0
    
    def __ne__(self, other):
        '''
        When using the operator (!=), compares if this diceset is different to another one
        :param other: the other diceset to compare with
        '''
        return not self.__eq__(other)
    
    def __ge__(self, other):
        '''
        When using the operator (>=), compares if this diceset is greater or equal than another one
        :param other: the other diceset to compare with
        '''
        if self.hand() == other.hand():
            return self.__cmp__(other) >= 0
        else:
            return self.hand() >= other.hand()
    
    def __gt__(self, other):
        '''
        When using the operator (>), compares if this diceset is greater than another one
        :param other: the other diceset to compare with
        '''
        if self.hand() == other.hand():
            return self.__cmp__(other) > 0
        else:
            return self.hand() > other.hand()
    
    def __le__(self, other):
        '''
        When using the operator (<=), compares if this diceset is less than another one
        :param other: the other diceset to compare with
        '''
        if self.hand() == other.hand():
            return self.__cmp__(other) <= 0
        else:
            return self.hand() <= other.hand()

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
        TODO Will return the name of dice of this combination, but I don't know yet
        if count the number of elements in self.dice or counting the 
        all the elements not being None.
        Many times this will be 5, but for calculating some probabilities
        it could be useful having less or more elements
        '''
        return len(self.dice)
    
    def __repr__(self, *args, **kwargs):
        '''
        Unambiguous string representation for this object, 
        useful for logging or debugging purposes
        '''
        return '[{}]'.format(','.join([str(die.val) for die in self.dice]) )
    
    def __str__(self, *args, **kwargs):
        '''
        Nice representation for this object, useful for
        showing in the app
        '''
        freqs={}
        for k,v in self.frequencies(letter=True).items():
            freqs[k] = v
        return '{} {}'.format(self.hand().name, freqs)

if __name__ == "__main__":
    dicesets = [DiceSet() for _ in range(1000)]
    dicesets = [d for d in dicesets if d.hand() >= Hand.FOUR_OF_KIND]
    for d in dicesets:
        print('{!r} '.format(d))
    
    from operator import itemgetter
    for i in range(len(dicesets)-1):
        x = dicesets[i]
        y = dicesets[i+1]
        if x == y:
            print('{} == {}'.format(x, y))
        elif x > y:
            print('{} > {}'.format(x, y))
        else:
            print('{} < {}'.format(x, y))
        
    