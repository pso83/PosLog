from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Tva(db.Model):
    __tablename__ = 'tva'
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(100), nullable=False)
    taux = db.Column(db.Float, nullable=False)
