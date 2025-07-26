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
        side = request.args.get('side', 'main')
        clavier = Clavier.query.get(clavier_id) if clavier_id else (claviers[0] if claviers else None)
        boutons = {}

        if clavier:
            boutons_data = BoutonClavier.query.filter_by(clavier_id=clavier.id).all()
            for b in boutons_data:
                boutons[b.position] = {
                    'position': b.position,
                    'couleur': b.couleur,
                    'images': b.image,
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
        element_type = data.get('type')
        element_id = int(data.get('element_id'))

        # Suppression de l’éventuel bouton existant
        BoutonClavier.query.filter_by(
            clavier_id=clavier_id,
            position=position
        ).delete()

        # Création du nouveau bouton
        bouton = BoutonClavier(
            clavier_id=clavier_id,
            position=position,
            element_type=element_type,
            couleur=data.get('couleur'),
            text_color=data.get('text_color'),  # ← on récupère bien text_color
            image=data.get('image'),  # ← c’était 'images', on corrige en 'image'
            masquer_texte=data.get('masquer_texte', False)
        )

        # Association de l’élément selon le type
        if element_type == 'article':
            bouton.article_id = element_id
        elif element_type == 'fonction':
            bouton.fonction_id = element_id
        # … le reste de tes elif …

        # Debug : vérifie que Python a bien pris en compte text_color
        print(f"🔧 bouton.couleur    = {bouton.couleur!r}")
        print(f"🔧 bouton.text_color = {bouton.text_color!r}")

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

        # --- Nouveau : calcul du prix unitaire et flag prix manuel ---
        prix_cents = 0
        price_manual = False
        if type_element == 'article' and b.article:
            # on prend prix_1 par défaut# on prend prix_1 par défaut
            prix_cents = int(round((b.article.prix_1 or 0) * 100))
            price_manual = bool(b.article.prix_manuel)
        # (idem éventuellement pour d'autres types…)

        data.append({
            "position": b.position,
            "type": type_element,
            "element_id": element_id,
            "nom": nom,
            "couleur": b.couleur,
            "text_color": b.text_color,
            "images": b.image,
            "masquer_texte": b.masquer_texte,
            "prix_unitaire": prix_cents,
            "price_manuel": price_manual
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
                image=b.get('images'),
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

@clavier_bp.route('/vente')
def clavier_vente():
    cid = request.args.get('clavier_id', type=int)
    # Récupère tous les boutons du clavier (via votre modèle)
    boutons = BoutonClavier.query.filter_by(clavier_id=cid).all()
    # Sérialise au format {label, value, programmed}
    data = [
      {
        'label': btn.label,
        'value': btn.action_value,
        'programmed': btn.is_programmed
      }
      for btn in boutons
    ]
    return jsonify(data)

@clavier_bp.route('/vente_fragment')
def clavier_vente_fragment():
    cid = request.args.get('clavier_id', type=int)
    boutons = (BoutonClavier.query
               .filter_by(clavier_id=cid)
               .order_by(BoutonClavier.position)
               .all())
    return render_template('_keyboard_vente.html', boutons=boutons)

