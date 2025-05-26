from flask_sqlalchemy import SQLAlchemy
from models import db

class Reseau(db.Model):
    __tablename__ = 'reseau'
    id = db.Column(db.Integer, primary_key=True)
    param = db.Column(db.String(255), nullable=False)
