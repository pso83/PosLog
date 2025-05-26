from flask import render_template
from models.vente import Vente
from models.vente_detail import VenteDetail
from models.article import db

def register_ticket_routes(app):
    @app.route('/ticket/<int:vente_id>', methods=['GET'])
    def afficher_ticket(vente_id):
        vente = Vente.query.get_or_404(vente_id)
        articles = VenteDetail.query.filter_by(vente_id=vente.id).all()

        # Exemple de données du commerce (à adapter dynamiquement si besoin)
        commerce = {
            'nom': 'Mon Glacier',
            'adresse': '123 Rue de la Glace, 75000 Paris',
            'telephone': '01 23 45 67 89'
        }

        return render_template('ticket_impression.html', vente={
            'date': vente.date,
            'montant_total': vente.montant,
            'mode': vente.mode,
            'articles': articles
        }, commerce=commerce)
