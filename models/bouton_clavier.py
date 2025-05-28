from flask_sqlalchemy import SQLAlchemy
from models import db

class BoutonClavier(db.Model):
    __tablename__ = 'boutons_clavier'

    id = db.Column(db.Integer, primary_key=True)
    clavier_id = db.Column(db.Integer, nullable=False)
    position = db.Column(db.Integer, nullable=False)  # de 1 à 55
    type = db.Column(db.String(20), nullable=False)   # article, menu, etc.
    element_id = db.Column(db.Integer, nullable=True) # identifiant de l’élément
    label = db.Column(db.String(50), nullable=True)
    couleur = db.Column(db.String(7), nullable=True)  # format HEX (#RRGGBB)
    image = db.Column(db.String(255), nullable=True)  # chemin image
    masquer_texte = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            "position": self.position,
            "type": self.type,
            "element_id": self.element_id,
            "label": self.label,
            "couleur": self.couleur,
            "image": self.image,
            "masquer_texte": self.masquer_texte
        }
