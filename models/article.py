from extensions import db
from models.menu_page_articles import menu_page_articles

class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    nom_article = db.Column(db.String(100), nullable=False)
    prix_1 = db.Column(db.Float)
    prix_2 = db.Column(db.Float)
    prix_3 = db.Column(db.Float)
    prix_4 = db.Column(db.Float)
    prix_5 = db.Column(db.Float)
    tva_id = db.Column(db.String(10))
    prix_manuel = db.Column(db.Boolean, default=False)
    vendu_au_poids = db.Column(db.Boolean, default=False)
    avec_code_barre = db.Column(db.Boolean, default=False)
    eligible_fidelite = db.Column(db.Boolean, default=False)
    retour_autorise = db.Column(db.Boolean, default=False)
    avoir_autorise = db.Column(db.Boolean, default=False)
    gere_stock = db.Column(db.Boolean, default=False)
    vendu_en_negatif = db.Column(db.Boolean, default=False)
    hors_ca = db.Column(db.Boolean, default=False)
    est_formule = db.Column(db.Boolean, default=False)
    composant_menu = db.Column(db.Boolean, default=False)
    composant_formule = db.Column(db.Boolean, default=False)
    appel_commentaire = db.Column(db.Boolean, default=False)
    imprimable_preparation = db.Column(db.Boolean, default=False)
    invisible_telecommande = db.Column(db.Boolean, default=False)
    vente_a_distance = db.Column(db.Boolean, default=False)
    gere_heure = db.Column(db.Boolean, default=False)
    depot_vente = db.Column(db.Boolean, default=False)
    gere_sav = db.Column(db.Boolean, default=False)
    commentaire_id = db.Column(db.Integer, db.ForeignKey('commentaires.id'))  # <== C'est ça qui manque
    commentaire = db.relationship('Commentaire', backref='articles')

    groupe_id = db.Column(db.Integer, db.ForeignKey('groupes.id'))
    famille_id = db.Column(db.Integer, db.ForeignKey('familles.id'))
    sous_famille_id = db.Column(db.Integer, db.ForeignKey('sous_familles.id'))

    groupe = db.relationship('Groupe')
    famille = db.relationship('Famille')
    sous_famille = db.relationship('SousFamille')

    menu_pages = db.relationship(
        'MenuPage',
        secondary=menu_page_articles,
        back_populates='articles'
    )





