from flask_sqlalchemy import SQLAlchemy
from models import db

class Commentaire(db.Model):
    __tablename__ = 'commentaires'
    id = db.Column(db.Integer, primary_key=True)
    texte = db.Column(db.Text, nullable=False)
