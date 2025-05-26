from flask_sqlalchemy import SQLAlchemy
from models import db

class Peripherique(db.Model):
    __tablename__ = 'peripheriques'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)
