import wrapt

from fractions import Fraction
from math import factorial as fact
from functools import reduce
from operator import mul

'''
Created on 18 feb. 2017

@author: madtyn
'''

@wrapt.decorator
def compFunc(wrapped, instance, args, kwargs):
    """
    Decorator operator overloading functions.
    Checks if the two instances involved in the operation are from the same class.
    :param wrapped: the decorated or wrapped function
    :param instance: the actual instance of the wrapped function being invoked
    :param args: the args
    :param kwargs: the kwargs
    :return: NotImplemented if the instances can't be operated, else None
    """
    # TODO We could improve this by checking if it's assignable from one another
    #     or inheriting the same hierarchy
    other = args[0]
    if instance.__class__ is other.__class__:
        return wrapped(other)
    return NotImplemented


def reverseDict(dic):
    '''
    Returns a reversed dict switching keys with values.
    Example:
        reverseDict({k1:v1, k2:v2,...}) == {v1:k1, v2:k2, ...}
    :param dic: the dict to reverse
    '''
    return dict([(v, k) for (k, v) in dic.items()])

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
    f1_6 = Fraction(1, 6)
    f5_6 = Fraction(5, 6)
    return numValidFaces * (
        ((f1_6 ** numberEqualDice)
         * (f5_6 ** (numberDiceToThrow - numberEqualDice))
         * (C(numberDiceToThrow, numberEqualDice) - 1))
        + (f1_6 ** numberEqualDice)
    )

def C(n, k=1):
    '''
    Statistical combinations 'nCk'
    :param n: number of elements to be combined
    :param k: number of elements to be taken for each combination
    :return: the 'n choose k' mathematical result
    '''
    '''
        Original formula: fact(n) / (fact(k) * fact(n-k))
        
        Performance shortcut (about 40% faster): 
            1.- Calculates the numerator as the product over the first k-th elements of fact(n)
            Let's call this f'(n,k)
            Example:
                n = 6, k = 2 => f'(n,k) =   30 = 6 · 5
                n = 6, k = 3 => f'(n,k) =  120 = 6 · 5 · 4
                n = 9, k = 4 => f'(n,k) = 3024 = 9 · 8 · 7 · 6
            2.- Then divide it by fact(k)
        
        New formula: f'(n,k) / fact(k)
        
        '''
    k = n - k if k > (n // 2) else k
    fnkProduct = reduce(mul, range(n, n - k, -1), 1)
    return fnkProduct // fact(k)

if __name__ == "__main__":
    print('C(997, 4) = {}'.format(C(997, 4)))
    print('C(8,4) == 70? => {}'.format(C(8, 4)))  # Should be 70
    print('C(50000,4) is {}'.format(C(50000, 4))) # No precission