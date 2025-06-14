from extensions import db

class Imprimante(db.Model):
    __tablename__ = 'imprimante'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(20))  # Windows ou Série
    nom_windows = db.Column(db.String(200), nullable=True)
    port_com = db.Column(db.Integer)
    vitesse = db.Column(db.String(10), nullable=True)
    bit_donnee = db.Column(db.String(10), nullable=True)
    bit_arret = db.Column(db.String(10), nullable=True)
    parite = db.Column(db.String(20), nullable=True)
    controle_flux = db.Column(db.String(20), nullable=True)

    # Relation avec les utilisateurs (une imprimante peut être liée à plusieurs utilisateurs)
    utilisateurs = db.relationship(
        'Utilisateur',
        back_populates='imprimante',
        foreign_keys='Utilisateur.imprimante_id'
    )
