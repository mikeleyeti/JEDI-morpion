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
    Retourne l'identifiant de l'aversaire de joueur.
    """
    return O if joueur == X else X


def est_vide(plateau, ligne, colonne):
    """
    Teste si la case du plateau est vide.
    """
    return plateau[ligne][colonne] == Vide


def coups_possibles(plateau):
    """
    Retourne la liste des cases vides sous la forme de couples
    de coodonnées.
    """
    return [(i, j) for i in range(3) for j in range(3)
            if est_vide(plateau, i, j)]


def jouer(plateau, joueur, ligne, colonne):
    """
    Joue un coup sur le plateau.
    """
    plateau[ligne][colonne] = joueur


def jouer_ia_alea(plateau, joueur):
    """
    Jouer un coup aléatoire sur le plateau.
    """
    i, j = choice(coups_possibles(plateau))
    jouer(plateau, joueur, i, j)


def nombre_cases_vides(plateau):
    """
    Retourne le nombre de cases vides sur le plateau.
    """
    return sum(l.count(Vide) for l in plateau)


def est_plein(plateau):
    """
    Teste si le plateau est plein.
    """
    return nombre_cases_vides(plateau) == 0


def victoire_ligne(plateau, joueur):
    """
    Teste si le plateau admet une victoire en ligne pour le joueur.
    """
    for ligne in plateau:
        if all(c == joueur for c in ligne):
            return True
    return False


def victoire_colonne(plateau, joueur):
    """
    Teste si le plateau admet une victoire en colonne pour le joueur.
    """
    for j in range(3):
        if all(plateau[i][j] == joueur for i in range(3)):
            return True
    return False


def victoire_diagonale(plateau, joueur):
    """
    Teste si le plateau admet une victoire en diagonale pour le joueur.
    """
    if (all(plateau[2 - i][i] == joueur for i in range(3))
            or all(plateau[i][i] == joueur for i in range(3))):
            return True
    return False


def victoire(plateau, joueur):
    """
    Teste si le plateau admet une victoire pour le joueur.
    """
    return (victoire_ligne(plateau, joueur)
            or victoire_colonne(plateau, joueur)
            or victoire_diagonale(plateau, joueur))


if __name__ == "__main__":
    # les tests sont à mettre ici
    pass
