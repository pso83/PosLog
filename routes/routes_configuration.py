from flask import request, redirect, render_template
from models.fonction import Fonction
from models.profil import Profil
from models.utilisateur import Utilisateur
from models.peripherique import Peripherique
from models.reseau import Reseau
from models.ticket import Ticket
from models.article import db

def register_configuration_routes(app):
    @app.route('/configuration/systeme', methods=['GET'])
    def configuration_page():
        return render_template('configuration_systeme.html')

    @app.route('/configuration/fonctions', methods=['POST'])
    def add_fonction():
        fonction = request.form.get('fonction')
        if fonction:
            db.session.add(Fonction(fonction=fonction))
            db.session.commit()
        return redirect('/configuration/systeme')

    @app.route('/configuration/profils', methods=['POST'])
    def add_profil():
        nom = request.form.get('nom')
        if nom:
            db.session.add(Profil(nom=nom))
            db.session.commit()
        return redirect('/configuration/systeme')

    @app.route('/configuration/utilisateurs', methods=['POST'])
    def add_utilisateur():
        nom = request.form.get('nom')
        mot_de_passe = request.form.get('mot_de_passe')
        profil_id = request.form.get('profil_id')
        if nom and mot_de_passe:
            db.session.add(Utilisateur(nom=nom, mot_de_passe=mot_de_passe, profil_id=profil_id))
            db.session.commit()
        return redirect('/configuration/systeme')

    @app.route('/configuration/peripheriques', methods=['POST'])
    def add_peripherique():
        nom = request.form.get('nom')
        type_ = request.form.get('type')
        if nom and type_:
            db.session.add(Peripherique(nom=nom, type=type_))
            db.session.commit()
        return redirect('/configuration/systeme')

    @app.route('/configuration/reseau', methods=['POST'])
    def add_reseau_param():
        param = request.form.get('param')
        if param:
            db.session.add(Reseau(param=param))
            db.session.commit()
        return redirect('/configuration/systeme')

    @app.route('/configuration/ticket', methods=['POST'])
    def set_ticket_template():
        template = request.form.get('template')
        if template:
            db.session.add(Ticket(template=template))
            db.session.commit()
        return redirect('/configuration/systeme')
