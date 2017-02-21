from martintc.poker.model.singleton import Singleton
from fractions import Fraction
import wrapt
'''
Created on 18 feb. 2017

@author: madtyn
'''

@wrapt.decorator
def compFunc(wrapped, instance, args, kwargs):
    other = args[0]
    if instance.__class__ is other.__class__:
        return wrapped(other)
    return NotImplemented

# Make this a Singleton?
class Utils(object):
    '''
    Class with useful functions
    '''
    
    @staticmethod
    def fact(i, current_factorial=1):
        '''
        The factorial function
        :param i: the number for calculating the factorial
        :param current_factorial: the acumulated product
        '''
        if i == 1:
            return current_factorial
        else:
            return Utils.fact(i - 1, current_factorial * i)
    
    @staticmethod
    def reverseDict(dic):
        '''
        Returns a reversed dict switching keys with values.
        Example:
            reverseDict({k1:v1, k2:v2,...}) == {v1:k1, v2:k2, ...}
        :param dic: thedict to reverse
        '''
        return dict([(v,k) for (k,v) in dic.items()])
    
    @staticmethod
    def C(n, r=1):
        '''
        Statistical combinations
        :param n: number of elements to be combined
        :param r: number of elements to be taken for each combination
        '''
        return Utils.fact(n) / (Utils.fact(r) * Utils.fact(n-r))
    
    @staticmethod
    def prob(numberEqualDice, numberDiceToThrow, numValidFaces):
        '''
        # C(ndadosatirar, n? dadosnecesitados)* (1/6)^(n? de dados necesitados)
        # * (n caras validas)
        # C(nDadosaTirar, n dadosnecesitados)*
        # [6^(ndadosSobrantes)/6^(ndadosaTirar)]* (n caras validas)
        # return Math.pow((double)1/6,
        # numberEqualDice)*numValidFaces*(factorial(numberDiceToThrow)/(factorial(numberDiceToThrow-numberEqualDice)*factorial(numberEqualDice)));
        
        :param numberEqualDice:
        :param numberDiceToThrow:
        :param numValidFaces:
        '''
        # TODO martintc Revisar especificamente todo el asunto matematico
        # With fraction use float(f) for a percentage
        f1_6 = Fraction(1,6)
        f5_6 = Fraction(5,6)
        return numValidFaces * (
            ( ( f1_6 ** numberEqualDice) 
              * (f5_6 ** (numberDiceToThrow - numberEqualDice)) 
              * (Utils.C(numberDiceToThrow, numberEqualDice) - 1)) 
                + ( f1_6 ** numberEqualDice))

if __name__ == "__main__":
    print(Utils.fact(6))
