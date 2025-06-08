from extensions import db
from models.article import Article
from models.bouton_clavier import BoutonClavier

class Clavier(db.Model):
    __tablename__ = 'claviers'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(255))

    boutons = db.relationship("BoutonClavier", backref="clavier", lazy="joined")


class ClavierBouton(db.Model):
    __tablename__ = 'clavier_boutons'
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.Integer, nullable=False)
    clavier_id = db.Column(db.Integer, db.ForeignKey('claviers.id'), nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'))

    article = db.relationship('Article', backref='boutons')
