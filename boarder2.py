class case():
    # makes the idividual tiles and their surroundings
    def __init__(self, coord):
        a = " . "
        b = " "
        c = "   "
        self.x = coord[0]
        self.y = coord[1]
        self.r = False
        self.t = False
        if self.x == 9:
            self.r = True
        if self.y == 9:
            self.t = True
        if self.t is False and self.r is False:
            self.type = 1
            self.layout = [[c, b], [a, b]]
        elif self.t is True and self.r is True:
            self.type = 2
            self.layout = [["--- "], [a, "|"]]
        elif self.t is True:
            self.type = 3
            self.layout = [["----"], [a, b]]
        elif self.r is True:
            self.type = 4
            self.layout = [[c, "|"], [a, "|"]]

    def murs(self, list_murs):
        mv = "|"
        mh = "-"
        mh3 = "---"
        mv_list = list_murs["verticaux"]
        mh_list = list_murs["horizontaux"]
        for murs in mv_list:
            if (murs[0], murs[1]) == (self.x + 1, self.y):
                self.layout[0][1] = mv
                self.layout[1][1] = mv
            if (murs[0], murs[1]) == (self.x + 1, self.y - 1):
                self.layout[1][1] = mv
        for murs in mh_list:
            if (murs[0], murs[1]) == (self.x, self.y + 1):
                self.layout[0][0] = mh3
                self.layout[0][1] = mh
            if (murs[0], murs[1]) == (self.x - 1, self.y + 1):
                self.layout[0][0] = mh3

    def joueurs(self, list_j):
        if (list_j[0]["pos"][0], list_j[0]["pos"][1]) == (self.x, self.y):
            self.layout[1][0] = " 1 "
        if (list_j[1]["pos"][0], list_j[1]["pos"][1]) == (self.x, self.y):
            self.layout[1][0] = " 2 "

    def list(self):
        ligne = "".join(self.layout[1])
        li_vide = "".join(self.layout[0])
        return [li_vide, ligne]

    def __str__(self):
        return(str(self.list()))


class board():
    # stiches the tiles to get the board
    def __init__(self, infos):
        self.jou = infos["joueurs"]
        self.mu = infos["murs"]
        self.idul = self.jou[0]["nom"]
        self.ai = self.jou[1]["nom"]

    def board_up(self):             # changer les noms de joueurs
        board = []
        for y in range(9, 0, -1):
            ligne1 = []
            ligne2 = []
            for x in range(1, 10):
                a = case((x, y))
                a.murs(self.mu)
                a.joueurs(self.jou)
                carr = a.list()
                ligne1 += carr[0]
                ligne2 += carr[1]
            u = "|"
            if y == 9:
                u = " "
            board += f"  {u}" + "".join(ligne1) + "\n" + f"{y} |" + "".join(ligne2) + "\n"
        board = (f"Légende: 1={self.idul}, 2={self.ai}\n" + "".join(board)
                 + "--|-----------------------------------\n  | 1   2   3   4   5   6   7   8   9")
        return "".join(board) + "\n"
