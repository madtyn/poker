from enum import Enum
'''
Created on 19 feb. 2017

@author: madtyn
'''
class Hand(Enum):
    NOTHING = (0,[1,1,1,1,1])
    PAIR = (1,[2,1,1,1])
    DOUBLE_PAIR = (2,[2,2,1])
    THREE_OF_KIND = (3,[3,1,1])
    FULL_HOUSE = (4,[3,2])
    FOUR_OF_KIND = (5,[4,1])
    FIVE_OF_KIND = (6,[5])
    
    def __init__(self, val, struct):
        self.val = val
        self.struct = struct
        
    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented
    
    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented
    
    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented
    
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented
    
    def __str__(self):
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
        for hand in cls:
            if hand.struct == struct:
                return hand
        return cls.NOTHING

if __name__ == "__main__":
    for x in []:
        for y in Hand:
            if x == y:
                print('{} == {}'.format(x.name, y.name))
            elif x > y:
                print('{} > {}'.format(x.name, y.name))
            else:
                print('{} < {}'.format(x.name, y.name))