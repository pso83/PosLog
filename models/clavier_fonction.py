from extensions import db

class ClavierFonction(db.Model):
    __tablename__ = 'clavier_fonction'
    id  = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    # …
    boutons = db.relationship('BoutonFonction', back_populates='clavier', cascade='all, delete-orphan')

class BoutonFonction(db.Model):
    __tablename__   = 'bouton_fonction'
    id              = db.Column(db.Integer, primary_key=True)
    clavier_id      = db.Column(db.Integer, db.ForeignKey('clavier_fonction.id'), nullable=False)
    position        = db.Column(db.Integer, nullable=False)
    # …
    clavier         = db.relationship('ClavierFonction', back_populates='boutons')
