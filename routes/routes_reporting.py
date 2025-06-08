from flask import request, render_template, send_file
from models.vente import Vente
from extensions import db
from io import StringIO
import csv
from datetime import datetime

def register_reporting_routes(app):
    @app.route('/reporting', methods=['GET'])
    def reporting():
        date_debut = request.args.get('date_debut')
        date_fin = request.args.get('date_fin')
        mode = request.args.get('mode')

        query = db.session.query(Vente)

        if date_debut:
            query = query.filter(Vente.date >= date_debut)
        if date_fin:
            query = query.filter(Vente.date <= date_fin + ' 23:59:59')
        if mode:
            query = query.filter(Vente.mode == mode)

        ventes = query.order_by(Vente.date.desc()).all()
        return render_template('reporting_ventes.html', ventes=ventes)

    @app.route('/reporting/export', methods=['GET'])
    def export_ventes_csv():
        date_debut = request.args.get('date_debut')
        date_fin = request.args.get('date_fin')
        mode = request.args.get('mode')

        query = db.session.query(Vente)

        if date_debut:
            query = query.filter(Vente.date >= date_debut)
        if date_fin:
            query = query.filter(Vente.date <= date_fin + ' 23:59:59')
        if mode:
            query = query.filter(Vente.mode == mode)

        ventes = query.order_by(Vente.date.desc()).all()

        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(['Date', 'Montant (€)', 'Mode de paiement'])

        for v in ventes:
            writer.writerow([v.date.strftime('%d/%m/%Y %H:%M'), f"{v.montant:.2f}", v.mode])

        output.seek(0)
        return send_file(output, mimetype='text/csv', as_attachment=True, download_name='reporting_ventes.csv')
