import sys
import random as rnd
import logging
from abc import abstractmethod

from martintc.poker.view.ui import output


class Loggable(object):
    """
    Class mixin for provide logging functions to any chid class
    """
    def __init__(self) -> None:
        super().__init__()
        self.__logger = None
        self.__logger = self.get_logger()
        # print(self.get_class())

        self.debug = self.get_logger().debug
        self.error = self.get_logger().error
        self.critical = self.get_logger().critical
        self.info = self.get_logger().info
        self.warn = self.get_logger().warning

    def get_logger(self):
        """
        Gets the logger for this class
        :return: the logger
        """
        if not self.__logger:
            self.__logger = logging.getLogger(self.get_class())
        return self.__logger

    def get_class(self):
        """
        Gets the class name for this class.
        Even when this method is inherited, the class name returned is the correct one.
        :return: the caller's class name
        """
        return self.__class__.__name__


class Player(Loggable):
    """
    Handles the player related info and functions
    """
    def __init__(self, name, lives=5) -> None:
        super().__init__()
        self.status = None

        self.name = name
        self.lives = lives

    @abstractmethod
    def accepts(self) -> bool:
        """
        Returns if the player accepted to surpass
        :return: True if accepted, False otherwise
        """
        raise NotImplementedError

    @abstractmethod
    def decide_to_lie(self, minimum=None, actualDiceset=None):
        """
        Decides if the player's going to lie or not
        :return: True if the player is going to lie, False if not
        """
        # TODO This decision should be complex, it should be different for machines and human players
        # TODO In computer players, this should involve:
        # 1.- Firstly and IMPORTANT, if it's possible to lie with the visible dice
        # 2.- If the actual dice the player knows for sure are higher than needed, it should be PROBABLY false
        # 3.- If the actual dice are not enough for overpassing, the harder it is to overpass, the more PROBABLY is the lie
        # TODO In humans, this just should ask for confirmation to lie
        raise NotImplementedError

    def __eq__(self, o: object) -> bool:
        return self.__class__ == o.__class__ \
               and (self is o or self.name == o.name)

    def __repr__(self):
        return self.name


class Robot(Player):
    def accepts(self) -> bool:
        # TODO in computer __players, they must decide depending on the shown dice
        return rnd.choice([True, False])

    def surrender(self):
        """
        The player surrenders
        """
        # TODO We should decide if this method is needed
        # return rnd.choice([True, False])
        pass

    def decide_to_lie(self, minimum=None, actualDiceset=None):
        """
        Decides if the player's going to lie or not
        :return: True if the player is going to lie, False if not
        """
        # TODO In computer players, this should involve:
        # 1.- Firstly and IMPORTANT, if it's possible to lie with the visible dice
        # 2.- If the actual dice the player knows for sure are higher than needed, it should be PROBABLY false
        # 3.- If the actual dice are not enough for overpassing, the harder it is to overpass, the more PROBABLY is the lie
        if actualDiceset < minimum:
            return True
        else:
            return rnd.choice([True, False])


class Human(Player):
    def accepts(self) -> bool:
        # TODO In human players this asks for believing or not the play hand offered
        return rnd.choice([True, False])

    def decide_to_lie(self, minimum=None, actualDiceset=None):
        """
        Decides if the player's going to lie or not
        :return: True if the player is going to lie, False if not
        """
        # TODO In humans, this just should ask for confirmation to lie
        return rnd.choice([True, False])


class Players(Loggable):
    """
    Handles the players functions, like the current player
    or moving to the next player
    """
    def __init__(self, players) -> None:
        super().__init__()
        self._players = []
        self._players = players[:]
        self._current_player_idx = 0

    def _index(self, idx) -> int:
        """
        Returns (the introduced index % the length of players)
        :rtype: the position index in the list
        """
        return idx % len(self._players)

    def _player_index(self, player):
        return self._players.index(player)

    def _previous_index(self):
        """
        Returns the position index in the list
        for the previous element to the current one
        :rtype: the position index in the list
        """
        return self._index(self._current_player_idx - 1)

    def _next_index(self):
        """
        Returns the position index in the list
        for the next element to the current one
        :rtype: the position index in the list
        """
        return self._index(self._current_player_idx + 1)

    def previousPlayer(self):
        """
        Returns the previous player to the current one
        :return: the previous player
        """
        return self._players[self._previous_index()]

    def next_player(self, player=None):
        """
        Returns the next player to the current one
        :return: the next player
        """
        if not player:
            return self._players[self._next_index()]
        else:
            return self._players[self._next_index(self._player_index(player))]

    def forwardCurrentPlayer(self):
        """
        Moves the current player to the next one and returns it
        :return: the new current player
        """
        self._current_player_idx = self._next_index()
        return self.currentPlayer()

    def currentPlayer(self):
        """
        Returns the current player
        :return: the current player
        """
        return self._players[self._current_player_idx]

    def registerPlayer(self, player):
        self._players.append(player)

    def removePlayer(self, player):
        try:
            self._players.remove(player)
        except ValueError:
            self.get_logger().error("Player {} didn't exist in the list".format(player.name))

    def surrenders(self, player):
        output(_('Player {0.name} surrenders!').format(player))
        self.loses(player)

    def loses(self, player):
        player.lives -= 1
        if player.lives <= 0:
            output(_('Player {0.name} is out of the game!').format(player))
            # We update the current player to the loser, so when removed, the next one becomes automatically the current
            self._current_player_idx = self._index(self._player_index(player))
            self.removePlayer(player)
            # In case it was the last position, we apply the modulus (%) with the length of players
            self._current_player_idx = self._index(self._current_player_idx)

    def __len__(self) -> int:
        """
        Returns the number of active __players who
        didn't lose yet
        :return: the number of __players
        """
        return len(self._players)

    def __repr__(self):
        return '[{}]'.format(', '.join([p.name for p in self._players]))


if __name__ == '__main__':
    from martintc.poker.view.languages import selectLanguage
    lang = selectLanguage(1)

    if lang:
        lang.install()  # Makes _() available as builtin
    p1 = Player('Matt', lives=1)
    p2 = Player('Kevin', lives=1)
    p3 = Player('John', lives=1)
    p4 = Player('Alice', lives=1)
    ps = Players([p1, p2, p3, p4])
    print(ps)
    print('Prev player is {}'.format(ps.previousPlayer()))
    print('Current player is {}'.format(ps.currentPlayer()))
    print('Next player is {}'.format(ps.next_player()))
    ps.forwardCurrentPlayer()
    print()
    print('Prev player is {}'.format(ps.previousPlayer()))
    print('Current player is {}'.format(ps.currentPlayer()))
    print('Next player is {}'.format(ps.next_player()))
    ps.loses(p4)
    print('Prev player is {}'.format(ps.previousPlayer()))
    print('Current player is {}'.format(ps.currentPlayer()))
    print('Next player is {}'.format(ps.next_player()))

