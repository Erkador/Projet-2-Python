from collections.abc import Iterable
import networkx as nx


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
        sortie = ""
        murs_h = self.etat["murs"]["horizontaux"]
        murs_v = self.etat["murs"]["verticaux"]
        nom_1 = self.etat["joueurs"][0]["nom"]
        nom_2 = "automate"
        pos_1 = self.etat["joueurs"][0]["pos"]
        pos_2 = self.etat["joueurs"][1]["pos"]
        sortie += f"Légende: 1={nom_1}, 2={nom_2}\n"
        sortie += "   -----------------------------------\n"
        grille = [["9", " ", "|", " ", ".", " ", " ", " ", ".", " ", " ", " ", ".", " ", " ", " ", ".",
                " ", " ", " ", ".", " ", " ", " ", ".", " ", " ", " ", ".", " ", " ", " ", ".", " ",
                " ", " ", ".", " ", "|", "\n"],
                [" ", " ", "|", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
                " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
                " ", " ", " ", " ", "|", "\n"],
                ["8", " ", "|", " ", ".", " ", " ", " ", ".", " ", " ", " ", ".", " ", " ", " ", ".",
                " ", " ", " ", ".", " ", " ", " ", ".", " ", " ", " ", ".", " ", " ", " ", ".", " ",
                " ", " ", ".", " ", "|", "\n"],
                [" ", " ", "|", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
                " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
                " ", " ", " ", " ", "|", "\n"],
                ["7", " ", "|", " ", ".", " ", " ", " ", ".", " ", " ", " ", ".", " ", " ", " ", ".",
                " ", " ", " ", ".", " ", " ", " ", ".", " ", " ", " ", ".", " ", " ", " ", ".", " ",
                " ", " ", ".", " ", "|", "\n"],
                [" ", " ", "|", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
                " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
                " ", " ", " ", " ", "|", "\n"],
                ["6", " ", "|", " ", ".", " ", " ", " ", ".", " ", " ", " ", ".", " ", " ", " ", ".",
                " ", " ", " ", ".", " ", " ", " ", ".", " ", " ", " ", ".", " ", " ", " ", ".", " ",
                " ", " ", ".", " ", "|", "\n"],
                [" ", " ", "|", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
                " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
                " ", " ", " ", " ", "|", "\n"],
                ["5", " ", "|", " ", ".", " ", " ", " ", ".", " ", " ", " ", ".", " ", " ", " ", ".",
                " ", " ", " ", ".", " ", " ", " ", ".", " ", " ", " ", ".", " ", " ", " ", ".", " ",
                " ", " ", ".", " ", "|", "\n"],
                [" ", " ", "|", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
                " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
                " ", " ", " ", " ", "|", "\n"],
                ["4", " ", "|", " ", ".", " ", " ", " ", ".", " ", " ", " ", ".", " ", " ", " ", ".",
                " ", " ", " ", ".", " ", " ", " ", ".", " ", " ", " ", ".", " ", " ", " ", ".", " ",
                " ", " ", ".", " ", "|", "\n"],
                [" ", " ", "|", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
                " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
                " ", " ", " ", " ", "|", "\n"],
                ["3", " ", "|", " ", ".", " ", " ", " ", ".", " ", " ", " ", ".", " ", " ", " ", ".",
                " ", " ", " ", ".", " ", " ", " ", ".", " ", " ", " ", ".", " ", " ", " ", ".", " ",
                " ", " ", ".", " ", "|", "\n"],
                [" ", " ", "|", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
                " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
                " ", " ", " ", " ", "|", "\n"],
                ["2", " ", "|", " ", ".", " ", " ", " ", ".", " ", " ", " ", ".", " ", " ", " ", ".",
                " ", " ", " ", ".", " ", " ", " ", ".", " ", " ", " ", ".", " ", " ", " ", ".", " ",
                " ", " ", ".", " ", "|", "\n"],
                [" ", " ", "|", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
                " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
                " ", " ", " ", " ", "|", "\n"],
                ["1", " ", "|", " ", ".", " ", " ", " ", ".", " ", " ", " ", ".", " ", " ", " ", ".",
                " ", " ", " ", ".", " ", " ", " ", ".", " ", " ", " ", ".", " ", " ", " ", ".", " ",
                " ", " ", ".", " ", "|", "\n"]]
        for i in murs_h:
            for e in range(7):
                grille[19 - 2 * i[1]][4 * i[0] - 1 + e] = "-"
        for i in murs_v:
            for e in range(3):
                grille[18 - (2 * i[1] + e)][4 * i[0] - 2] = "|"
        grille[18 - 2 * pos_1[1]][4 * pos_1[0]] = "1"
        grille[18 - 2 * pos_2[1]][4 * pos_2[0]] = "2"
        jeu = ""
        for i in grille:
            jeu += "".join(i)
        sortie += jeu
        sortie += "--|-----------------------------------\n  | 1   2   3   4   5   6   7   8   9"
        return sortie

    def déplacer_jeton(self, joueur, position):
        """
        Pour le joueur spécifié, déplacer son jeton à la position spécifiée.

        :param joueur: un entier spécifiant le numéro du joueur (1 ou 2).
        :param position: le tuple (x, y) de la position du jeton (1<=x<=9 et 1<=y<=9).
        :raises QuoridorError: le numéro du joueur est autre que 1 ou 2.
        :raises QuoridorError: la position est invalide (en dehors du damier).
        :raises QuoridorError: la position est invalide pour l'état actuel du jeu.
        """
        TestPlayersNumbers(joueur)

        if position[0] not in range(10, 1) or position[1] not in range(10, 1):
            raise QuoridorError("Position given is outside of board")

        if self.etat["joueurs"][OtherPlayer(joueur)]["pos"] == position:
            raise QuoridorError("Position given is invalid (occupied)")
        
        positionJoueur = self.etat["joueurs"][joueur]["pos"]

        mouvementX = position[0] - self.etat["joueurs"][joueur]["pos"][0]
        mouvementY = position[1] - self.etat["joueurs"][joueur]["pos"][1]

        if(mouvementY > 0):
            positionHorizontal = (position[0], position[1] - 1)
            positionAvantHorizontal = (position[0] - 1, position[1] - 1)

            if positionHorizontal in self.etat['murs']['horizontaux'] or positionAvantHorizontal in self.etat['murs']['horizontaux']:
                raise QuoridorError("Position given is invalid (occupied)")
        elif(mouvementY < 0):
            positionHorizontal = (position[0], position[1])
            positionAvantHorizontal = (position[0] - 1, position[1])

            if positionHorizontal in self.etat['murs']['horizontaux'] or positionAvantHorizontal in self.etat['murs']['horizontaux']:
                raise QuoridorError("Position given is invalid (occupied)")

        if(mouvementX > 0):
            positionVertical = (position[0] - 1, position[1])
            positionAvantVertical = (position[0] - 1, position[1] - 1)

            if positionVertical in self.etat['murs']['verticaux'] or positionAvantVertical in self.etat['murs']['verticaux']:
                raise QuoridorError("Position given is invalid (occupied)")
        elif(mouvementX < 0):
            positionVertical = (position[0], position[1])
            positionAvantVertical = (position[0], position[1] - 1)

            if positionVertical in self.etat['murs']['verticaux'] or positionAvantVertical in self.etat['murs']['verticaux']:
                raise QuoridorError("Position given is invalid (occupied)")

        positionVertical = (position[0], position[1] - 1)

        self.etat["joueurs"][joueur]["pos"] = position

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
        return self.etat

    def jouer_coup(self, joueur):
        """
        Pour le joueur spécifié, jouer automatiquement son meilleur coup pour l'état actuel
        de la partie. Ce coup est soit le déplacement de son jeton, soit le placement d'un
        mur horizontal ou vertical.

        :param joueur: un entier spécifiant le numéro du joueur (1 ou 2).
        :raises QuoridorError: le numéro du joueur est autre que 1 ou 2.
        :raises QuoridorError: la partie est déjà terminée.
        """
        TestPlayersNumbers(joueur)

        if self.partie_terminée() is str:
            raise QuoridorError(f"Player {joueur} tried to run a finished game")

        self.last_player = joueur

        graphe = construire_graphe(
            [joueur['pos'] for joueur in self.etat['joueurs']],
            self.etat['murs']['horizontaux'],
            self.etat['murs']['verticaux']
                                    )

        self.déplacer_jeton(joueur, nx.shortest_path(graphe, joueur['pos'], 'B' + str(joueur))[1])

    def partie_terminée(self):
        """
        Déterminer si la partie est terminée.

        :returns: le nom du gagnant si la partie est terminée; False autrement.
        """
        if self.last_player == 1:
            goal = 9
        else:
            goal = 1

        if self.etat["joueurs"][self.last_player]["pos"][1] == goal:
            return self.etat["joueurs"][self.last_player]["nom"]
        else:
            return False

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
        TestPlayersNumbers(joueur)

        if self.etat["joueur"][joueur]["murs"] == 0:
            raise QuoridorError(f"Player {joueur} has no more walls")

        MursHor = self.etat['murs']['horizontaux']
        MursVer = self.etat['murs']['verticaux']

        if(orientation == "horizontal"):
            posHorAvant = (position[0] - 1, position[1])
            posHorApres = (position[0] + 1, position[1])
            posVerCorresp = (position[0], position[1] + 1)

            if position in MursHor or posHorAvant in MursHor or posHorApres in MursHor or posVerCorresp in MursVer:
                raise QuoridorError(f"There is already a wall at {position}")

            if position[0] not in range(1, 9) or position[1] not in range(1, 9):
                raise QuoridorError(f"Position {position} is invalid")

            self.etat['murs']['horizontaux'] += [position[0], position[1]]
        else:
            posVerAvant = (position[0], position[1] - 1)
            posVerApres = (position[0], position[1] + 1)
            posHorCorres = (position[0] - 1, position[1])

            if position in MursVer or posVerAvant in MursVer or posVerApres in MursVer or posHorCorres in MursHor:
                raise QuoridorError(f"There is already a wall at {position}")

            if position[0] not in range(1, 9) or position[1] not in range(2, 10):
                raise QuoridorError(f"Position {position} is invalid")

            self.etat['murs']['verticaux'] += [position[0], position[1]]

        self.etat['joueurs'][joueur]["murs"] -= 1

