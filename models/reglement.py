from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Reglement(db.Model):
    __tablename__ = 'reglements'
    id = db.Column(db.Integer, primary_key=True)
    mode = db.Column(db.String(100), nullable=False)
