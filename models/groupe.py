from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Groupe(db.Model):
    __tablename__ = 'groupes'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
