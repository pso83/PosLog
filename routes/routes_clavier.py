from flask import render_template, request, redirect, url_for, jsonify, Blueprint
from extensions import db
from models.article import Article
from models.clavier import Clavier
from models import clavier
from models.bouton_clavier import BoutonClavier
from models.tva import Tva
from models.Groupe import Groupe
from models.Famille import Famille
from models.SousFamille import SousFamille
from models.reglement import Reglement
from models.commentaire import Commentaire, ElementCommentaire
from models.ticket_config import TicketConfig
from models.fonction import Fonction
from models.utilisateur import Utilisateur
from models.menu import Menu
from models.menu_page import MenuPage
from models.formule import Formule, FormuleComposant
from models.profil import Profil

# 🔧 Ajoute ceci :
clavier_bp = Blueprint('clavier_bp', __name__)

def register_clavier_routes(app):
    @clavier_bp.route('/programmation/claviers')
    def programmation_claviers():
        claviers = Clavier.query.all()
        clavier_id = request.args.get('clavier_id', type=int)
        clavier = Clavier.query.get(clavier_id) if clavier_id else (claviers[0] if claviers else None)
        boutons = {}

        if clavier:
            boutons_data = BoutonClavier.query.filter_by(clavier_id=clavier.id).all()
            for b in boutons_data:
                boutons[b.position] = {
                    'position': b.position,
                    'couleur': b.couleur,
                    'image': b.image,
                    'type': b.element_type,
                    'element_id': b.article_id or b.fonction_id or b.menu_id or b.formule_id or b.utilisateur_id or b.reglement_id or b.commentaire_id or b.sous_clavier_id,
                    'masquer_texte': b.masquer_texte,
                }

        return render_template(
            "programmation_claviers.html",
            claviers=claviers,
            clavier=clavier,
            boutons=boutons,
            message=request.args.get('message')
        )

    @app.route('/programmer/claviers/save', methods=['POST'])
    def enregistrer_clavier():
        nom = request.form.get('nom_clavier')
        clavier = Clavier.query.first()
        if clavier:
            clavier.nom = nom
        else:
            clavier = Clavier(nom=nom)
            db.session.add(clavier)
        db.session.commit()
        return redirect(url_for('afficher_claviers'))

    @app.route('/programmer/claviers/assign', methods=['POST'])
    def assigner_article():
        position = int(request.form.get('position'))
        clavier = Clavier.query.first()
        if not clavier:
            return redirect(url_for('afficher_claviers'))

        articles = Article.query.all()
        return render_template('assigner_article.html', position=position, articles=articles, clavier_id=clavier.id)

    @clavier_bp.route('/save_bouton', methods=['POST'])
    def save_bouton():
        data = request.get_json()
        print("🔧 Données reçues :", data)

        clavier_id = int(data.get('clavier_id'))
        position = int(data.get('position'))
        type = data.get('type')
        element_id = int(data.get('element_id'))

        # Supprimer bouton existant à cette position
        BoutonClavier.query.filter_by(clavier_id=clavier_id, position=position).delete()

        bouton = BoutonClavier(
            clavier_id=clavier_id,
            position=position,
            element_type=type,  # ✅ Ajouté
            couleur=data.get('couleur'),
            image=data.get('image'),
            masquer_texte=data.get('masquer_texte', False)
        )

        if type == 'article':
            bouton.article_id = element_id
        elif type == 'fonction':
            bouton.fonction_id = element_id
        elif type == 'menu':
            bouton.menu_id = element_id
        elif type == 'formule':
            bouton.formule_id = element_id
        elif type == 'utilisateur':
            bouton.utilisateur_id = element_id
        elif type == 'reglement':
            bouton.reglement_id = element_id
        elif type == 'commentaire':
            bouton.commentaire_id = element_id
        elif type == 'clavier':
            bouton.sous_clavier_id = element_id

        db.session.add(bouton)
        db.session.commit()

        return jsonify({'status': 'ok'})


