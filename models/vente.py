from extensions import db
from datetime import datetime

from models import db

class Vente(db.Model):
    __tablename__ = 'ventes'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    montant = db.Column(db.Float, nullable=False)
    mode = db.Column(db.String(50), nullable=False)

