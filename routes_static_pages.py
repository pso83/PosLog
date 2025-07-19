# routes_static_pages.py
from flask import Blueprint, render_template, session, redirect, url_for
from models.utilisateur import Utilisateur

static_bp = Blueprint('static_pages', __name__)

def register_static_pages(app):
    @app.route('/vente')
    def vente():
        # 1) Redirection vers le login si pas de session
        if 'user' not in session:
            return redirect(url_for('auth.login'))

        # 2) Récupère l'utilisateur en base via son nom
        user = Utilisateur.query.filter_by(nom=session['user']).first()
        if not user:
            # Session corrompue ou utilisateur supprimé : on efface et on redirige
            session.pop('user', None)
            return redirect(url_for('auth.login'))

        # 3) Passe son clavier_id à Jinja
        return render_template(
            'vente.html',
            user_keyboard_id=user.clavier_id
        )

    @app.route('/programmer')
    def programmer():
        return render_template('programmation.html')

    @app.route('/gestion')
    def gestion():
        return render_template('gestion.html')

    @app.route('/stocks')
    def stocks():
        return render_template('stocks.html')

    # … autres routes statiques …
