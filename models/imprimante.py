from extensions import db

class Imprimante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    ip = db.Column(db.String(100))
    port = db.Column(db.Integer)
    emplacement = db.Column(db.String(100))
