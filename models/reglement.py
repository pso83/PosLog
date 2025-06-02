from extensions import db

class Reglement(db.Model):
    __tablename__ = 'reglements'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    montant = db.Column(db.Float, nullable=True)

    reglement_connecte = db.Column(db.Boolean, default=False)
    saisie_quantite = db.Column(db.Boolean, default=False)
    saisie_montant = db.Column(db.Boolean, default=False)
    valeur_programmee = db.Column(db.Boolean, default=False)
    pas_de_rendu = db.Column(db.Boolean, default=False)
    pourboire = db.Column(db.Boolean, default=False)
    avoir = db.Column(db.Boolean, default=False)

