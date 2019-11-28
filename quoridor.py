from collections.abc import Iterable

class QuoridorError(Exception):
    pass


class Quoridor:

    def __init__(self, joueurs, murs=None):
        """
        Initialiser une partie de Quoridor avec les joueurs et les murs spécifiés, 
        en s'assurant de faire une copie profonde de tout ce qui a besoin d'être copié.

        //:param joueurs: un itérable de deux joueurs dont le premier est toujours celui qui 
        //débute la partie. Un joueur est soit une chaîne de caractères soit un dictionnaire. 
        //Dans le cas d'une chaîne, il s'agit du nom du joueur. Selon le rang du joueur dans 
        //l'itérable, sa position est soit (5,1) soit (5,9), et chaque joueur peut initialement
        //placer 10 murs. Dans le cas où l'argument est un dictionnaire, celui-ci doit contenir 
        //une clé 'nom' identifiant le joueur, une clé 'murs' spécifiant le nombre de murs qu'il 
        //peut encore placer, et une clé 'pos' qui spécifie sa position (x, y) actuelle.
        
        :param murs: un dictionnaire contenant une clé 'horizontaux' associée à la liste des
        positions (x, y) des murs horizontaux, et une clé 'verticaux' associée à la liste des
        positions (x, y) des murs verticaux. Par défaut, il n'y a aucun mur placé sur le jeu.

        """
        if not isinstance(joueurs, Iterable):
            raise QuoridorError("Not iterable")
        if len(joueurs) > 2:
            raise QuoridorError("Iterable not equal to 2")
        if murs and murs != type(dict):
            raise QuoridorError("Murs is present but not dict")
        self.players = [
                {'nom': "", 'murs': 10, 'pos': (5, 1)},
                {'nom': "", 'murs': 10, 'pos': (5, 9)},
            ]
        if murs is None:
            self.murs = {
                'horizontaux': [],
                'verticaux': []
            }
        else:
            self.murs = murs
        self.etat = {'joueurs': self.players, 'murs': self.murs}
        for i, val in enumerate(joueurs):
            if val is str:
                self.players[i]['nom'] = val
                if i == 0:
                    self.players[i]['pos'] = (5, 1)
                elif i == 1:
                    self.players[i]['pos'] = (5, 9)
            elif val is dict:
                self.players[i]['nom'] = val['nom']
                self.players[i]['murs'] = val['murs']
                self.players[i]['pos'] = val['pos']
        for i, val in enumerate(self.players):
            x, y = self.players[i]['pos']
            if x < 1 or x > 9 or y < 1 or y > 9:
                raise QuoridorError("Player position out of bounds")
            if self.players[i]['murs'] > 10 or self.players[i]['murs'] < 0:
                raise QuoridorError("Number of walls invalid")
        if len(self.murs['horizontaux']) > 0:
            for i in self.murs['horizontaux']:
                x, y = i[0], i[1]
                if x < 1 or x > 8 or y < 2 or y > 9:
                    raise QuoridorError("Horizontal wall out of bounds")
        if len(self.murs['verticaux']) > 0:
            for i in self.murs['verticaux']:
                x, y = i[0], i[1]
                if x < 2 or x > 9 or y < 1 or y > 8:
                    raise QuoridorError("Vertical wall out of bounds")
        placed_walls = 0
        placed_walls += len(self.murs['horizontaux']) + len(self.murs['verticaux'])
        placable_walls = 0
        placable_walls += self.players[0]['murs'] + self.players[1]['murs']
        if placed_walls + placable_walls != 20:
            raise QuoridorError("Number of walls not equal to 20")


    def __str__(self):
        """
        Produire la représentation en art ascii correspondant à l'état actuel de la partie. 
        Cette représentation est la même que celle du TP précédent.

        :returns: la chaîne de caractères de la représentation.
        """

    def déplacer_jeton(self, joueur, position):
        """
        Pour le joueur spécifié, déplacer son jeton à la position spécifiée.

        :param joueur: un entier spécifiant le numéro du joueur (1 ou 2).
        :param position: le tuple (x, y) de la position du jeton (1<=x<=9 et 1<=y<=9).
        :raises QuoridorError: le numéro du joueur est autre que 1 ou 2.
        :raises QuoridorError: la position est invalide (en dehors du damier).
        :raises QuoridorError: la position est invalide pour l'état actuel du jeu.
        """

    def état_partie(self):
        """
        Produire l'état actuel de la partie.

        :returns: une copie de l'état actuel du jeu sous la forme d'un dictionnaire:
        {
            'joueurs': [
                {'nom': nom1, 'murs': n1, 'pos': (x1, y1)},
                {'nom': nom2, 'murs': n2, 'pos': (x2, y2)},
            ],
            'murs': {
                'horizontaux': [...],
                'verticaux': [...],
            }
        }
        
        où la clé 'nom' d'un joueur est associée à son nom, la clé 'murs' est associée 
        au nombre de murs qu'il peut encore placer sur ce damier, et la clé 'pos' est 
        associée à sa position sur le damier. Une position est représentée par un tuple 
        de deux coordonnées x et y, où 1<=x<=9 et 1<=y<=9.

        Les murs actuellement placés sur le damier sont énumérés dans deux listes de
        positions (x, y). Les murs ont toujours une longueur de 2 cases et leur position
        est relative à leur coin inférieur gauche. Par convention, un mur horizontal se
        situe entre les lignes y-1 et y, et bloque les colonnes x et x+1. De même, un
        mur vertical se situe entre les colonnes x-1 et x, et bloque les lignes x et x+1.
        """

    def jouer_coup(self, joueur):
        """
        Pour le joueur spécifié, jouer automatiquement son meilleur coup pour l'état actuel 
        de la partie. Ce coup est soit le déplacement de son jeton, soit le placement d'un 
        mur horizontal ou vertical.

        :param joueur: un entier spécifiant le numéro du joueur (1 ou 2).
        :raises QuoridorError: le numéro du joueur est autre que 1 ou 2.
        :raises QuoridorError: la partie est déjà terminée.
        """

    def partie_terminée(self):
        """
        Déterminer si la partie est terminée.

        :returns: le nom du gagnant si la partie est terminée; False autrement.
        """

    def placer_mur(self, joueur: int, position: tuple, orientation: str):
        """
        Pour le joueur spécifié, placer un mur à la position spécifiée.

        :param joueur: le numéro du joueur (1 ou 2).
        :param position: le tuple (x, y) de la position du mur.
        :param orientation: l'orientation du mur ('horizontal' ou 'vertical').
        :raises QuoridorError: le numéro du joueur est autre que 1 ou 2.
        :raises QuoridorError: un mur occupe déjà cette position.
        :raises QuoridorError: la position est invalide pour cette orientation.
        :raises QuoridorError: le joueur a déjà placé tous ses murs.
        """

test = Quoridor(["noob", "as fuck"])