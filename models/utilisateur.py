from extensions import db

class Utilisateur(db.Model):
    __tablename__ = 'utilisateurs'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))
    code = db.Column(db.String(50))
    profil_id = db.Column(db.Integer, db.ForeignKey('profils.id'))
    clavier_id = db.Column(db.Integer, db.ForeignKey('claviers.id'))
    mode_vente = db.Column(db.String(20))
    imprimante_id = db.Column(db.Integer, db.ForeignKey('imprimante.id'), nullable=True)

    # Relations
    profil = db.relationship('Profil', back_populates='utilisateurs')
    clavier = db.relationship('Clavier', back_populates='utilisateurs')
    imprimante = db.relationship(
        'Imprimante',
        back_populates='utilisateurs',
        foreign_keys=[imprimante_id]
    )
