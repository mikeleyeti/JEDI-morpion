from flask import Flask, render_template, redirect, url_for, request
import json

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


def manche(plateau, ligne, colonne):
    pass


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
    return render_template('jeu.html', plateau=plateau)


@morpion_app.route('/jouer/<int:ligne>/<int:colonne>')
def jouer(ligne, colonne):
    plateau, joueur, suivant, gagnant, nulle = lecture_donnees()
    # # A modifier : faire appel à une fonction jouer qui teste la case...
    if joueur == 'X':
        plateau[ligne][colonne] = -1
        joueur = 'O'
    else:
        plateau[ligne][colonne] = 1
        joueur = 'X'
    ecriture_donnees(plateau, joueur, suivant, gagnant, nulle)
    return redirect('/jeu')


@morpion_app.route("/reset")
def reset():
    # plateau, joueur, suivant, gagnant, nulle = lecture_donnees()
    # initialisation(joueur,suivant)
    return redirect('/')


if __name__ == '__main__':
    morpion_app.run(debug=True)
