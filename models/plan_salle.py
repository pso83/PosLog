from extensions import db

class TablePlan(db.Model):
    __tablename__ = 'table_plan'
    id           = db.Column(db.Integer, primary_key=True)
    salle_id     = db.Column(db.Integer, db.ForeignKey('salles.id'), nullable=False)
    type_element = db.Column(db.String(50), nullable=False)
    image        = db.Column(db.String(200), nullable=False)
    numero       = db.Column(db.Integer, nullable=True)
    nb_places    = db.Column(db.Integer, nullable=True)
    x            = db.Column(db.Float,   nullable=False)
    y            = db.Column(db.Float,   nullable=False)
    rotation     = db.Column(db.Float,   nullable=False, default=0)
    salle        = db.relationship('Salle', back_populates='elements')
