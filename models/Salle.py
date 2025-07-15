from extensions import db

class Salle(db.Model):
    __tablename__ = 'salles'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    plan_type = db.Column(db.String(50), nullable=False)

    tables = db.relationship('TablePlan', back_populates='salle', cascade='all, delete-orphan')

    elements = db.relationship('TablePlan', back_populates='salle', cascade='all, delete-orphan')

    # on ne stocke pas le .png en base, on le génère
    @property
    def plan_image(self):
        return f"{self.plan_type}.png"