@clavier_bp.route("/boutons/<int:clavier_id>")
def get_boutons(clavier_id):
    boutons = BoutonClavier.query.filter_by(clavier_id=clavier_id).all()
    data = []

    for b in boutons:
        nom = f"Vide {b.position}"
        element_id = None
        type_element = b.element_type

        if type_element == 'article' and b.article:
            nom = b.article.nom_article
            element_id = b.article_id
        elif type_element == 'fonction' and b.fonction:
            nom = b.fonction.nom
            element_id = b.fonction_id
        elif type_element == 'menu' and b.menu:
            nom = b.menu.nom
            element_id = b.menu_id
        elif type_element == 'formule' and b.formule:
            nom = b.formule.nom
            element_id = b.formule_id
        elif type_element == 'utilisateur' and b.utilisateur:
            nom = b.utilisateur.nom
            element_id = b.utilisateur_id
        elif type_element == 'commentaire' and b.commentaire:
            nom = b.commentaire.nom
            element_id = b.commentaire_id
        elif type_element == 'clavier' and b.sous_clavier:
            nom = b.sous_clavier.nom
            element_id = b.sous_clavier_id
        elif type_element == 'reglement' and b.reglement:
            nom = b.reglement.nom
            element_id = b.reglement_id

        data.append({
            "position": b.position,
            "type": type_element,
            "element_id": element_id,
            "nom": nom,
            "couleur": b.couleur,
            "image": b.image,
            "masquer_texte": b.masquer_texte
        })

    return jsonify(data)

@clavier_bp.route('/import/<int:id>', methods=['POST'])
def import_clavier(id):
    fichier = request.files.get('file')
    if not fichier:
        return redirect(url_for('clavier_bp.programmation_claviers', clavier_id=id, message="Aucun fichier sélectionné", message_type="warning"))

    try:
        import json
        data = json.load(fichier)
        boutons = data.get('boutons', [])

        # Supprimer les anciens
        BoutonClavier.query.filter_by(clavier_id=id).delete()

        for b in boutons:
            type_element = b.get('type')
            element_id = b.get('element_id')

            bouton = BoutonClavier(
                clavier_id=id,
                position=b.get('position'),
                couleur=b.get('couleur'),
                image=b.get('image'),
                masquer_texte=b.get('masquer_texte', False),
                element_type=type_element
            )

            # Affectation selon le type
            if type_element == 'article':
                bouton.article_id = element_id
            elif type_element == 'fonction':
                bouton.fonction_id = element_id
            elif type_element == 'menu':
                bouton.menu_id = element_id
            elif type_element == 'formule':
                bouton.formule_id = element_id
            elif type_element == 'utilisateur':
                bouton.utilisateur_id = element_id
            elif type_element == 'reglement':
                bouton.reglement_id = element_id
            elif type_element == 'commentaire':
                bouton.commentaire_id = element_id
            elif type_element == 'clavier':
                bouton.sous_clavier_id = element_id

            db.session.add(bouton)

        db.session.commit()
        return redirect(url_for('clavier_bp.programmation_claviers', clavier_id=id, message="Importation réussie", message_type="success"))

    except Exception as e:
        print("Erreur lors de l'importation :", e)
        return redirect(url_for('clavier_bp.programmation_claviers', clavier_id=id, message="Erreur lors de l'importation", message_type="danger"))

@clavier_bp.route('/clavier/supprimer/<int:id>', methods=['POST'])
def supprimer_clavier(id):
    clavier = Clavier.query.get_or_404(id)

    # Supprime les boutons associés
    BoutonClavier.query.filter_by(clavier_id=id).delete()

    # Supprime le clavier
    db.session.delete(clavier)
    db.session.commit()

    return redirect(url_for('clavier_bp.programmation_claviers', message="Clavier supprimé", message_type="success"))


