from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Famille(db.Model):
    __tablename__ = 'familles'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
