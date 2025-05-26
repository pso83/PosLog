from flask_sqlalchemy import SQLAlchemy
from models import db

class Clavier(db.Model):
    __tablename__ = 'claviers'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
