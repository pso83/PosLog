from models import db

class SousFamille(db.Model):
    __tablename__ = 'sous_familles'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    famille_id = db.Column(db.Integer, db.ForeignKey('familles.id'), nullable=False)
