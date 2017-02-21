from itertools import product, repeat
from fractions import Fraction
from martintc.poker.model.die import Die
from collections import Counter
from martintc.poker.model.pokerhand import Hand
from operator import itemgetter
from martintc.poker.model.utils import compFunc

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

    def __init__(self, inp=[], throw=True, length=5):
        '''
        Constructor
        
        :param throw: if True generates a random diceset by throwing all its dice
        :param length: the length of the diceset, 5 by default
        '''
        if inp:
            self.dice = [Die(number) for number in inp[:length]]
        elif throw:
            self.dice = [Die(throw=throw) for _ in range(length)]
        else:
            self.dice = []
        self.dice.sort()

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
    
    def surpassProb(self, n=None):
        '''
        Calculates the exact probabiity for surpassing this diceset's value
        '''
        favorableCases = 0
        cases = 0
        '''
        We obtain as many times FACES(=[NRJQKA]) as number of dice (=n) in this diceset.
        For n=5 dice, it would be 5 lists [NRJQKA], [NRJQKA],...x2..., [NRJQKA]
        
        Then we do a cartesian product 
        (with FACESxFACES it would get all pairs (N,N) (N,R)..(N,A), (R,N),..,(A,A) )
        (with FACESxFACESxFACES it would get all tuples (N,N,N) (N,N,R)..(N,N,A),..,(N,A,A),(R,N,N),..,(A,A,A) )
        
        So we have now all cases ready for being converted to list and used
        
        '''
        if not n:
            n = len(self.dice)
        n_FACES = repeat(Die.FACES, n)
        allCases = [list(elem) for elem in product(*n_FACES )]
        for case in allCases:
            cases += 1
            x=DiceSet(inp=case)
            if x >  self:
                print(x)
                favorableCases += 1
        
        return Fraction(favorableCases,cases)
        
    def test(self):
        '''
        Tests the dice
        '''
        for die in self.dice:
            die.test()
    
    #OPERATOR FUNCTIONS
    def __add__(self, other):
        '''
        Returns a new diceset as the addition between dicesets, which would be:
        
        [1,1] + [3,4] == [1,1,3,4]
        [N,N] + [J,Q] == [N,N,J,Q]
        
        :param other: the other diceset
        '''
        d = DiceSet(inp=self.dice + other.dice)
        return d
    
    def __sub__(self, other):
        '''
        Returns a new diceset with these dice and with the dice in other removed
        
        [1,1,3,3,4] - [1,3,4] == [1,3,4]
        
        :param other: the other diceset
        '''
        _dice = self.dice[:]
        for d in other.diceset: 
            _dice.remove(d)
        ds = DiceSet(inp=_dice)
        return ds
    
    def __truediv__(self, other):
        '''
        Returns a new diceset with these dice and all the dice in other removed
        
        [1,1,3,3,4] / [1,3,4] == []
        
        :param other: the other diceset
        '''
        ds = DiceSet(inp=[d for d in self.dice if d not in other.dice])
        return ds

    def __mul__(self, other):
        '''
        Returns a new diceset 

        [1,2] * 3  == [1,2,1,2,1,2]
                       1   2   3        

        :param other: an integer
        '''
        if type(other) is int:
            d = DiceSet(inp=self.dice * other)
            return d
        else:
            return NotImplemented

    # SORTING FUNCTIONS
    @compFunc 
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
    # Constructor testing
    print('{!r}'.format(DiceSet()))
    print('{!r}'.format(DiceSet(length=3)))
    print('{!r}'.format(DiceSet(throw=False)))
    print('{!r}'.format(DiceSet(throw=False, length=2)))
    print('{!r}'.format(DiceSet([2,3,3,6])))
    print('{!r}'.format(DiceSet([5,5,5,4,4], length=4)))
    print('{!r}'.format(DiceSet([2,2,2,6,6], False)))
    print('{!r}'.format(DiceSet([1,1,1,4,4], False, 4)))
    print(DiceSet(inp=[4,4]).surpassProb())
    diceset = DiceSet([6,6,6,5,5])
    print(diceset)
    
    #Comparison testing
    dicesets = [DiceSet() for _ in range(10)]
    dicesets = [d for d in dicesets if d.hand() > Hand.PAIR]
    for d in dicesets:
        print('{!r} '.format(d))
    
    for i in range(len(dicesets)-1):
        x = dicesets[i]
        y = dicesets[i+1]
        if x == y:
            print('{} == {}'.format(x, y))
        elif x > y:
            print('{} > {}'.format(x, y))
        else:
            print('{} < {}'.format(x, y))
       
    