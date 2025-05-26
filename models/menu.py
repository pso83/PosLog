from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Menu(db.Model):
    __tablename__ = 'menus'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
