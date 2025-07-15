from flask import Blueprint, render_template, redirect, url_for, request, jsonify, current_app
from models.utilisateur import Utilisateur
from models.profil import Profil
from models.clavier import Clavier
from models.imprimante import Imprimante
from models.ticket_config import TicketConfig
from models.reseau import Reseau
from models.peripherique import Peripherique
from models.plan_salle import TablePlan
from utils.auth import login_required
from extensions import db
from models.Salle import Salle
import os

configuration_bp = Blueprint('configuration', __name__)

# Page d'accueil de configuration
@configuration_bp.route('/configuration')
def configuration_home():
    salles = Salle.query.all()
    salle_id = salles[0].id if salles else None
    return render_template('configuration_home.html', salles=salles, salle_id=salle_id)

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
        "configuration_utilisateurs.html",
        utilisateurs=utilisateurs,
        profils=profils,
        claviers=claviers,
        imprimantes=imprimantes,
        edit_utilisateur=edit_utilisateur,
        request=request  # ✅ ligne indispensable
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
    return render_template('configuration_profils.html', profils=profils, request=request)

# ---- Imprimantes ----
@configuration_bp.route('/configuration/imprimantes')
def configuration_imprimantes():
    imprimantes = Imprimante.query.all()
    return render_template('configuration_imprimantes.html',
                           imprimantes=imprimantes,
                           imprimante=None,
                           request=request)  # Ajouté

# ---- Plans de salle ----

# Affiche la liste des salles (page avec la liste à gauche)
@configuration_bp.route('/configuration/salles', methods=['GET'])
@login_required
def configuration_salles():
    salles = Salle.query.all()
    return render_template('configuration_salles.html', salles=salles)

# Ajout d'une nouvelle salle
@configuration_bp.route('/configuration/salles/add', methods=['POST'])
def add_salle():
    nom = request.form.get('nom')
    plan_type = request.form.get('plan_type')
    if nom and plan_type:
        salle = Salle(nom=nom, plan_type=plan_type)
        db.session.add(salle)
        db.session.commit()
    return redirect(url_for('configuration.configuration_salles'))


# Modification d'une salle existante
@configuration_bp.route('/configuration/salles/edit/<int:salle_id>', methods=['POST'])
def edit_salle(salle_id):
    salle = Salle.query.get_or_404(salle_id)
    salle.nom = request.form.get('nom')
    salle.plan_type = request.form.get('plan_type')
    db.session.commit()
    return redirect(url_for('configuration.configuration_salles'))


# Suppression d'une salle
@configuration_bp.route('/configuration/salles/delete/<int:salle_id>', methods=['POST'])
def delete_salle(salle_id):
    salle = Salle.query.get_or_404(salle_id)
    db.session.delete(salle)
    db.session.commit()
    return redirect(url_for('configuration.configuration_salles'))


# Affichage du plan d'une salle et enregistrement des éléments via POST (AJAX)
@configuration_bp.route('/configuration/plan_salle/<int:salle_id>', methods=['GET', 'POST'])
@login_required
def configuration_plan_salle(salle_id):
    salle = Salle.query.get_or_404(salle_id)

    if request.method == 'POST':
        data = request.get_json() or {}
        # On suppose que le payload est { "tables": [ {...}, {...} ] }
        tables_data = data.get('tables', [])

        # On supprime l'ancien plan
        TablePlan.query.filter_by(salle_id=salle_id).delete()

        for tab in tables_data:
            # on accepte soit 'type' soit 'type_element'
            type_element = tab.get('type') or tab.get('type_element')
            filename     = tab.get('filename')
            x            = tab.get('x', 0)
            y            = tab.get('y', 0)
            rotation     = tab.get('rotation', 0)
            numero       = tab.get('numero')
            nb_places    = tab.get('nb_places')

            tp = TablePlan(
                type_element = type_element,
                filename     = filename,
                x            = x,
                y            = y,
                rotation     = rotation,
                numero       = numero,
                nb_places    = nb_places,
                salle_id     = salle_id
            )
            db.session.add(tp)

        db.session.commit()
        return jsonify(status='ok')

    # en GET, on renvoie la page + les items existants
    items = [{
        'type': tp.type_element,
        'filename': tp.image,  # ← on récupère maintenant tp.image
        'x': tp.x,
        'y': tp.y,
        'rotation': tp.rotation,
        'numero': tp.numero,
        'nb_places': tp.nb_places
    } for tp in TablePlan.query.filter_by(salle_id=salle_id).all()]

    salles = Salle.query.all()
    return render_template(
        'configuration_plan_salle.html',
        salles      = salles,
        salle       = salle,
        items       = items
    )


