class Status(object):
    def __init__(self, players) -> None:
        super().__init__()
        self.players
        self.__currentPlayer = None
        if len(players):
            self.__currentPlayer = 0

    def prevPlayer(self):
        return self.players[self.__playerIndex(self.__currentPlayer - 1)]

    def nextPlayer(self):
        return self.players[self.__playerIndex(self.__currentPlayer + 1)]

    def changePlayer(self):
        self.__currentPlayer = self.__playerIndex(self.__currentPlayer + 1)

    

    def __playerIndex(self, index):
        return index % len(self.players)