def construire_graphe(joueurs, murs_horizontaux, murs_verticaux):
    """
    Crée le graphe des déplacements admissibles pour les joueurs.

    :param joueurs: une liste des positions (x,y) des joueurs.
    :param murs_horizontaux: une liste des positions (x,y) des murs horizontaux.
    :param murs_verticaux: une liste des positions (x,y) des murs verticaux.
    :returns: le graphe bidirectionnel (en networkX) des déplacements admissibles.
    """

    graphe = nx.DiGraph()

    # pour chaque colonne du damier
    for x in range(1, 10):
        # pour chaque ligne du damier
        for y in range(1, 10):
            # ajouter les arcs de tous les déplacements possibles pour cette tuile
            if x > 1:
                graphe.add_edge((x, y), (x-1, y))
            if x < 9:
                graphe.add_edge((x, y), (x+1, y))
            if y > 1:
                graphe.add_edge((x, y), (x, y-1))
            if y < 9:
                graphe.add_edge((x, y), (x, y+1))

    # retirer tous les arcs qui croisent les murs horizontaux
    for x, y in murs_horizontaux:
        graphe.remove_edge((x, y-1), (x, y))
        graphe.remove_edge((x, y), (x, y-1))
        graphe.remove_edge((x+1, y-1), (x+1, y))
        graphe.remove_edge((x+1, y), (x+1, y-1))

    # retirer tous les arcs qui croisent les murs verticaux
    for x, y in murs_verticaux:
        graphe.remove_edge((x-1, y), (x, y))
        graphe.remove_edge((x, y), (x-1, y))
        graphe.remove_edge((x-1, y+1), (x, y+1))
        graphe.remove_edge((x, y+1), (x-1, y+1))

    # retirer tous les arcs qui pointent vers les positions des joueurs
    # et ajouter les sauts en ligne droite ou en diagonale, selon le cas
    for joueur in map(tuple, joueurs):

        for prédécesseur in list(graphe.predecessors(joueur)):
            graphe.remove_edge(prédécesseur, joueur)

            # si admissible, ajouter un lien sauteur
            successeur = (2*joueur[0]-prédécesseur[0], 2*joueur[1]-prédécesseur[1])

            if successeur in graphe.successors(joueur) and successeur not in joueurs:
                # ajouter un saut en ligne droite
                graphe.add_edge(prédécesseur, successeur)

            else:
                # ajouter les liens en diagonal
                for successeur in list(graphe.successors(joueur)):
                    if prédécesseur != successeur and successeur not in joueurs:
                        graphe.add_edge(prédécesseur, successeur)

    # ajouter les noeuds objectifs des deux joueurs
    for x in range(1, 10):
        graphe.add_edge((x, 9), 'B1')
        graphe.add_edge((x, 1), 'B2')

    return graphe


def TestPlayersNumbers(joueur):
    if joueur not in [1, 2]:
        raise QuoridorError(f"Player {joueur} is not a valid #")


def OtherPlayer(joueur):
    if joueur == 1:
        return 0
    else:
        return 1
