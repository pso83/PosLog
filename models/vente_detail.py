from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class VenteDetail(db.Model):
    __tablename__ = 'vente_details'
    id = db.Column(db.Integer, primary_key=True)
    vente_id = db.Column(db.Integer, db.ForeignKey('ventes.id'), nullable=False)
    nom = db.Column(db.String(255), nullable=False)
    quantite = db.Column(db.Integer, nullable=False)
    prix_total = db.Column(db.Float, nullable=False)
