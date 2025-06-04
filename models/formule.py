from extensions import db

class Formule(db.Model):
    __tablename__ = 'formules'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prix = db.Column(db.Float, nullable=False)
    composants = db.relationship('FormuleComposant', back_populates='formule', cascade='all, delete-orphan')

class FormuleComposant(db.Model):
    __tablename__ = 'formule_composants'
    id = db.Column(db.Integer, primary_key=True)
    formule_id = db.Column(db.Integer, db.ForeignKey('formules.id'), nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'), nullable=False)

    formule = db.relationship('Formule', back_populates='composants')
    article = db.relationship('Article')



