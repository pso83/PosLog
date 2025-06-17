from extensions import db

class Salle(db.Model):
    __tablename__ = 'salles'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    plan_type = db.Column(db.Enum('restaurant', 'bar', 'plage'), nullable=False)

    tables = db.relationship('TablePlan', back_populates='salle', cascade='all, delete-orphan')
