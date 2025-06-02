from extensions import db

class BoutonClavier(db.Model):
    __tablename__ = 'boutons_clavier'  # ← ici le nom exact de ta table en base

    id = db.Column(db.Integer, primary_key=True)
    clavier_id = db.Column(db.Integer, db.ForeignKey('claviers.id'), nullable=False)
    position = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(50))
    element_id = db.Column(db.Integer)
    label = db.Column(db.String(100))
    couleur = db.Column(db.String(20))
    image = db.Column(db.String(255))
    masquer_texte = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'position': self.position,
            'type': self.type,
            'element_id': self.element_id,
            'label': self.label,
            'couleur': self.couleur,
            'image': self.image,
            'masquer_texte': self.masquer_texte
        }
