from extensions import db

class Imprimante(db.Model):
    __tablename__ = 'imprimante'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    emplacement = db.Column(db.String(100), nullable=True)
    type = db.Column(db.String(50), nullable=True)  # Exemple : "ticket", "cuisine"
