from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Vente(db.Model):
    __tablename__ = 'ventes'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    montant = db.Column(db.Float, nullable=False)
    mode = db.Column(db.String(50), nullable=False)  # ex: 'espèces', 'carte'
