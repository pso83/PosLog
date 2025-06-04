from extensions import db

class Imprimante(db.Model):
    __tablename__ = 'imprimantes'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
