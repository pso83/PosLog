from models import db

class Famille(db.Model):
    __tablename__ = 'familles'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    groupe_id = db.Column(db.Integer, db.ForeignKey('groupes.id'), nullable=False)

    sous_familles = db.relationship('SousFamille', backref='famille', lazy=True)
