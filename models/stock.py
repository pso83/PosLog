from extensions import db
from datetime import datetime

from models import db

class MouvementStock(db.Model):
    __tablename__ = 'mouvements_stock'
    id = db.Column(db.Integer, primary_key=True)
    article = db.Column(db.String(255), nullable=False)
    quantite = db.Column(db.Integer, nullable=False)
    type_mouvement = db.Column(db.String(10), nullable=False)  # 'entree' ou 'sortie'
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
