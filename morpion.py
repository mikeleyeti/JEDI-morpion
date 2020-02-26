from random import choice


# convention pour le plateau
X, Vide, O = -1, 0, 1


def nouveau_plateau():
    """
    Retroune un plateau vide.
    """
    return [[Vide] * 3 for _ in range(3)]


def autre_joueur(joueur):
    """
    TODO.
    """
    return O if joueur == X else X


def est_vide(plateau, ligne, colonne):
    """
    TODO.
    """
    return plateau[ligne][colonne] == Vide


def coups_possibles(plateau):
    """
    TODO.
    """
    return [(i, j) for i in range(3) for j in range(3)
            if est_vide(plateau, i, j)]


def jouer(plateau, joueur, ligne, colonne):
    """
    TODO.
    """
    plateau[ligne][colonne] = joueur


def jouer_ia_alea(plateau, joueur):
    """
    TODO.
    """
    i, j = choice(coups_possibles(plateau))
    jouer(plateau, joueur, i, j)


def est_plein(plateau):
    """
    TODO.
    """
    return sum(l.count(Vide) for l in plateau) == 0


def victoire_ligne(plateau, joueur):
    """
    TODO.
    """
    for ligne in plateau:
        if all(c == joueur for c in ligne):
            return True
    return False


def victoire_colonne(plateau, joueur):
    """
    TODO.
    """
    for j in range(3):
        if all(plateau[i][j] == joueur for i in range(3)):
            return True
    return False


def victoire_diagonale(plateau, joueur):
    """
    TODO.
    """
    if (all(plateau[2 - i][i] == joueur for i in range(3))
            or all(plateau[i][i] == joueur for i in range(3))):
            return True
    return False


def victoire(plateau, joueur):
    """
    TODO.
    """
    return (victoire_ligne(plateau, joueur)
            or victoire_colonne(plateau, joueur)
            or victoire_diagonale(plateau, joueur))


if __name__ == "__main__":
    # les tests sont à mettre ici
    pass
