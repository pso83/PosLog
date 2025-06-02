from extensions import db
from datetime import datetime


class Edition(db.Model):
    __tablename__ = 'editions'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    genere_le = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
