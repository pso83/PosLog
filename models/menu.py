from extensions import db

class Menu(db.Model):
    __tablename__ = 'menu'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)

    pages = db.relationship('MenuPage', back_populates='menu', cascade="all, delete-orphan")
