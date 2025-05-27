from flask import render_template
from models.vente import Vente
from models.stock import MouvementStock
from models import db
from sqlalchemy import func, desc, case
from datetime import date

def register_dashboard_routes(app):
    @app.route('/dashboard', methods=['GET'])
    def dashboard():
        today = date.today()

        ventes_du_jour = db.session.query(func.sum(Vente.montant)).filter(func.date(Vente.date) == today).scalar() or 0
        total_cb = db.session.query(func.sum(Vente.montant)).filter(func.date(Vente.date) == today, Vente.mode == 'carte').scalar() or 0
        total_cash = db.session.query(func.sum(Vente.montant)).filter(func.date(Vente.date) == today, Vente.mode == 'especes').scalar() or 0

        top_articles = db.session.query(
            MouvementStock.article,
            func.sum(MouvementStock.quantite).label('quantite')
        ).filter(MouvementStock.type_mouvement == 'sortie').group_by(MouvementStock.article).order_by(desc('quantite')).limit(5).all()

        articles_bas_stock = db.session.query(MouvementStock.article).group_by(MouvementStock.article).having(
            func.sum(
                case(
                    (MouvementStock.type_mouvement == 'entree', MouvementStock.quantite),
                    else_=-MouvementStock.quantite
                )
            ) < 5
        ).count()

        dernieres_ventes = db.session.query(Vente).order_by(Vente.date.desc()).limit(5).all()

        return render_template('dashboard_caisse.html',
                               ventes_du_jour=ventes_du_jour,
                               total_cb=total_cb,
                               total_cash=total_cash,
                               top_articles=[{'nom': a[0], 'quantite': int(a[1])} for a in top_articles],
                               articles_bas_stock=articles_bas_stock,
                               dernieres_ventes=dernieres_ventes)
