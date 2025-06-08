from extensions import db

class BoutonClavier(db.Model):
    __tablename__ = 'boutons_clavier'

    id = db.Column(db.Integer, primary_key=True)
    clavier_id = db.Column(db.Integer, db.ForeignKey('claviers.id'))
    position = db.Column(db.Integer, nullable=False)

    # Associations multiples possibles
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'), nullable=True)
    fonction_id = db.Column(db.Integer, db.ForeignKey('fonctions.id'), nullable=True)
    sous_clavier_id = db.Column(db.Integer, db.ForeignKey('claviers.id'), nullable=True)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'), nullable=True)
    formule_id = db.Column(db.Integer, db.ForeignKey('formules.id'), nullable=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateurs.id'), nullable=True)
    reglement_id = db.Column(db.Integer, db.ForeignKey('reglements.id'), nullable=True)
    commentaire_id = db.Column(db.Integer, db.ForeignKey('commentaires.id'), nullable=True)

    # Relations
    article = db.relationship("Article", lazy='joined')
    fonction = db.relationship("Fonction", lazy='joined')
    clavier = db.relationship("Clavier", backref="boutons", foreign_keys='BoutonClavier.clavier_id')
    menu = db.relationship("Menu", lazy='joined')
    formule = db.relationship("Formule", lazy='joined')
    utilisateur = db.relationship("Utilisateur", lazy='joined')
    reglement = db.relationship("Reglement", lazy='joined')
    commentaire = db.relationship("Commentaire", lazy='joined')