@configuration_bp.route('/api/plan_salle/<int:salle_id>')
@login_required
def api_plan_salle(salle_id):
    """
    Renvoie le plan enregistré au format JSON.
    """
    elements = TablePlan.query.filter_by(salle_id=salle_id).all()
    return jsonify([
        {
            'id':            e.id,
            'type_element':  e.type_element,
            # on renvoie le chemin complet pour l'affichage côté client
            'image':         url_for('static',
                                    filename=f'images/elements/{e.type_element}/{e.image}'),
            'numero':        e.numero,
            'nb_places':     e.nb_places,
            'rotation':      e.rotation,
            'x':             e.x,
            'y':             e.y
        }
        for e in elements
    ])

@configuration_bp.route('/configuration/plan/save', methods=['POST'])
def save_plan_elements():
    """
    Reçoit JSON { salle_id, elements: [...] } et remplace en base.
    """
    data     = request.get_json() or {}
    salle_id = data.get('salle_id')
    elements = data.get('elements', [])

    try:
        # On supprime l’ancien
        TablePlan.query.filter_by(salle_id=salle_id).delete()

        # On ré-insère chaque élément
        for el in elements:
            tp = TablePlan(
                salle_id     = salle_id,
                type_element = el.get('type_element'),
                image        = el.get('image').rsplit('/', 1)[-1],  # n’en garder que le nom de fichier
                numero       = el.get('numero'),
                nb_places    = el.get('nb_places'),
                rotation     = el.get('rotation', 0),
                x            = el.get('x'),
                y            = el.get('y')
            )
            db.session.add(tp)

        db.session.commit()
        return jsonify({'status': 'success'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

@configuration_bp.route('/configuration/elements/<categorie>')
def get_element_images(categorie):
    base_dir = os.path.join(current_app.static_folder, 'images', 'elements', categorie)
    if not os.path.isdir(base_dir):
        return jsonify(images=[])

    images = []
    for file in os.listdir(base_dir):
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
            images.append(f'/static/images/elements/{categorie}/{file}')
    return jsonify(images=images)

# ---- Ticket ----
@configuration_bp.route('/configuration/ticket', methods=['GET', 'POST'])
def configuration_ticket():
    config = TicketConfig.query.first()

    if request.method == 'POST':
        nom_commerce = request.form.get('nom_commerce')
        adresse = request.form.get('adresse')
        footer = request.form.get('footer')

        if config:
            config.nom_commerce = nom_commerce
            config.adresse = adresse
            config.footer = footer
        else:
            config = TicketConfig(nom_commerce=nom_commerce, adresse=adresse, footer=footer)
            db.session.add(config)

        db.session.commit()
        return redirect(url_for('configuration.configuration_ticket'))

    return render_template("configuration_ticket.html", config=config, request=request)

# ---- Réseau ----
@configuration_bp.route('/configuration/reseau')
def configuration_reseau():
    reseaux = Reseau.query.all()
    return render_template('configuration_reseau.html', reseaux=reseaux, request=request)

# ---- Périphériques ----
@configuration_bp.route('/configuration/peripheriques')
def configuration_peripheriques():
    peripheriques = Peripherique.query.all()
    return render_template('configuration_peripheriques.html', peripheriques=peripheriques, request=request)
