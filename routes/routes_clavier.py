from flask import render_template, request, redirect, url_for, jsonify, Blueprint
from extensions import db
from models.article import Article
from models.clavier import Clavier, ClavierBouton
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
                    'label': b.label,
                    'couleur': b.couleur,
                    'image': b.image,
                    'type': b.type,
                    'element_id': b.element_id,
                    'masquer_texte': b.masquer_texte,
                }

        return render_template("programmation_clavier.html", claviers=claviers, clavier=clavier, boutons=boutons)

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

    @app.route('/clavier/save_bouton', methods=['POST'])
    def save_bouton():
        data = request.get_json()

        position = int(data['position'])
        type_elem = data.get('type')
        element_id = int(data.get('element_id')) if data.get('element_id') else None
        label = data.get('label', '')
        couleur = data.get('couleur', '#e0e0e0')
        image = data.get('image', '')
        masquer_texte = data.get('masquer_texte') in ['true', 'True', True]
        clavier_id = int(data.get('clavier_id')) if data.get('clavier_id') else 1

        bouton = BoutonClavier.query.filter_by(clavier_id=clavier_id, position=position).first()

        if not bouton:
            bouton = BoutonClavier(clavier_id=clavier_id, position=position)

        bouton.type = type_elem
        bouton.element_id = element_id
        bouton.label = label
        bouton.couleur = couleur
        bouton.image = image
        bouton.masquer_texte = masquer_texte

        db.session.add(bouton)
        db.session.commit()

        return jsonify({"status": "ok"})

@clavier_bp.route('/clavier/boutons/<int:clavier_id>')
def get_boutons(clavier_id):
    print(f"🔍 Requête boutons pour clavier ID: {clavier_id}")
    boutons = BoutonClavier.query.filter_by(clavier_id=clavier_id).all()
    boutons_map = {b.position: b for b in boutons}
    boutons_final = []

    for pos in range(1, 56):
        b = boutons_map.get(pos)
        if b:
            data = {
                'position': b.position,
                'label': b.label,
                'couleur': b.couleur,
                'image': b.image,
                'type': b.type,
                'element_id': b.element_id,
                'masquer_texte': b.masquer_texte,
                'nom_article': None,
                'nom_menu': None,
                'nom_formule': None,
                'nom_clavier': None,
                'nom_fonction': None,
                'nom_utilisateur': None,
                'nom_reglement': None,
                'nom_commentaire': None,
            }

            if b.type == 'article':
                a = Article.query.get(b.element_id)
                data['nom_article'] = a.nom_article if a else None
            elif b.type == 'menu':
                m = Menu.query.get(b.element_id)
                data['nom_menu'] = m.nom if m else None
            elif b.type == 'formule':
                f = Formule.query.get(b.element_id)
                data['nom_formule'] = f.nom if f else None
            elif b.type == 'clavier':
                c = Clavier.query.get(b.element_id)
                data['nom_clavier'] = c.nom if c else None
            elif b.type == 'fonction':
                f = Fonction.query.get(b.element_id)
                data['nom_fonction'] = f.nom if f else None
            elif b.type == 'utilisateur':
                u = Utilisateur.query.get(b.element_id)
                data['nom_utilisateur'] = u.nom if u else None
            elif b.type == 'reglement':
                r = Reglement.query.get(b.element_id)
                data['nom_reglement'] = r.nom if r else None
            elif b.type == 'commentaire':
                cm = Commentaire.query.get(b.element_id)
                data['nom_commentaire'] = cm.texte if cm else None

            boutons_final.append(data)
        else:
            boutons_final.append({
                'position': pos,
                'label': f'Vide {pos}',
                'couleur': '#e0e0e0',
                'image': None,
                'type': 'vide',
                'element_id': None,
                'masquer_texte': False,
            })

    return jsonify(boutons_final)
