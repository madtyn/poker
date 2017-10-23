'''
Created on 18 feb. 2017

@author: madtyn
'''


class Borg1:
    """
        Allow different instances sharing the same identical state
        So:
            a = Borg()
            b = Borg()
            a == b  # True. Also if you change one, you change the other one
        """
    _shared_state= {}

    def __new__(cls, *args, **kwargs):
        obj = super(Borg1, cls).__new__(cls)
        obj.__dict__ = cls._shared_state
        return obj

    def __init__(self, q=1, w=2):
        self.q = q
        self.w = w


class Borg2(object):
    """
    Allow different instances sharing the same identical state
    So:
        a = Borg()
        b = Borg()
        a == b  # True. Also if you change one, you change the other one
    """
    __shared_state = {}

    def __init__(self, q=4, w=5):
        self.__dict__ = self.__shared_state
        self.q = q
        self.w = w
        # and whatever else you want in your class -- that's all!


class Singleton(type):
    """
    Singleton metaclass

    You can make Singleton classes by declaring them in this way:

    class Logger(metaclass=Singleton):
        pass # Or whatever
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


if __name__ == '__main__':
    class S(object, metaclass=Singleton):
        def __init__(self, x):
            self.x = x

        def __repr__(self):
            return str(self.x)

    value = 15
    print('s1 = S({})'.format(value))
    s1 = S(value)
    print('s1 is {}'.format(s1))
    value = -88
    print('s2 = S({})'.format(value))
    s2 = S(value)
    print('s1 is {}'.format(s1))
    print('s2 is {}'.format(s2))
    value = 31
    print('s2.x = {}'.format(value))
    s2.x = 31
    print('s1 is {}'.format(s1))
    print('s2 is {}'.format(s2))


    print('Borg implementations comparison:\n')
    class A(Borg1):
        def __init__(self, q=-1, w=-2, e=-8):
            self.e = e
            super().__init__(q,w)

        def __repr__(self):
            return 'q={}, w={}, e={}'.format(self.q,self.w,self.e)

    class B(Borg1):
        def __init__(self, q=-10, w=-20, e=-80):
            self.e = e
            super().__init__(q, w)

        def __repr__(self):
            return 'q={}, w={}, e={}'.format(self.q,self.w,self.e)

    clazz = A

    x = clazz()
    print(x)
    y = clazz(7)
    print(y)
    z = clazz(11,22)
    print(z)
    g = clazz(55,66,77)
    print(g)
    x.q = 1
    y.w = 1
    z.e = 1
    print(x)
    print(y)
    print(z)
    print(g)

    print('-------------------')

    clazz = B

    x = clazz()
    print(x)
    y = clazz(7)
    print(y)
    z = clazz(11, 22)
    print(z)
    g = clazz(55, 66, 77)
    print(g)
    x.q = 1
    y.w = 1
    z.e = 1
    print(x)
    print(y)
    print(z)
    print(g)