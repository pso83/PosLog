from extensions import db

class TicketConfig(db.Model):
    __tablename__ = 'ticket_config'
    id = db.Column(db.Integer, primary_key=True)
    nom_commerce = db.Column(db.String(100))
    adresse = db.Column(db.Text)
    siret = db.Column(db.String(20))
    tva_intra = db.Column(db.String(50))
    entete_ligne1 = db.Column(db.String(100))
    entete_ligne2 = db.Column(db.String(100))
    pied_ligne1 = db.Column(db.String(100))
    pied_ligne2 = db.Column(db.String(100))
    pied_ligne3 = db.Column(db.String(100))
    pied_ligne4 = db.Column(db.String(100))
