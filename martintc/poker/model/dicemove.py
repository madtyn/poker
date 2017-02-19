from martintc.poker.model.die import Die
from collections import Counter
from martintc.poker.model.pokerhand import Hand

'''
Created on 18 feb. 2017

@author: madtyn
'''

class DiceMove(object):
    '''
    This class represents a specific move from one player
    gathering the values from different dice to sum up an only value
    for the whole move.
    '''

    def __init__(self, throw=True, length=5):
        '''
        Constructor
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
        numberEqualFaces = sorted(list(dice.frequencies().values()), reverse=True)
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
            
    def __len__(self):
        '''
        TODO
        Will return the name of dice of this combination, but I don't know yet
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
        for k,v in self.frequencies().items():
            freqs[]
        # TODO It depends on the value function
        return '{} []'.format(self.hand().name)

if __name__ == "__main__":
    for _ in range(1000):
        dice = DiceMove()
        if dice.hand() >= Hand.FIVE_OF_KIND:
            print('{!r} is the hand {}'.format(dice, dice.hand()))
    print('dice = 0!r'.format(dice))
    dice.sort()
    print('sorted dice = 0!r'.format(dice))
