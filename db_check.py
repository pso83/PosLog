from flask import Flask
from config import Config
from models.article import db

# Importation des modèles
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

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    try:
        print("🔍 Connexion à la base de données...")
        connection = db.engine.connect()
        print("✅ Connexion réussie à la base : ma_caisse")
        print("📋 Tables existantes :", db.inspect(db.engine).get_table_names())

        print("🔁 Création des tables manquantes...")
        db.create_all()
        print("✅ Toutes les tables sont en place.")
    except Exception as e:
        print("❌ Erreur lors de la connexion ou de la création des tables :", e)
