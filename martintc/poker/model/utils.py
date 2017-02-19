from martintc.poker.model.singleton import Singleton
from fractions import Fraction
'''
Created on 18 feb. 2017

@author: madtyn
'''

class Utils(object, metaclass=Singleton):
    '''
    Class with math functions
    '''
    @staticmethod
    def fact(i, current_factorial=1):
        if i == 1:
            return current_factorial
        else:
            return Utils.fact(i - 1, current_factorial * i)
    
    @staticmethod
    def C(n, r=1):
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
