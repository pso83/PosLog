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
@configuration_bp.route('/configuration/utilisateurs', methods=['GET', 'POST'])
def configuration_utilisateurs():
    # Enregistrement ou mise à jour
    if request.method == 'POST':
        user_id = request.form.get('id')
        nom = request.form.get('nom')
        code = request.form.get('code')
        profil_id = request.form.get('profil_id')
        clavier_id = request.form.get('clavier_id') or None
        mode_vente = request.form.get('mode_vente') or ''
        imprimante_id = request.form.get('imprimante_id') or None

        if user_id:
            utilisateur = Utilisateur.query.get(user_id)
            if utilisateur:
                utilisateur.nom = nom
                utilisateur.code = code
                utilisateur.profil_id = profil_id
                utilisateur.clavier_id = clavier_id
                utilisateur.mode_vente = mode_vente
                utilisateur.imprimante_id = imprimante_id
        else:
            utilisateur = Utilisateur(
                nom=nom,
                code=code,
                profil_id=profil_id,
                clavier_id=clavier_id,
                mode_vente=mode_vente,
                imprimante_id=imprimante_id
            )
            db.session.add(utilisateur)

        db.session.commit()
        return redirect(url_for('configuration.configuration_utilisateurs'))

    # Mode GET
    utilisateurs = Utilisateur.query.all()
    profils = Profil.query.all()
    claviers = Clavier.query.all()
    imprimantes = Imprimante.query.all()

    # Mode édition
    edit_id = request.args.get('edit')
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
    return redirect(url_for('configuration.configuration_utilisateurs', edit=id))

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
