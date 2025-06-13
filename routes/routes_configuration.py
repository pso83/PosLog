from flask import request, redirect, render_template, Blueprint, url_for
from models.fonction import Fonction
from models.profil import Profil
from models.ticket_config import TicketConfig
from models.utilisateur import Utilisateur
from models.peripherique import Peripherique
from models.reseau import Reseau
from models.ticket import Ticket
from models.imprimante import Imprimante
from models.clavier import Clavier
from extensions import db
import win32print

def register_configuration_routes(app):
    @app.route('/configuration')
    def configuration_home():
        return render_template('configuration_main.html')

    @app.route('/configuration/utilisateurs')
    def configuration_utilisateurs():
        return render_template("configuration_utilisateurs.html")

    @app.route('/configuration/profils', methods=['GET', 'POST'])
    def configuration_profils():
        if request.method == 'POST':
            nom = request.form.get('nom')
            if nom:
                db.session.add(Profil(nom=nom))
                db.session.commit()
                flash("Profil ajouté avec succès.", "success")
            return redirect(url_for('configuration_profils'))

        profils = Profil.query.all()
        return render_template('configuration_profils.html', profils=profils)

    @app.route('/configuration/imprimantes')
    def configuration_imprimantes():
        return render_template("configuration_imprimantes.html")

    @app.route('/configuration/reseau')
    def configuration_reseau():
        return render_template("configuration_reseau.html")

    @app.route('/configuration/ticket')
    def configuration_ticket():
        return render_template("configuration_ticket.html")

    @app.route('/configuration/peripheriques')
    def configuration_peripheriques():
        return render_template("configuration_peripheriques.html")

