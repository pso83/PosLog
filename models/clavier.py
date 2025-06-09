from extensions import db

class Clavier(db.Model):
    __tablename__ = 'claviers'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)

    # Relation avec les boutons affectés à ce clavier
    boutons = db.relationship(
        "BoutonClavier",
        back_populates="clavier",
        foreign_keys="BoutonClavier.clavier_id",
        cascade="all, delete-orphan"
    )