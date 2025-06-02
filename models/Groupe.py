from models import db

class Groupe(db.Model):
    __tablename__ = 'groupes'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)

    familles = db.relationship('Famille', backref='groupe', lazy=True)
