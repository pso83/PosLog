from extensions import db

class TablePlan(db.Model):
    __tablename__ = 'table_plan'
    id = db.Column(db.Integer, primary_key=True)
    salle_id = db.Column(db.Integer, db.ForeignKey('salles.id'), nullable=False)  # ✅ ici "salles.id"
    type_element = db.Column(db.String(50))
    image = db.Column(db.String(200))
    numero = db.Column(db.String(20))
    nb_places = db.Column(db.Integer)
    x = db.Column(db.Float)
    y = db.Column(db.Float)
    rotation = db.Column(db.Float, default=0)

    salle = db.relationship('Salle', back_populates='elements')
