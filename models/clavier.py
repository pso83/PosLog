from models import db
from models.article import Article

class Clavier(db.Model):
    __tablename__ = 'claviers'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)

    boutons = db.relationship('ClavierBouton', backref='clavier', cascade='all, delete-orphan')


class ClavierBouton(db.Model):
    __tablename__ = 'clavier_boutons'
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.Integer, nullable=False)
    clavier_id = db.Column(db.Integer, db.ForeignKey('claviers.id'), nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'))

    article = db.relationship('Article', backref='boutons')
