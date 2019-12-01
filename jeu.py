import quoridor
from collections.abc import Iterable

if __name__ == "__main__":
    """Bloc principal du module principal"""
    joueurs = ["j1", "j2"]
    
    jeu = quoridor.Quoridor(joueurs)
    
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
        if jeu.partie_terminée() == False:
            jeu.jouer_coup(2)
        else:
            print(jeu.partie_terminée())
            break