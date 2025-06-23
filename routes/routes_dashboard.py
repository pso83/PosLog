
from flask import render_template, session, redirect, url_for
from models.vente import Vente
from models.stock import MouvementStock
from extensions import db
from sqlalchemy import func, desc, case
from utils.auth import login_required
from datetime import date
from functools import wraps
from datetime import datetime, timedelta

def register_dashboard_routes(app):
    @app.route('/dashboard', methods=['GET'])
    @login_required
    def dashboard():
        user = session.get('user', 'Inconnu')
        timeout_minutes = int(session.get('timeout_minutes') or 15)  # Ajouté ici

        today = date.today()

        ventes_du_jour = db.session.query(func.sum(Vente.montant)).filter(func.date(Vente.date) == today).scalar() or 0
        total_cb = db.session.query(func.sum(Vente.montant)).filter(func.date(Vente.date) == today, Vente.mode == 'carte').scalar() or 0
        total_cash = db.session.query(func.sum(Vente.montant)).filter(func.date(Vente.date) == today, Vente.mode == 'especes').scalar() or 0

        top_articles = db.session.query(
            MouvementStock.article,
            func.sum(MouvementStock.quantite).label('quantite')
        ).filter(MouvementStock.type_mouvement == 'sortie')\
         .group_by(MouvementStock.article)\
         .order_by(desc('quantite'))\
         .limit(5).all()

        articles_bas_stock = db.session.query(MouvementStock.article)\
            .group_by(MouvementStock.article)\
            .having(
                func.sum(
                    case(
                        (MouvementStock.type_mouvement == 'entree', MouvementStock.quantite),
                        else_=-MouvementStock.quantite
                    )
                ) < 5
            ).count()

        dernieres_ventes = db.session.query(Vente).order_by(Vente.date.desc()).limit(5).all()

        return render_template('dashboard_caisse.html',
                               utilisateur=user,
                               ventes_du_jour=ventes_du_jour,
                               total_cb=total_cb,
                               total_cash=total_cash,
                               top_articles=[{'nom': a[0], 'quantite': int(a[1])} for a in top_articles],
                               articles_bas_stock=articles_bas_stock,
                               dernieres_ventes=dernieres_ventes,
                               timeout_minutes=timeout_minutes)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('auth.login'))

        # Gestion du timeout
        last_active_str = session.get('last_active')
        timeout_minutes = int(session.get('timeout_minutes') or 5)

        if last_active_str:
            last_active = datetime.fromisoformat(last_active_str)
            now = datetime.utcnow()
            if now - last_active > timedelta(minutes=timeout_minutes):
                session.clear()
                return redirect(url_for('auth.login'))

        # Met à jour l'activité
        session['last_active'] = datetime.utcnow().isoformat()

        return f(*args, **kwargs)
    return decorated_function
