from flask import request, redirect, render_template, Blueprint, url_for
from models.fonction import Fonction
from models.profil import Profil
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
    def configuration_root():
        return redirect(url_for('configuration_utilisateurs'))

    @app.route('/configuration/systeme', methods=['GET'])
    def configuration_page():
        utilisateurs = Utilisateur.query.all()
        profils = Profil.query.all()
        claviers = Clavier.query.all()
        imprimantes = Imprimante.query.all()

        print("🧪 Profils chargés:", profils)
        print("🧪 Claviers chargés:", claviers)
        print("🧪 Imprimantes chargées:", imprimantes)

        return render_template(
            '/configuration/systeme',
            utilisateurs=utilisateurs,
            utilisateur=None,
            profils=profils,
            claviers=claviers,
            imprimantes=imprimantes,
            profil=None,
            config={}
        )

    @app.route('/configuration/peripheriques')
    def configuration_peripheriques():
        return render_template('configuration_peripheriques.html')

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

    @app.route('/configuration/buzzer_preparation')
    def configuration_buzzer_preparation(): ...

    @app.route('/configuration/buzzer_client')
    def configuration_buzzer_client(): ...

    @app.route('/configuration/ecran_preparation')
    def configuration_ecran_preparation(): ...

    @app.route('/configuration/telecommandes')
    def configuration_telecommandes(): ...

    config_bp = Blueprint('configuration', __name__)

    @config_bp.route("/configuration/imprimantes", methods=["GET", "POST"])
    def configuration_imprimantes():
        if request.method == "POST":
            data = request.form
            imprimante = Imprimante(
                nom=data.get("nom"),
                type=data.get("type"),
                nom_windows=data.get("nom_windows") if data.get("type") == "Windows" else None,
                port_com=data.get("port_com") if data.get("type") == "Série" else None,
                vitesse=data.get("vitesse") if data.get("type") == "Série" else None,
                bit_donnee=data.get("bit_donnee") if data.get("type") == "Série" else None,
                bit_arret=data.get("bit_arret") if data.get("type") == "Série" else None,
                parite=data.get("parite") if data.get("type") == "Série" else None,
                control_flux=data.get("control_flux") if data.get("type") == "Série" else None
            )
            db.session.add(imprimante)
            db.session.commit()
            return redirect(url_for("configuration.configuration_imprimantes"))

        imprimantes = Imprimante.query.all()
        try:
            printers = [p[2] for p in win32print.EnumPrinters(2)]
        except:
            printers = []
        return render_template("configuration_imprimantes.html", imprimantes=imprimantes, printers=printers)
