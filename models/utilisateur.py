from extensions import db
from models.imprimante import Imprimante


class Utilisateur(db.Model):
    __tablename__ = 'utilisateurs'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(50), nullable=False)

    profil_id = db.Column(db.Integer, db.ForeignKey('profils.id'))
    clavier_id = db.Column(db.Integer, db.ForeignKey('claviers.id'))
    mode_vente = db.Column(db.String(20))  # 'ticket', 'table', 'compte'
    imprimante_id = db.Column(db.Integer, db.ForeignKey('imprimantes.id'))

    profil = db.relationship('Profil', backref='utilisateurs')
    clavier = db.relationship('Clavier', backref='utilisateurs')
    imprimante = db.relationship('Imprimante', backref='utilisateurs')
