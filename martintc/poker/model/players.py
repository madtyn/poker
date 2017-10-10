import logging


class Loggable(object):
    def __init__(self) -> None:
        super().__init__()
        print(self.get_class())

    def get_class(self):
        return self.__class__.__name__


class Players(Loggable):
    def __init__(self, players) -> None:
        super().__init__()
        print(__class__.__name__)
        self._logger = logging.getLogger(__class__.__name__)
        self._players = []
        self._players = players[:]
        self._current_player_idx = 0

    def _index(self, idx):
        return idx % len(self._players)

    def _nextIndex(self):
        return self._index(self._current_player_idx + 1)

    def _previousIndex(self):
        return self._index(self._current_player_idx - 1)

    def nextPlayer(self):
        return self._players[self._nextIndex()]

    def previousPlayer(self):
        return self._players[self._previousIndex()]

    def forwardCurrentPlayer(self):
        self._current_player_idx = self._nextIndex()
        return self.currentPlayer()

    def currentPlayer(self):
        return self._players[self._current_player_idx]

    def registerPlayer(self, player):
        self._players.append(player)

    def removePlayer(self, player):
        try:
            self._players.remove(player)
        except ValueError:
            self._logger.error("Player {} didn't exist in the list".format(player.name))

    def __repr__(self):
        return '[{}]'.format(', '.join([p.name for p in self._players]))


class Player(Loggable):
    def __init__(self, name, lives=5) -> None:
        super().__init__()
        print(__class__.__name__)
        self._logger = logging.getLogger(__class__.__name__)
        self.name = name
        self.lives = lives

    def __repr__(self):
        return self.name


if __name__ == '__main__':
    p1 = Player('Matt')
    p2 = Player('Kevin')
    p3 = Player('John')
    p4 = Player('Alice')
    ps = Players([p1, p2, p3, p4])
    print(ps)
    print('Current player is {}'.format(ps.currentPlayer()))
    print('Next player is {}'.format(ps.nextPlayer()))
    print('Prev player is {}'.format(ps.previousPlayer()))
    ps.forwardCurrentPlayer()
    print('Current player is {}'.format(ps.currentPlayer()))

