'''
Created on 18 feb. 2017

@author: madtyn
'''

class Singleton(type):
    '''
    Singleton metaclass
    
    You can make Singleton classes by declaring them in this way:
    
    class Logger(metaclass=Singleton):
        pass # Or whatever
    '''

    def __init__(self):
        '''
        Constructor
        '''
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
