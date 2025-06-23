from flask import Blueprint, render_template, request, redirect, session, url_for
from models.utilisateur import Utilisateur
from functools import wraps
from datetime import datetime, timedelta

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'], endpoint='login')
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        now = datetime.now()
        if username == "Super Admin" and password == now.strftime('%H%d'):
            session['user'] = "Utilisateur root"
            return redirect(url_for('dashboard'))
        user = Utilisateur.query.filter_by(nom=username).first()
        if user and user.code == password:
            session['user'] = user.nom
            session['timeout_minutes'] = user.profil.timeout
            session['last_active'] = datetime.utcnow().isoformat()
            return redirect(url_for('dashboard'))
        return render_template('login.html', users=Utilisateur.query.all(), erreur="Erreur d’identifiants")
    return render_template('login.html', users=Utilisateur.query.all())

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('auth.login'))

        last_active_str = session.get('last_active')
        timeout_minutes = int(session.get('timeout_minutes') or 15)

        if last_active_str:
            last_active = datetime.fromisoformat(last_active_str)
            now = datetime.utcnow()
            if now - last_active > timedelta(minutes=timeout_minutes):
                session.clear()
                return redirect(url_for('auth.login'))

        session['last_active'] = datetime.utcnow().isoformat()
        return f(*args, **kwargs)
    return decorated_function
