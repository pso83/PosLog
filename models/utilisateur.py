from extensions import db

class Utilisateur(db.Model):
    __tablename__ = 'utilisateurs'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(50), nullable=False)

    profil_id = db.Column(db.Integer, db.ForeignKey('profils.id'))
    clavier_id = db.Column(db.Integer, db.ForeignKey('claviers.id'))
    imprimante_id = db.Column(db.Integer, db.ForeignKey('imprimante.id'), nullable=True)

    mode_vente = db.Column(db.String(20))  # 'ticket', 'table', 'compte'

    profil = db.relationship("Profil", back_populates="utilisateurs")
    clavier = db.relationship("Clavier", backref="utilisateurs")
    imprimante = db.relationship("Imprimante", backref="utilisateur", uselist=False)




