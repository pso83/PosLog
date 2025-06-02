from extensions import db

class Utilisateur(db.Model):
    __tablename__ = 'utilisateurs'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    mot_de_passe = db.Column(db.String(255), nullable=False)
    profil_id = db.Column(db.Integer, db.ForeignKey('profils.id'))
