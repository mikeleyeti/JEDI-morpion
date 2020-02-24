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
    if suivant == 'ia':
        plateau = IA_niveau_0(plateau, joueur)
        suivant = 'humain'
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
# todo : gérer la fin de partie : nulle et victoire
