def QuoridorError(Exception):
    pass


def TestPlayersNumbers(joueur):
    if joueur not in [1, 2]:
        raise QuoridorError(f"Player {joueur} is not a valid #")


def OtherPlayer(joueur):
    if joueur == 1:
        return 2
    else:
        return 1


class Quoridor:

    def __init__(self, joueurs, murs=None):
        pass

        """
        LP
        """

    def __str__(self):
        import boarder2 as boarder
        a = boarder.board(self.etat)
        return(a.board_up())

    def déplacer_jeton(self, joueur, position):
        TestPlayersNumbers(joueur)

        if position[0] not in range(10, 1) or position[1] not in range(10, 1):
            raise QuoridorError("Position given is outside of board")

        if self.etat["joueurs"][OtherPlayer(joueur)]["pos"] == position:
            raise QuoridorError("Position given is invalid (occupied)")

        self.etat["joueurs"][joueur]["pos"] = position

    def placer_mur(self, joueur: int, position: tuple, orientation: str):
        TestPlayersNumbers(joueur)

        if self.etat["joueur"][joueur]["murs"] == 0:
            raise QuoridorError(f"Player {joueur} has no more walls")

        """
        :param orientation: l'orientation du mur ('horizontal' ou 'vertical').

        :raises QuoridorError: un mur occupe déjà cette position.
        :raises QuoridorError: la position est invalide pour cette orientation.
        """

    def état_partie(self):
        return self.etat

    def jouer_coup(self, joueur):

        TestPlayersNumbers(joueur)

        if self.partie_terminée() is str:
            raise QuoridorError(f"Player {joueur} tried to run a finished game")

        """
        Dave
        """

        self.last_player = joueur

    def partie_terminée(self):
        if self.last_player == 1:
            goal = 9
        else:
            goal = 1

        if self.etat["joueurs"][self.last_player]["pos"][1] == goal:
            return self.etat["joueurs"][self.last_player]["nom"]
        else:
            return False
