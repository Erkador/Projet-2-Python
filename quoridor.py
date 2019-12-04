"""Ce module contient la classe et les fonctions nécéssaireau fonctionnement de Quoridor"""
from collections.abc import Iterable
import networkx as nx


class QuoridorError(Exception):
    """Cette classe sert à relever des erreurs au code"""
    pass


class Quoridor:
    """Cette classe implémente la plus grande partie du jeu"""

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
            raise QuoridorError("Players is not an iterable")

        if len(joueurs) > 2:
            raise QuoridorError("More than two players were given")

        if murs and not isinstance(murs, dict):
            raise QuoridorError("Walls given are not in a dictionary")

        if isinstance(joueurs[0], str):
            self.players = [
                                {'nom': f"{joueurs[0]}", 'murs': 10, 'pos': (5, 1)},
                                {'nom': f"{joueurs[1]}", 'murs': 10, 'pos': (5, 9)},
                            ]
        else:
            self.players = joueurs
            self.players[0]["pos"] = [self.players[0]["pos"][0], self.players[0]["pos"][1]]
            self.players[1]["pos"] = [self.players[1]["pos"][0], self.players[1]["pos"][1]]

        if isinstance(murs, dict):
            self.murs = murs

        else:
            self.murs = {
                            'horizontaux': [],
                            'verticaux': []
                        }

        self.etat = {'joueurs': self.players, 'murs': self.murs}

        for i, val in enumerate(joueurs):
            if isinstance(val, str):
                self.players[i]['nom'] = val
                if i == 0:
                    self.players[i]['pos'] = (5, 1)
                elif i == 1:
                    self.players[i]['pos'] = (5, 9)
            elif isinstance(val, dict):
                self.players[i]['nom'] = val['nom']
                self.players[i]['murs'] = val['murs']
                self.players[i]['pos'] = val['pos']

        for i in range(2):
            x, y = self.players[i]['pos']
            if x < 1 or x > 9 or y < 1 or y > 9:
                raise QuoridorError(f"Player {i} out of bounds")
            qtt_murs = self.players[i]['murs']
            if qtt_murs > 10 or qtt_murs < 0:
                raise QuoridorError(f"Player {i} number of walls invalid")

        for i in self.murs['horizontaux']:
            x, y = i[0], i[1]
            if x < 1 or x > 8 or y < 2 or y > 9:
                raise QuoridorError("Horizontal wall out of bounds")

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

        self.last_player = 2

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
        nom_2 = self.etat["joueurs"][1]["nom"]
        pos_1 = self.etat["joueurs"][0]["pos"]
        pos_2 = self.etat["joueurs"][1]["pos"]
        sortie += f"Légende: 1={nom_1}, 2={nom_2}\n"
        sortie += "   -----------------------------------\n"
        grille = [["9", " ", "|", " ", ".", " ", " ", " ", ".", " ", " ", " ",
                   ".", " ", " ", " ", ".", " ", " ", " ", ".", " ", " ", " ",
                   ".", " ", " ", " ", ".", " ", " ", " ", ".", " ", " ", " ",
                   ".", " ", "|", "\n"],
                  [" ", " ", "|", " ", " ", " ", " ", " ", " ", " ", " ", " ",
                   " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
                   " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
                   " ", " ", "|", "\n"],
                  ["8", " ", "|", " ", ".", " ", " ", " ", ".", " ", " ", " ",
                   ".", " ", " ", " ", ".", " ", " ", " ", ".", " ", " ", " ",
                   ".", " ", " ", " ", ".", " ", " ", " ", ".", " ", " ", " ",
                   ".", " ", "|", "\n"],
                  [" ", " ", "|", " ", " ", " ", " ", " ", " ", " ", " ", " ",
                   " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
                   " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
                   " ", " ", "|", "\n"],
                  ["7", " ", "|", " ", ".", " ", " ", " ", ".", " ", " ", " ",
                   ".", " ", " ", " ", ".", " ", " ", " ", ".", " ", " ", " ",
                   ".", " ", " ", " ", ".", " ", " ", " ", ".", " ", " ", " ",
                   ".", " ", "|", "\n"],
                  [" ", " ", "|", " ", " ", " ", " ", " ", " ", " ", " ", " ",
                   " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
                   " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
                   " ", " ", "|", "\n"],
                  ["6", " ", "|", " ", ".", " ", " ", " ", ".", " ", " ", " ",
                   ".", " ", " ", " ", ".", " ", " ", " ", ".", " ", " ", " ",
                   ".", " ", " ", " ", ".", " ", " ", " ", ".", " ", " ", " ",
                   ".", " ", "|", "\n"],
                  [" ", " ", "|", " ", " ", " ", " ", " ", " ", " ", " ", " ",
                   " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
                   " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
                   " ", " ", "|", "\n"],
                  ["5", " ", "|", " ", ".", " ", " ", " ", ".", " ", " ", " ",
                   ".", " ", " ", " ", ".", " ", " ", " ", ".", " ", " ", " ",
                   ".", " ", " ", " ", ".", " ", " ", " ", ".", " ", " ", " ",
                   ".", " ", "|", "\n"],
                  [" ", " ", "|", " ", " ", " ", " ", " ", " ", " ", " ", " ",
                   " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
                   " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
                   " ", " ", "|", "\n"],
                  ["4", " ", "|", " ", ".", " ", " ", " ", ".", " ", " ", " ",
                   ".", " ", " ", " ", ".", " ", " ", " ", ".", " ", " ", " ",
                   ".", " ", " ", " ", ".", " ", " ", " ", ".", " ", " ", " ",
                   ".", " ", "|", "\n"],
                  [" ", " ", "|", " ", " ", " ", " ", " ", " ", " ", " ", " ",
                   " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
                   " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
                   " ", " ", "|", "\n"],
                  ["3", " ", "|", " ", ".", " ", " ", " ", ".", " ", " ", " ",
                   ".", " ", " ", " ", ".", " ", " ", " ", ".", " ", " ", " ",
                   ".", " ", " ", " ", ".", " ", " ", " ", ".", " ", " ", " ",
                   ".", " ", "|", "\n"],
                  [" ", " ", "|", " ", " ", " ", " ", " ", " ", " ", " ", " ",
                   " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
                   " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
                   " ", " ", "|", "\n"],
                  ["2", " ", "|", " ", ".", " ", " ", " ", ".", " ", " ", " ",
                   ".", " ", " ", " ", ".", " ", " ", " ", ".", " ", " ", " ",
                   ".", " ", " ", " ", ".", " ", " ", " ", ".", " ", " ", " ",
                   ".", " ", "|", "\n"],
                  [" ", " ", "|", " ", " ", " ", " ", " ", " ", " ", " ", " ",
                   " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
                   " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
                   " ", " ", "|", "\n"],
                  ["1", " ", "|", " ", ".", " ", " ", " ", ".", " ", " ", " ",
                   ".", " ", " ", " ", ".", " ", " ", " ", ".", " ", " ", " ",
                   ".", " ", " ", " ", ".", " ", " ", " ", ".", " ", " ", " ",
                   ".", " ", "|", "\n"]]
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
        position = [position[0], position[1]]
        test_players_numbers(joueur)

        if position[0] not in range(1, 10) or position[1] not in range(1, 10):
            raise QuoridorError("Position given is outside of board")

        if self.etat["joueurs"][other_player(joueur) - 1]["pos"] == position:
            raise QuoridorError("Position given is invalid (occupied)")

        if self.etat["joueurs"][joueur - 1]["pos"] == position:
            raise QuoridorError("Player cannot stay immobile")

        pos_joueur = self.etat["joueurs"][joueur - 1]["pos"]
        mouvement_x = position[0] - pos_joueur[0]
        mouvement_y = position[1] - pos_joueur[1]

        if abs(mouvement_x) + abs(mouvement_y) > 2:
            raise QuoridorError("Player tried to move more than 2 tiles")

        murs_hor = self.etat['murs']['horizontaux']
        murs_ver = self.etat['murs']['verticaux']

        if mouvement_y > 0:
            pos_hor = [position[0], position[1]]
            pos_avant_hor = [(position[0] - 1), position[1]]

            if pos_hor in murs_hor or pos_avant_hor in murs_hor:
                raise QuoridorError("Position given is invalid (occupied)")

        elif mouvement_y < 0:
            pos_hor = [position[0], (position[1] + 1)]
            pos_avant_hor = [(position[0] - 1), (position[1] + 1)]

            if pos_hor in murs_hor or pos_avant_hor in murs_hor:
                raise QuoridorError("Position given is invalid (occupied)")

        if mouvement_x > 0:
            pos_ver = [position[0], position[1]]
            pos_avant_ver = [position[0], position[1] - 1]

            if pos_ver in murs_ver or pos_avant_ver in murs_ver:
                raise QuoridorError("Position given is invalid (occupied)")

        elif mouvement_x < 0:
            pos_ver = [(position[0] + 1), position[1]]
            pos_avant_ver = [(position[0] + 1), position[1] - 1]

            if pos_ver in murs_ver or pos_avant_ver in murs_ver:
                raise QuoridorError("Position given is invalid (occupied)")

        self.etat["joueurs"][joueur - 1]["pos"] = position
        self.last_player = joueur

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
        test_players_numbers(joueur)

        if isinstance(self.partie_terminée(), str):
            raise QuoridorError(f"Player {joueur} tried to run a finished game")

        graphe = construire_graphe(
            [joueur['pos'] for joueur in self.etat['joueurs']],
            self.etat['murs']['horizontaux'],
            self.etat['murs']['verticaux']
                )

        new_pos = nx.shortest_path(
            graphe,
            self.etat['joueurs'][joueur - 1]['pos'],
            'B' + str(joueur)
                )

        self.déplacer_jeton(joueur, new_pos[1])

    def partie_terminée(self):
        """
        Déterminer si la partie est terminée.

        :returns: le nom du gagnant si la partie est terminée; False autrement.
        """

        if self.etat["joueurs"][0]["pos"][1] == 9:
            return self.etat["joueurs"][0]["nom"]

        if self.etat["joueurs"][1]["pos"][1] == 1:
            return self.etat["joueurs"][1]["nom"]

        else:
            return False

    def placer_mur(self, joueur, position, orientation):
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
        position = [position[0], position[1]]
        test_players_numbers(joueur)

        if self.etat["joueurs"][joueur - 1]["murs"] == 0:
            raise QuoridorError(f"Player {joueur} has no more walls")

        murs_hor = self.etat['murs']['horizontaux']
        murs_ver = self.etat['murs']['verticaux']

        if orientation == "horizontal":
            pos_hor_avant = [position[0] - 1, position[1]]
            pos_hor_apres = [position[0] + 1, position[1]]
            pos_ver_corresp = [position[0] + 1, position[1] - 1]

            if position in murs_hor or pos_ver_corresp in murs_ver:
                raise QuoridorError(f"There is already a wall here")

            if pos_hor_avant in murs_hor or pos_hor_apres in murs_hor:
                raise QuoridorError(f"There is already a wall left/right")

            if position[0] not in range(1, 9) or position[1] not in range(2, 10):
                raise QuoridorError(f"Position {position} is invalid")

            self.etat['murs']['horizontaux'].append([position[0], position[1]])

        else:
            pos_ver_avant = [position[0] - 1, position[1] - 1]
            pos_ver_apres = [position[0], position[1] + 1]
            pos_hor_corresp = [position[0] - 1, position[1] + 1]

            if position in murs_ver or pos_hor_corresp in murs_hor:
                raise QuoridorError(f"There is already a wall here")

            if pos_ver_avant in murs_ver or pos_ver_apres in murs_ver:
                raise QuoridorError(f"There is already a wall above/below")

            if position[0] not in range(1, 9) or position[1] not in range(1, 9):
                raise QuoridorError(f"Position {position} is invalid")

            self.etat['murs']['verticaux'].append([position[0], position[1]])

        self.etat['joueurs'][joueur - 1]["murs"] -= 1
        self.last_player = joueur


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
                graphe.add_edge((x, y), (x - 1, y))
            if x < 9:
                graphe.add_edge((x, y), (x + 1, y))
            if y > 1:
                graphe.add_edge((x, y), (x, y - 1))
            if y < 9:
                graphe.add_edge((x, y), (x, y + 1))

    # retirer tous les arcs qui croisent les murs horizontaux
    for x, y in murs_horizontaux:
        graphe.remove_edge((x, y - 1), (x, y))
        graphe.remove_edge((x, y), (x, y - 1))
        graphe.remove_edge((x + 1, y - 1), (x + 1, y))
        graphe.remove_edge((x + 1, y), (x + 1, y - 1))

    # retirer tous les arcs qui croisent les murs verticaux
    for x, y in murs_verticaux:
        graphe.remove_edge((x - 1, y), (x, y))
        graphe.remove_edge((x, y), (x - 1, y))
        graphe.remove_edge((x - 1, y + 1), (x, y + 1))
        graphe.remove_edge((x, y + 1), (x - 1, y + 1))

    # s'assurer que les positions des joueurs sont bien des tuples (et non des listes)
    j1, j2 = tuple(joueurs[0]), tuple(joueurs[1])

    # traiter le cas des joueurs adjacents
    if j2 in graphe.successors(j1) or j1 in graphe.successors(j2):

        # retirer les liens entre les joueurs
        graphe.remove_edge(j1, j2)
        graphe.remove_edge(j2, j1)

        def ajouter_lien_sauteur(noeud, voisin):
            """
            :param noeud: noeud de départ du lien.
            :param voisin: voisin par dessus lequel il faut sauter.
            """
            saut = 2*voisin[0]-noeud[0], 2*voisin[1]-noeud[1]

            if saut in graphe.successors(voisin):
                # ajouter le saut en ligne droite
                graphe.add_edge(noeud, saut)

            else:
                # ajouter les sauts en diagonale
                for saut in graphe.successors(voisin):
                    graphe.add_edge(noeud, saut)

        ajouter_lien_sauteur(j1, j2)
        ajouter_lien_sauteur(j2, j1)

    # ajouter les noeuds objectifs des deux joueurs
    for x in range(1, 10):
        graphe.add_edge((x, 9), 'B1')
        graphe.add_edge((x, 1), 'B2')

    return graphe


def test_players_numbers(joueur):
    '''Méthode qui test si le numéro de joueur est 1 ou 2
    Raise une erreur si le numéro de joueur n'est pas valide'''
    if joueur not in [1, 2]:
        raise QuoridorError(f"Player {joueur} is not a valid #")


def other_player(joueur):
    '''Méthode qui retourne le numéro du joueur adverse'''
    if joueur == 1:
        return 2
    return 1
