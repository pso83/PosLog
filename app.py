from flask import Flask, render_template, redirect, url_for, request, session
from config import Config
from extensions import db
from routes_static_pages import register_static_pages
from flask_login import current_user

# Import obligatoire pour db.create_all()
from models.article import Article
from models.clavier import Clavier
from models.tva import Tva
from models.Groupe import Groupe
from models.Famille import Famille
from models.SousFamille import SousFamille
from models.reglement import Reglement
from models.commentaire import Commentaire
from models.menu import Menu
from models.formule import Formule
from models.fonction import Fonction
from models.profil import Profil
from models.utilisateur import Utilisateur
from models.peripherique import Peripherique
from models.reseau import Reseau
from models.ticket import Ticket
from models.edition import Edition
from models.cloture import Cloture
from models.stock import MouvementStock
from models.vente import Vente
from models.vente_detail import VenteDetail
from models.bouton_clavier import BoutonClavier
from models.imprimante import Imprimante
from routes.routes_auth import auth_bp

# Routes principales
from routes.routes_programmation import register_routes, programmation_bp, register_programmation_routes
from routes.routes_configuration import configuration_bp
from routes.routes_gestion import register_gestion_routes
from routes.routes_stock import register_stock_routes
from routes.routes_dashboard import register_dashboard_routes
from routes.routes_reporting import register_reporting_routes
from routes.routes_ticket import register_ticket_routes
from routes.routes_clavier import register_clavier_routes, clavier_bp
from routes.routes_familles import familles_bp

# Initialisation app Flask
app = Flask(__name__)
app.config.from_object(Config)

# Initialisation
register_static_pages(app)
db.init_app(app)

# Enregistrement des routes (uniques)
register_routes(app)
app.register_blueprint(configuration_bp)

register_gestion_routes(app)
register_stock_routes(app)
register_dashboard_routes(app)
register_reporting_routes(app)
register_ticket_routes(app)
register_programmation_routes(app)
register_clavier_routes(app)

# Enregistrement des Blueprints (attention aux doublons !)
app.register_blueprint(programmation_bp, url_prefix="/programmer")
app.register_blueprint(clavier_bp, url_prefix="/clavier")
app.register_blueprint(familles_bp)
#app.register_blueprint(configuration_bp)

app.register_blueprint(auth_bp)

# Route racine
@app.route('/')
def loading():
    return render_template('loading.html')

@app.context_processor
def inject_user():
    return dict(current_user=current_user)

# Lancement
if __name__ == '__main__':
    with app.app_context():
        print("🔁 Création des tables si elles n’existent pas...")
        db.create_all()
        print("📋 Tables existantes :", db.inspect(db.engine).get_table_names())
    app.run(debug=True)
