from flask import request, redirect, render_template
from models.stock import MouvementStock
from extensions import db
from datetime import datetime

def register_stock_routes(app):
    @app.route('/stocks', methods=['GET'])
    def stock_page():
        return render_template('gestion_stocks.html')

    @app.route('/stocks/entree', methods=['POST'])
    def stock_entree():
        article = request.form.get('article')
        quantite = request.form.get('quantite')
        if article and quantite:
            m = MouvementStock(article=article, quantite=int(quantite), type_mouvement='entree', date=datetime.utcnow())
            db.session.add(m)
            db.session.commit()
        return redirect('/stocks')

    @app.route('/stocks/sortie', methods=['POST'])
    def stock_sortie():
        article = request.form.get('article')
        quantite = request.form.get('quantite')
        if article and quantite:
            m = MouvementStock(article=article, quantite=int(quantite), type_mouvement='sortie', date=datetime.utcnow())
            db.session.add(m)
            db.session.commit()
        return redirect('/stocks')
