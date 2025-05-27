from models import db

class Tva(db.Model):
    __tablename__ = 'tva'

    id = db.Column(db.Integer, primary_key=True)
    taux = db.Column(db.String(10), nullable=False)
