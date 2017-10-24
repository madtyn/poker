

# TODO Should be a singleton
class Status(object):
    """
    Represents the current status of the game.
    This should have all the info required for saving  the game
    and restoring it later.
    """
    def __init__(self, players) -> None:
        super().__init__()
        self.__players = players

    @property
    def players(self):
        return self.__players

    @players.setter
    def set_players(self, players):
        self.__players = players

    def current_player(self):
        return self.__players.currentPlayer()

    def prevPlayer(self):
        """
        Returns the previous player to the current one
        :return: the previous player
        """
        return self.__players.previousPlayer()

    def nextPlayer(self):
        """
        Returns the next player to the current one
        :return: the next player
        """
        return self.__players.next_player()

    def changePlayer(self):
        self.__players.forwardCurrentPlayer()
        return self.__players.currentPlayer()

    def winner(self):
        if len(self.__players) == 1:
            return self.__players.currentPlayer()

    def surrenders(self, player):
        self.__players.surrenders(player)

    def loses(self, player):
        self.__players.loses(player)