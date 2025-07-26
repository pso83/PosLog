from extensions import db

class BoutonClavier(db.Model):
    __tablename__ = 'boutons_clavier'

    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.Integer, nullable=False)
    clavier_id = db.Column(db.Integer, db.ForeignKey('claviers.id'), nullable=False)

    # back_populates avec Clavier
    clavier = db.relationship(
        'Clavier',
        back_populates='boutons',
        foreign_keys=[clavier_id]
    )

    # les clés étrangères selon les types de bouton :
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'))
    fonction_id = db.Column(db.Integer, db.ForeignKey('fonctions.id'))
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'))
    formule_id = db.Column(db.Integer, db.ForeignKey('formules.id'))
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateurs.id'))
    reglement_id = db.Column(db.Integer, db.ForeignKey('reglements.id'))
    commentaire_id = db.Column(db.Integer, db.ForeignKey('commentaires.id'))
    sous_clavier_id = db.Column(db.Integer, db.ForeignKey('claviers.id'))

    # champs visuels
    couleur = db.Column(db.String(20))
    text_color = db.Column(db.String(20), nullable=True)
    image = db.Column(db.String(255))
    masquer_texte = db.Column(db.Boolean, default=False)

    # relations vers les entités
    article = db.relationship("Article")
    fonction = db.relationship("Fonction")
    menu = db.relationship("Menu")
    formule = db.relationship("Formule")
    utilisateur = db.relationship("Utilisateur")
    reglement = db.relationship("Reglement")
    commentaire = db.relationship("Commentaire")

    sous_clavier = db.relationship(
        'Clavier',
        foreign_keys=[sous_clavier_id]
    )

    element_type = db.Column(db.String(50))

