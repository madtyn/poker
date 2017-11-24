

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
        """
        Returns the current player
        :return: the current player
        """
        return self.__players.currentPlayer()

    def prevPlayer(self):
        """
        Returns the previous player to the current one
        :return: the previous player
        """
        return self.__players.previousPlayer()

    def next_player(self):
        """
        Returns the next player to the current one
        :return: the next player
        """
        return self.__players.next_player()

    def change_player(self):
        """

        :return:
        """
        self.__players.forwardCurrentPlayer()
        return self.__players.currentPlayer()

    def winner(self):
        """
        Returns the winner player, if any, otherwise None
        :return: the winner player
        """
        if len(self.__players) == 1:
            return self.__players.currentPlayer()

    def surrenders(self, player):
        """
        Called for doing the needed operations for surrender
        :param player: the player
        """
        self.__players.surrenders(player)
        return player

    def loses(self, player):
        """
        Called for doing the needed operations for losing
        :param player: the player
        """
        self.__players.loses(player)
        return player
