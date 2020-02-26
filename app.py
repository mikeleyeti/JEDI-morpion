from flask import Flask, render_template, redirect, request
import morpion


morpion_app = Flask(__name__)
plateau, joueur = 2 * [None]


# permet de passer une fonction à Jinja2
@morpion_app.context_processor
def utility_processor():
    def pion(joueur):
        return {morpion.X: u"❌",
                morpion.Vide: u"?",
                morpion.O: u"🔵"}[joueur]

    def est_vide(ligne, colonne):
        return morpion.est_vide(plateau, ligne, colonne)
    return dict(pion=pion, est_vide=est_vide)


@morpion_app.route('/', methods=['GET'])
def nouvelle_partie():
    return render_template('nouvelle_partie.html')


@morpion_app.route('/', methods=['POST'])
def debut_jeu():
    global plateau, joueur

    plateau = morpion.nouveau_plateau()
    joueur = getattr(morpion, request.form['joueur'])
    if request.form['debut'] == "ia":
        jouer_ia()

    return redirect('/jeu')


@morpion_app.route('/jeu')
def affichage():
    return render_template('jeu.html', plateau=plateau)


def fin_partie(joueur_test):
    if morpion.victoire(plateau, joueur_test):
        return render_template("fin_de_partie.html",
                               gagnant=joueur_test,
                               nulle=False,
                               joueur=joueur)
    if morpion.est_plein(plateau):
        return render_template("fin_de_partie.html",
                               gagnant=joueur_test,
                               nulle=True,
                               joueur=joueur)


def jouer_joueur(ligne, colonne):
    morpion.jouer(plateau, joueur, ligne, colonne)
    return fin_partie(joueur)


def jouer_ia():
    joueur_ia = morpion.autre_joueur(joueur)
    morpion.jouer_ia_alea(plateau, joueur_ia)
    return fin_partie(joueur_ia)


@morpion_app.route('/jouer?l=<int:ligne>&c=<int:colonne>')
def jouer(ligne, colonne):
    # on fait jouer le joueur
    res = jouer_joueur(ligne, colonne)
    if res is not None:
        return res

    # puis l'ia
    res = jouer_ia()
    if res is not None:
        return res

    return redirect('/jeu')


@morpion_app.route("/reset")
def reset():
    return redirect('/')


if __name__ == '__main__':
    morpion_app.run(debug=True)
