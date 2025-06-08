from flask import request, redirect, render_template
from models.edition import Edition
from models.cloture import Cloture
from extensions import db
from datetime import datetime

def register_gestion_routes(app):
    @app.route('/gestion/caisse', methods=['GET'])
    def gestion_caisse_page():
        return render_template('gestion_caisse.html')

    @app.route('/gestion/edition', methods=['POST'])
    def generer_edition():
        date = request.form.get('date')
        if date:
            edition = Edition(date=date, genere_le=datetime.utcnow())
            db.session.add(edition)
            db.session.commit()
        return redirect('/gestion/caisse')

    @app.route('/gestion/cloture', methods=['POST'])
    def effectuer_cloture():
        date = request.form.get('date')
        responsable = request.form.get('responsable')
        if date and responsable:
            cloture = Cloture(date=date, responsable=responsable, cloture_le=datetime.utcnow())
            db.session.add(cloture)
            db.session.commit()
        return redirect('/gestion/caisse')
