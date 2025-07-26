from extensions import db

class ClavierProduit(db.Model):
    __tablename__ = 'clavier_produit'
    id  = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    # …
    boutons = db.relationship('BoutonProduit', back_populates='clavier', cascade='all, delete-orphan')

class BoutonProduit(db.Model):
    __tablename__   = 'bouton_produit'
    id              = db.Column(db.Integer, primary_key=True)
    clavier_id      = db.Column(db.Integer, db.ForeignKey('clavier_produit.id'), nullable=False)
    position        = db.Column(db.Integer, nullable=False)
    # …
    clavier         = db.relationship('ClavierProduit', back_populates='boutons')
