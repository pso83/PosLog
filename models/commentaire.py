from extensions import db

class Commentaire(db.Model):
    __tablename__ = 'commentaires'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    elements = db.relationship('ElementCommentaire', backref='commentaire', cascade='all, delete-orphan')

class ElementCommentaire(db.Model):
    __tablename__ = 'element_commentaire'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    commentaire_id = db.Column(db.Integer, db.ForeignKey('commentaires.id'), nullable=False)
