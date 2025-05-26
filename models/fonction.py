from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Fonction(db.Model):
    __tablename__ = 'fonctions'
    id = db.Column(db.Integer, primary_key=True)
    fonction = db.Column(db.String(100), nullable=False)
