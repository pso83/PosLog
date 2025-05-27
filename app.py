from flask import Flask
from config import Config
from models.article import db
from routes_static_pages import register_static_pages


# Importation explicite de tous les modèles (obligatoire pour db.create_all)
from models.article import Article
from models.clavier import Clavier
from models.tva import Tva
from models.groupe import Groupe
from models.famille import Famille
from models.sous_famille import SousFamille
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

# Enregistrement des routes
from routes.routes_programmation import register_routes
from routes.routes_configuration import register_configuration_routes
from routes.routes_gestion import register_gestion_routes
from routes.routes_stock import register_stock_routes
from routes.routes_dashboard import register_dashboard_routes
from routes.routes_reporting import register_reporting_routes
from routes.routes_ticket import register_ticket_routes
from routes.routes_programmation import register_programmation_routes


app = Flask(__name__)
app.config.from_object(Config)
register_static_pages(app)
db.init_app(app)

# Routes d’enregistrement
register_routes(app)
register_configuration_routes(app)
register_gestion_routes(app)
register_stock_routes(app)
register_dashboard_routes(app)
register_reporting_routes(app)
register_ticket_routes(app)
register_programmation_routes(app)

@app.route('/')
def index():
    return '<h3>Bienvenue sur le système d’encaissement</h3><a href="/dashboard">Accéder au tableau de bord</a>'

if __name__ == '__main__':
    with app.app_context():
        print("🔁 Création des tables si elles n’existent pas...")
        db.create_all()
        print("📋 Tables existantes :", db.inspect(db.engine).get_table_names())
    app.run(debug=True)
