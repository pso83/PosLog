from flask_sqlalchemy import SQLAlchemy
from models import db

class Formule(db.Model):
    __tablename__ = 'formules'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
