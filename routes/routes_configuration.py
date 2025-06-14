from flask import Blueprint, render_template, redirect, url_for, request
from models.utilisateur import Utilisateur
from models.profil import Profil
from models.clavier import Clavier
from models.imprimante import Imprimante
from models.ticket_config import TicketConfig
from models.reseau import Reseau
from models.peripherique import Peripherique
from extensions import db

configuration_bp = Blueprint('configuration', __name__)

# Page d'accueil de configuration
@configuration_bp.route('/configuration')
def configuration_home():
    return render_template('configuration_home.html')

# ---- Utilisateurs ----
@configuration_bp.route('/configuration/utilisateurs')
def configuration_utilisateurs():
    utilisateurs = Utilisateur.query.all()
    profils = Profil.query.all()
    claviers = Clavier.query.all()
    imprimantes = Imprimante.query.all()

    edit_id = request.args.get('edit_id')
    edit_utilisateur = Utilisateur.query.get(edit_id) if edit_id else None

    return render_template(
        'configuration_utilisateurs.html',
        utilisateurs=utilisateurs,
        profils=profils,
        claviers=claviers,
        imprimantes=imprimantes,
        edit_utilisateur=edit_utilisateur
    )

@configuration_bp.route('/configuration/utilisateurs/edit/<int:id>')
def edit_utilisateur(id):
    utilisateur = Utilisateur.query.get_or_404(id)
    utilisateurs = Utilisateur.query.all()
    profils = Profil.query.all()
    claviers = Clavier.query.all()
    imprimantes = Imprimante.query.all()
    return render_template('configuration_utilisateurs.html',
                           utilisateurs=utilisateurs,
                           profils=profils,
                           claviers=claviers,
                           imprimantes=imprimantes,
                           edit_utilisateur=utilisateur)


@configuration_bp.route('/configuration/utilisateurs/save', methods=['POST'])
def save_utilisateur():
    form = request.form
    id = form.get('id')
    is_edit = bool(id)

    utilisateur = Utilisateur.query.get(id) if is_edit else Utilisateur()

    utilisateur.nom = form.get('nom')
    utilisateur.code = form.get('code')
    utilisateur.profil_id = form.get('profil_id') or None
    utilisateur.clavier_id = form.get('clavier_id') or None
    utilisateur.mode_vente = form.get('mode_vente')
    utilisateur.imprimante_id = form.get('imprimante_id') or None

    db.session.add(utilisateur)
    db.session.commit()

    if is_edit:
        return redirect(url_for('configuration.configuration_utilisateurs', edit_id=utilisateur.id))
    else:
        return redirect(url_for('configuration.configuration_utilisateurs'))


@configuration_bp.route('/configuration/utilisateurs/delete/<int:id>')
def delete_utilisateur(id):
    utilisateur = Utilisateur.query.get_or_404(id)
    db.session.delete(utilisateur)
    db.session.commit()
    return redirect(url_for('configuration.configuration_utilisateurs'))

# ---- Profils ----
@configuration_bp.route('/configuration/profils')
def configuration_profils():
    profils = Profil.query.all()
    return render_template('configuration_profils.html', profils=profils)

# ---- Imprimantes ----
@configuration_bp.route('/configuration/imprimantes')
def configuration_imprimantes():
    imprimantes = Imprimante.query.all()
    return render_template('configuration_imprimantes.html',
                           imprimantes=imprimantes,
                           imprimante=None)  # Ajouté


# ---- Claviers ----
@configuration_bp.route('/configuration/claviers')
def configuration_claviers():
    claviers = Clavier.query.all()
    return render_template('configuration_claviers.html', claviers=claviers)

# ---- Ticket ----
@configuration_bp.route('/configuration/ticket')
def configuration_ticket():
    config = TicketConfig.query.first()
    return render_template('configuration_ticket.html', config=config)

# ---- Réseau ----
@configuration_bp.route('/configuration/reseau')
def configuration_reseau():
    reseaux = Reseau.query.all()
    return render_template('configuration_reseau.html', reseaux=reseaux)

# ---- Périphériques ----
@configuration_bp.route('/configuration/peripheriques')
def configuration_peripheriques():
    peripheriques = Peripherique.query.all()
    return render_template('configuration_peripheriques.html', peripheriques=peripheriques)
