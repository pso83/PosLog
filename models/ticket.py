from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Ticket(db.Model):
    __tablename__ = 'ticket'
    id = db.Column(db.Integer, primary_key=True)
    template = db.Column(db.Text, nullable=False)
