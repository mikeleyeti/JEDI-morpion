import json
from random import choice

from flask import Flask, render_template, redirect, request

morpion_app = Flask(__name__)


## Conventions :
# -1 = X
# 0 = Vide
# 1 = O


## Initialisation
def initialisation(joueur, premier):
    dico = {
        "plateau": [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
        "joueur": joueur,  # 'X' ou 'O'
        "suivant": premier,  # 'humain' ou 'ia'
        "gagnant": False,
        "nulle": False
    }
    with open('donnees.txt', 'w') as fichier:
        json.dump(dico, fichier)


def lecture_donnees():
    with open('donnees.txt') as json_file:
        dico = json.load(json_file)
    plateau, joueur, suivant, gagnant, nulle = dico["plateau"], dico["joueur"], dico["suivant"], dico["gagnant"], dico[
        "nulle"]
    return plateau, joueur, suivant, gagnant, nulle


def ecriture_donnees(plateau, joueur, suivant, gagnant, nulle):
    dico = {
        "plateau": plateau,
        "joueur": joueur,
        "suivant": suivant,
        "gagnant": gagnant,
        "nulle": nulle
    }
    with open('donnees.txt', 'w') as fichier:
        json.dump(dico, fichier)


def IA_niveau_0(plateau, joueur):
    liste_coups = []
    for i in range(len(plateau)):
        for j in range(len(plateau[i])):
            if plateau[i][j] == 0:
                liste_coups.append((i, j))
    i, j = choice(liste_coups)
    if joueur == 'X':
        plateau[i][j] = 1
    else:
        plateau[i][j] = -1
    return plateau


def test_fin_partie(plateau):
    gagnant = False
    nulle = False
    # test lignes
    for i in range(len(plateau)):
        if plateau[i][0] == plateau[i][1] == plateau[i][2] and plateau[i][0] != 0:
            gagnant = plateau[i][0]
    # test colonnes
    for i in range(len(plateau)):
        if plateau[0][i] == plateau[1][i] == plateau[2][i] and plateau[0][i] != 0:
            gagnant = plateau[0][i]
    # test diagonales
    if ((plateau[0][0] == plateau[1][1] == plateau[2][2]) or (plateau[0][2] == plateau[1][1] == plateau[2][0])) and \
            plateau[1][1] != 0:
        gagnant = plateau[1][1]
    if sum([l.count(0) for l in plateau]) == 0:  # Compte le nombre de case = 0
        if gagnant == False:
            nulle = True
    return gagnant, nulle


# Tests de la fonction test_fin_partie
assert test_fin_partie([[0, 0, 0], [0, 0, 0], [0, 0, 0]]) == (False, False)
assert test_fin_partie([[1, 1, 1], [0, 0, 0], [0, 0, 0]]) == (1, False)
assert test_fin_partie([[0, 1, 1], [-1, -1, -1], [0, 0, 0]]) == (-1, False)
assert test_fin_partie([[0, 1, 1], [-1, 1, -1], [1, 0, 0]]) == (1, False)
assert test_fin_partie([[0, 1, -1], [-1, 1, -1], [1, 0, -1]]) == (-1, False)
assert test_fin_partie([[-1, 1, -1], [-1, 1, -1], [1, -1, 1]]) == (False, True)


@morpion_app.route('/', methods=['GET'])
def nouvellePartie():
    return render_template('nouvelle_partie.html')


@morpion_app.route('/', methods=['POST'])
def debutJeu():
    joueur = request.form['joueur']
    premier = request.form['debut']
    initialisation(joueur, premier)
    return redirect('/jeu')


@morpion_app.route('/jeu')
def affichage():
    plateau, joueur, suivant, gagnant, nulle = lecture_donnees()
    gagnant, nulle = test_fin_partie(plateau)
    if nulle or gagnant != False:
        return render_template("fin-de-partie.html", gagnant=gagnant, nulle=nulle, joueur=joueur)
    if suivant == 'ia':
        plateau = IA_niveau_0(plateau, joueur)
        suivant = 'humain'
    gagnant, nulle = test_fin_partie(plateau)
    if nulle or gagnant != False:
        return render_template("fin-de-partie.html", gagnant=gagnant, nulle=nulle, joueur=joueur)
    ecriture_donnees(plateau, joueur, suivant, gagnant, nulle)
    return render_template('jeu.html', plateau=plateau)


@morpion_app.route('/jouer/<int:ligne>/<int:colonne>')
def jouer(ligne, colonne):
    plateau, joueur, suivant, gagnant, nulle = lecture_donnees()
    # # A modifier : faire appel à une fonction jouer qui teste la case...
    if suivant == 'humain':
        if joueur == 'X':
            plateau[ligne][colonne] = -1
        else:
            plateau[ligne][colonne] = 1
        suivant = 'ia'
    else:  # suivant == 'ia'
        # fonction IA basée sur min/max pour remplacer IA aléatoire
        print("A l'ordi de jouer")
    ecriture_donnees(plateau, joueur, suivant, gagnant, nulle)
    return redirect('/jeu')


@morpion_app.route("/reset")
def reset():
    # plateau, joueur, suivant, gagnant, nulle = lecture_donnees()
    # initialisation(joueur,suivant)
    return redirect('/')


if __name__ == '__main__':
    morpion_app.run(debug=True)
