'''
Created on 19 feb. 2017

@author: madtyn
'''
from enum import Enum
class Hand(Enum):
    '''
    This will represent a hand in the game. Useful for comparisons
    '''
    NOTHING = (0,[1,1,1,1,1])
    PAIR = (1,[2,1,1,1])
    DOUBLE_PAIR = (2,[2,2,1])
    THREE_OF_KIND = (3,[3,1,1])
    FULL_HOUSE = (4,[3,2])
    FOUR_OF_KIND = (5,[4,1])
    FIVE_OF_KIND = (6,[5])
    
    def __init__(self, val, struct):
        '''
        Constructor
        :param val: the value for ordering and comparing hands
        :param struct: the list with the frequencies
        '''
        self.val = val
        self.struct = struct
        
    def __eq__(self, other):
        '''
        When using the operator (==), compares if this hand's value is equal to another one
        :param other: the other hand to compare with
        '''
        if self.__class__ is other.__class__:
            return self.val == other.val
    
    def __ne__(self,other):
        '''
        When using the operator (!=), compares if this hand's value is different to another one
        :param other: the other hand to compare with
        '''
        return not self.__eq__(other)
    
    def __ge__(self, other):
        '''
        When using the operator (>=), compares if this hand's value is greater or equal than another one
        :param other: the other hand to compare with
        '''
        if self.__class__ is other.__class__:
            return self.val >= other.val
        return NotImplemented
    
    def __gt__(self, other):
        '''
        When using the operator (>), compares if this hand's value is greater than another one
        :param other: the other hand to compare with
        '''
        if self.__class__ is other.__class__:
            return self.val > other.val
        return NotImplemented
    
    def __le__(self, other):
        '''
        When using the operator (<=), compares if this hand's value is less than another one
        :param other: the other hand to compare with
        '''
        if self.__class__ is other.__class__:
            return self.val <= other.val
        return NotImplemented
    
    def __lt__(self, other):
        '''
        When using the operator (<), compares if this hand's value is less than another one
        :param other: the other hand to compare with
        '''
        if self.__class__ is other.__class__:
            return self.val < other.val
        return NotImplemented
    
    def __str__(self):
        '''
        Nice representation for this object, 
        useful for showing in the app
        '''
        return self.name
    
    @classmethod
    def getHand(cls, struct):
        '''
        Gets the hand from a sorted list with the number of equal faces
        Example:
            Hand.getHand([4,1]) == Hand.FOUR_OF_KIND
            Hand.getHand([3,2]) == Hand.FULL_HOUSE
        :param cls: the class (Hand)
        :param struct: the list with th number of equal faces, from the greatest to the smallest
        '''
        if sum(struct) == 5:
            for hand in cls:
                if hand.struct == struct:
                    return hand
        else:
            for hand in cls:
                #Lists are sorted
                # We compare element by element (only as much as the shortest list)
                equalElements = [x==y for x,y in zip(struct, hand.struct)]
                if False not in equalElements:
                    return hand
        return cls.NOTHING

if __name__ == "__main__":
    for x in Hand:
        for y in Hand:
            print('{h.name} whose value is {h.value} and val is {h.val}'.format(h=x))
            print('{h.name} whose value is {h.value} and val is {h.val}'.format(h=y))
            if x == y:
                print('{} == {}'.format(x.name, y.name))
            elif x > y:
                print('{} > {}'.format(x.name, y.name))
            else:
                print('{} < {}'.format(x.name, y.name))