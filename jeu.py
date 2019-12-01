import quoridor
# from collections.abc import Iterable


if __name__ == "__main__":
    """Bloc principal du module principal"""

    joueurs = [
        {"nom": "idul", "murs": 7, "pos": [5, 5]},
        {"nom": "automate", "murs": 3, "pos": [8, 6]}
               ]

    murs = {
        "horizontaux": [[4, 4], [2, 6], [3, 8], [5, 8], [7, 8]],
        "verticaux": [[6, 2], [4, 4], [2, 6], [7, 5], [7, 7]]
               }

    jeu = quoridor.Quoridor(joueurs, murs)

    while True:
        ETAT = jeu.état_partie()
        print(jeu)
        type_coup = input("Entrez votre type de coup: (D = déplacer joueur, MH = mur horizontal et MV = mur vertical ) ")
        x = int(input("Entrez la coordonnée x de votre coup: "))
        y = int(input("Entrez la coordonnée y de votre coup: "))
        POS = (x, y)
        if type_coup == "D":
            jeu.déplacer_jeton(1, POS)
        elif type_coup == "MH":
            jeu.placer_mur(1, POS, 'horizontal')
        elif type_coup == "MV":
            jeu.placer_mur(1, POS, 'vertical')
        else:
            print("Commande n'existe pas")
            continue
        print(jeu)
        if jeu.partie_terminée() is False:
            jeu.jouer_coup(2)
        else:
            print(jeu.partie_terminée())
            break
