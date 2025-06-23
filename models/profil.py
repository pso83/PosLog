from extensions import db

class Profil(db.Model):
    __tablename__ = 'profils'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)

    # Accès
    acces_vente = db.Column(db.Boolean, default=False)
    acces_programmation = db.Column(db.Boolean, default=False)
    acces_gestion = db.Column(db.Boolean, default=False)
    acces_configuration = db.Column(db.Boolean, default=False)
    acces_clients = db.Column(db.Boolean, default=False)

    # Autorisations
    offrir = db.Column(db.Boolean, default=False)
    annuler_ligne = db.Column(db.Boolean, default=False)
    annuler_commande_avant_encaissement = db.Column(db.Boolean, default=False)
    annuler_ticket_encaisse = db.Column(db.Boolean, default=False)
    annuler_ticket_attente = db.Column(db.Boolean, default=False)
    remise = db.Column(db.Boolean, default=False)
    changement_tarif = db.Column(db.Boolean, default=False)
    mise_en_attente = db.Column(db.Boolean, default=False)
    transfert_table = db.Column(db.Boolean, default=False)
    transfert_compte = db.Column(db.Boolean, default=False)
    modifier_couverts = db.Column(db.Boolean, default=False)

    # Création
    creer_utilisateur = db.Column(db.Boolean, default=False)
    creer_client = db.Column(db.Boolean, default=False)
    creer_carte_cadeau = db.Column(db.Boolean, default=False)
    creer_avoir = db.Column(db.Boolean, default=False)

    # Modification
    modifier_utilisateur = db.Column(db.Boolean, default=False)
    modifier_client = db.Column(db.Boolean, default=False)
    modifier_carte_cadeau = db.Column(db.Boolean, default=False)
    modifier_avoir = db.Column(db.Boolean, default=False)

    # Suppression
    supprimer_utilisateur = db.Column(db.Boolean, default=False)
    supprimer_client = db.Column(db.Boolean, default=False)
    supprimer_carte_cadeau = db.Column(db.Boolean, default=False)
    supprimer_avoir = db.Column(db.Boolean, default=False)

    timeout = db.Column(db.Integer, default=5)

    utilisateurs = db.relationship('Utilisateur', back_populates='profil')
