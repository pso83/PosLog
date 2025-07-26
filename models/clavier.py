from extensions import db
from models.bouton_clavier import BoutonClavier

class Clavier(db.Model):
    __tablename__ = 'claviers'

    id    = db.Column(db.Integer, primary_key=True)
    nom   = db.Column(db.String(100), nullable=False)
    side  = db.Column(
              db.Enum('main','function', name='clavier_sides'),
              nullable=False,
              default='main'
            )

    # On précise ici que cette relation utilise bien la colonne BoutonClavier.clavier_id
    boutons = db.relationship(
        'BoutonClavier',
        back_populates='clavier',
        foreign_keys=[BoutonClavier.clavier_id],
        cascade='all, delete-orphan'
    )

    # relations inverse de Utilisateur, inchangées après votre dernier correctif
    main_users     = db.relationship(
                        'Utilisateur',
                        back_populates='clavier',
                        foreign_keys='Utilisateur.clavier_id'
                     )
    function_users = db.relationship(
                        'Utilisateur',
                        back_populates='function_clavier',
                        foreign_keys='Utilisateur.function_clavier_id'
                     )