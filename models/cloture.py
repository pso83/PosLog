from extensions import db
from datetime import datetime


class Cloture(db.Model):
    __tablename__ = 'clotures'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    responsable = db.Column(db.String(100), nullable=False)
    cloture_le = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
