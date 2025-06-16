from extensions import db

class TablePlan(db.Model):
    __tablename__ = 'table_plan'

    id = db.Column(db.Integer, primary_key=True)
    plan_type = db.Column(db.Enum('restaurant', 'bar', 'plage'), nullable=False, default='restaurant')
    type_element = db.Column(db.String(20), nullable=False)  # 'table', 'tabouret', 'matelas', etc.
    nom_element = db.Column(db.String(50), nullable=True)    # ex: "Matelas" pour plage
    numero = db.Column(db.Integer, nullable=False)
    nb_places = db.Column(db.Integer, nullable=True)         # Non obligatoire pour les bars
    forme = db.Column(db.Enum('ronde', 'carrée', 'rectangulaire'), nullable=False, default='ronde')
    x = db.Column(db.Float, nullable=True)
    y = db.Column(db.Float, nullable=True)
    largeur = db.Column(db.Float, nullable=True)
    hauteur = db.Column(db.Float, nullable=True)
