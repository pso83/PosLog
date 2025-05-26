from flask import Flask, render_template, request, redirect
from models.article import db
from models.clavier import Clavier
from models.tva import Tva
from models.groupe import Groupe
from models.famille import Famille
from models.sous_famille import SousFamille
from models.reglement import Reglement
from models.commentaire import Commentaire
from models.menu import Menu
from models.formule import Formule

def register_routes(app):
    @app.route('/programmation/elements', methods=['GET'])
    def show_programmation_elements():
        return render_template('programmation_elements.html')

    @app.route('/programmation/claviers', methods=['POST'])
    def add_clavier():
        nom = request.form.get('nom')
        if nom:
            db.session.add(Clavier(nom=nom))
            db.session.commit()
        return redirect('/programmation/elements')

    @app.route('/programmation/tva', methods=['POST'])
    def add_tva():
        label = request.form.get('label')
        taux = request.form.get('taux')
        if label and taux:
            db.session.add(Tva(label=label, taux=taux))
            db.session.commit()
        return redirect('/programmation/elements')

    @app.route('/programmation/groupes', methods=['POST'])
    def add_groupe():
        nom = request.form.get('nom')
        if nom:
            db.session.add(Groupe(nom=nom))
            db.session.commit()
        return redirect('/programmation/elements')

    @app.route('/programmation/familles', methods=['POST'])
    def add_famille():
        nom = request.form.get('nom')
        if nom:
            db.session.add(Famille(nom=nom))
            db.session.commit()
        return redirect('/programmation/elements')

    @app.route('/programmation/sousfamilles', methods=['POST'])
    def add_sous_famille():
        nom = request.form.get('nom')
        if nom:
            db.session.add(SousFamille(nom=nom))
            db.session.commit()
        return redirect('/programmation/elements')

    @app.route('/programmation/reglements', methods=['POST'])
    def add_reglement():
        mode = request.form.get('mode')
        if mode:
            db.session.add(Reglement(mode=mode))
            db.session.commit()
        return redirect('/programmation/elements')

    @app.route('/programmation/commentaires', methods=['POST'])
    def add_commentaire():
        texte = request.form.get('texte')
        if texte:
            db.session.add(Commentaire(texte=texte))
            db.session.commit()
        return redirect('/programmation/elements')

    @app.route('/programmation/menus', methods=['POST'])
    def add_menu():
        nom = request.form.get('nom')
        if nom:
            db.session.add(Menu(nom=nom))
            db.session.commit()
        return redirect('/programmation/elements')

    @app.route('/programmation/formules', methods=['POST'])
    def add_formule():
        nom = request.form.get('nom')
        if nom:
            db.session.add(Formule(nom=nom))
            db.session.commit()
        return redirect('/programmation/elements')
