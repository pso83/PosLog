from flask import render_template, Blueprint
from flask_login import login_required, current_user

static_bp = Blueprint('static_pages', __name__)

def register_static_pages(app):
    @app.route('/vente')
    def vente():
        return render_template('vente.html')

    @app.route('/programmer')
    def programmer():
        return render_template('programmation.html')

    @app.route('/gestion')
    def gestion():
        return render_template('gestion.html')

    @app.route('/stocks')
    def stocks():
        return render_template('stocks.html')

    @static_bp.route('/vente')
    @login_required
    def vente():
        return render_template(
            'vente.html',
            user_keyboard_id=current_user.clavier_id
        )
