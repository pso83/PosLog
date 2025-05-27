from models import db

class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prix1 = db.Column(db.Float)
    prix2 = db.Column(db.Float)
    prix3 = db.Column(db.Float)
    prix4 = db.Column(db.Float)
    prix5 = db.Column(db.Float)
    tva = db.Column(db.String(10))

    prix_manuel = db.Column(db.Boolean, default=False)
    article_vendu_au_poids = db.Column(db.Boolean, default=False)
    code_barre = db.Column(db.Boolean, default=False)
    eligible_fidelite = db.Column(db.Boolean, default=False)
    gere_en_stock = db.Column(db.Boolean, default=False)
