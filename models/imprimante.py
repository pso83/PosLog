from extensions import db

class Imprimante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), nullable=False)  # "Série" ou "Windows"
    nom = db.Column(db.String(100), nullable=False)

    # Champs spécifiques à Windows
    nom_windows = db.Column(db.String(100), nullable=True)

    # Champs spécifiques à Série
    port_com = db.Column(db.Integer, nullable=True)
    vitesse = db.Column(db.Integer, nullable=True)
    bit_donnee = db.Column(db.Integer, nullable=True)
    bit_arret = db.Column(db.String(4), nullable=True)  # "1", "1.5", "2"
    parite = db.Column(db.String(10), nullable=True)    # "Aucun", "Paire", "Impaire"
    controle_flux = db.Column(db.String(20), nullable=True)  # "Aucun contrôl", "RTS/CTS", "XON/XOFF"
