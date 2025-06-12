from flask import Flask, render_template, jsonify, send_file, Blueprint, request, redirect, url_for, flash
from models import db, article, Groupe, Famille, SousFamille, tva, clavier
from extensions import db
from models.article import Article
from models.clavier import Clavier
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
from models.imprimante import Imprimante
import win32print

import json
import io
from datetime import datetime
from io import BytesIO

clavier_bp = Blueprint('programmation', __name__)

programmation_bp = Blueprint('programmation', __name__)

def get_windows_printers():
    printers = []
    try:
        flags = win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS
        printers_info = win32print.EnumPrinters(flags)
        for printer in printers_info:
            printers.append(printer[2])
    except Exception as e:
        print(f"Erreur lors de la récupération des imprimantes : {e}")
    return printers

# Fonction utilitaire générique de désaffectation des boutons

def desaffecter_boutons(element_type, element_id):
    field_map = {
        'article': BoutonClavier.article_id,
        'fonction': BoutonClavier.fonction_id,
        'menu': BoutonClavier.menu_id,
        'formule': BoutonClavier.formule_id,
        'utilisateur': BoutonClavier.utilisateur_id,
        'reglement': BoutonClavier.reglement_id,
        'commentaire': BoutonClavier.commentaire_id,
        'clavier': BoutonClavier.sous_clavier_id
    }

    champ = field_map.get(element_type)
    if not champ:
        return

    boutons = BoutonClavier.query.filter(champ == element_id).all()

    for b in boutons:
        db.session.delete(b)

    db.session.commit()


def register_routes(app):

    @app.route('/programmation/elements', methods=['GET'])
    def show_programmation_elements():
        return render_template('programmation_elements.html')

    # Route pour afficher la programmation des claviers
    @programmation_bp.route('/claviers')
    def programmation_claviers():
        claviers = Clavier.query.all()
        clavier_id = request.args.get("clavier_id", type=int)

        clavier = Clavier.query.get(clavier_id) if clavier_id else (claviers[0] if claviers else None)

        boutons = []
        if clavier:
            for b in clavier.boutons:
                if b.article_id:
                    bouton_type = 'article'
                    element_id = b.article_id
                elif b.fonction_id:
                    bouton_type = 'fonction'
                    element_id = b.fonction_id
                elif b.menu_id:
                    bouton_type = 'menu'
                    element_id = b.menu_id
                elif b.formule_id:
                    bouton_type = 'formule'
                    element_id = b.formule_id
                elif b.utilisateur_id:
                    bouton_type = 'utilisateur'
                    element_id = b.utilisateur_id
                elif b.reglement_id:
                    bouton_type = 'reglement'
                    element_id = b.reglement_id
                elif b.commentaire_id:
                    bouton_type = 'commentaire'
                    element_id = b.commentaire_id
                elif b.sous_clavier_id:
                    bouton_type = 'sous_clavier'
                    element_id = b.sous_clavier_id
                else:
                    bouton_type = None
                    element_id = None

                boutons.append({
                    'id': b.id,
                    'position': b.position,
                    'type': bouton_type,
                    'element_id': element_id
                })

        return render_template('programmation_claviers.html', claviers=claviers, clavier=clavier, boutons=boutons,
                               message=None)

    # Route pour créer un clavier
    @app.route('/clavier/creer', methods=['POST'])
    def creer_clavier():
        nom = request.form.get('nom')
        if nom:
            clavier = Clavier(nom=nom)
            db.session.add(clavier)
            db.session.commit()
        return redirect(url_for('clavier_bp.programmation_claviers', message='Clavier créé'))

    # Route pour réinitialiser tous les boutons d'un clavier
    @app.route('/clavier/reset')
    def reset_clavier():
        clavier_id = request.args.get('clavier_id', type=int)
        clavier = Clavier.query.get(clavier_id)
        if clavier:
            BoutonClavier.query.filter_by(clavier_id=clavier.id).delete()
            db.session.commit()
        return redirect(url_for('programmation.programmation_claviers', message='Clavier réinitialisé', clavier_id=clavier_id))

    # Route pour dupliquer un clavier
    @app.route('/clavier/dupliquer/<int:id>')
    def dupliquer_clavier(id):
        original = Clavier.query.get_or_404(id)
        nouveau = Clavier(nom=original.nom + " (copie)")
        db.session.add(nouveau)
        db.session.flush()

        for bouton in original.boutons:
            copie = BoutonClavier(
                clavier_id=nouveau.id,
                position=bouton.position,
                type=bouton.type,
                element_id=bouton.element_id,
                label=bouton.label,
                couleur=bouton.couleur,
                image=bouton.image,
                masquer_texte=bouton.masquer_texte
            )
            db.session.add(copie)

        db.session.commit()
        return redirect(url_for('programmation.programmation_claviers', message='Clavier dupliqué', clavier_id=nouveau.id))

    # Route pour exporter les boutons d'un clavier
    @programmation_bp.route('/clavier/export/<int:id>')
    def export_clavier(id):
        clavier = Clavier.query.get(id)
        if not clavier:
            return "Clavier introuvable", 404

        data = {
            'nom': clavier.nom,
            'boutons': []
        }

        for b in clavier.boutons:
            bouton_type = (
                'article' if b.article_id else
                'fonction' if b.fonction_id else
                'menu' if b.menu_id else
                'formule' if b.formule_id else
                'utilisateur' if b.utilisateur_id else
                'reglement' if b.reglement_id else
                'commentaire' if b.commentaire_id else
                'clavier' if b.sous_clavier_id else
                None
            )

            element_id = (
                    b.article_id or b.fonction_id or b.menu_id or b.formule_id or
                    b.utilisateur_id or b.reglement_id or b.commentaire_id or b.sous_clavier_id
            )

            data['boutons'].append({
                'position': b.position,
                'type': bouton_type,
                'element_id': element_id,
                'couleur': b.couleur,
                'image': b.image,
                'masquer_texte': b.masquer_texte
            })

        json_data = json.dumps(data, ensure_ascii=False, indent=2)
        buffer = io.BytesIO(json_data.encode('utf-8'))

        return send_file(
            buffer,
            mimetype='application/json',
            as_attachment=True,
            download_name=f"clavier_{clavier.nom}.json"
        )

    # Route pour importer des boutons dans un clavier
    @clavier_bp.route('/import/<int:id>', methods=['POST'])
    def import_clavier(id):
        fichier = request.files.get('file')
        if not fichier:
            return redirect(
                url_for('programmation.programmation_claviers', clavier_id=id, message="Aucun fichier sélectionné"))

        try:
            data = json.load(fichier)
            boutons = data.get('boutons', [])

            # Supprimer les anciens boutons de ce clavier
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

                # Affectation de la bonne clé étrangère selon le type
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

                # Définir le label à afficher sur le bouton
                label = f"Vide {b.get('position')}"
                if type_element == 'article':
                    obj = Article.query.get(element_id)
                    label = obj.nom_article if obj else label
                elif type_element == 'fonction':
                    obj = Fonction.query.get(element_id)
                    label = obj.nom if obj else label
                elif type_element == 'menu':
                    obj = Menu.query.get(element_id)
                    label = obj.nom if obj else label
                elif type_element == 'formule':
                    obj = Formule.query.get(element_id)
                    label = obj.nom if obj else label
                elif type_element == 'utilisateur':
                    obj = Utilisateur.query.get(element_id)
                    label = obj.nom if obj else label
                elif type_element == 'reglement':
                    obj = Reglement.query.get(element_id)
                    label = obj.nom if obj else label
                elif type_element == 'commentaire':
                    obj = Commentaire.query.get(element_id)
                    label = obj.texte if obj else label
                elif type_element == 'clavier':
                    obj = Clavier.query.get(element_id)
                    label = obj.nom if obj else label

                bouton.label = label
                db.session.add(bouton)

            db.session.commit()
            return redirect(
                url_for('programmation.programmation_claviers', clavier_id=id, message="Importation réussie"))

        except Exception as e:
            print("Erreur lors de l'importation :", e)
            return redirect(
                url_for('programmation.programmation_claviers', clavier_id=id, message="Erreur lors de l'importation"))

    # Route pour supprimer un bouton spécifique d'un clavier
    @app.route('/clavier/effacer_bouton/', methods=['POST'])
    def effacer_bouton():
        position = int(request.form.get('effacerPosition'))
        clavier_id = int(request.args.get('clavier_id', 1))
        bouton = BoutonClavier.query.filter_by(clavier_id=clavier_id, position=position).first()
        if bouton:
            db.session.delete(bouton)
            db.session.commit()
        return redirect(url_for('programmation.programmation_claviers', clavier_id=clavier_id))

    # Route pour supprimer tous les boutons d'une ligne donnée
    @app.route('/clavier/effacer_ligne/', methods=['POST'])
    def effacer_ligne():
        ligne = int(request.form.get('effacerLigne'))
        clavier_id = int(request.args.get('clavier_id', 1))
        start = (ligne - 1) * 5 + 1
        end = ligne * 5
        boutons = BoutonClavier.query.filter(
            BoutonClavier.clavier_id == clavier_id,
            BoutonClavier.position.between(start, end)
        ).all()
        for b in boutons:
            db.session.delete(b)
        db.session.commit()
        return redirect(url_for('programmation.programmation_claviers', clavier_id=clavier_id))

    @app.route('/clavier/elements')
    def get_elements_par_type():
        type_elem = request.args.get('type')

        if type_elem == 'article':
            data = Article.query.with_entities(Article.id, Article.nom_article.label('nom')).all()
        elif type_elem == 'menu':
            data = Menu.query.with_entities(Menu.id, Menu.nom.label('nom')).all()
        elif type_elem == 'formule':
            data = Formule.query.with_entities(Formule.id, Formule.nom.label('nom')).all()
        elif type_elem == 'fonction':
            data = Fonction.query.with_entities(Fonction.id, Fonction.nom.label('nom')).all()
        elif type_elem == 'reglement':
            data = Reglement.query.with_entities(Reglement.id, Reglement.nom.label('nom')).all()
        elif type_elem == 'utilisateur':
            data = Utilisateur.query.with_entities(Utilisateur.id, Utilisateur.nom.label('nom')).all()
        elif type_elem == 'commentaire':
            data = Commentaire.query.with_entities(Commentaire.id, Commentaire.texte.label('nom')).all()
        elif type_elem == 'clavier':
            data = Clavier.query.with_entities(Clavier.id, Clavier.nom.label('nom')).all()
        else:
            return jsonify([])

        return jsonify([{"id": el.id, "nom": el.nom} for el in data])

        # Requête à utiliser dans la vue clavier pour affichage dynamique
        @app.route('/clavier/boutons/<int:clavier_id>')
        def afficher_boutons_clavier(clavier_id):
            try:
                boutons = db.session.execute(text('''
                                                  SELECT b.position,
                                                         b.label,
                                                         b.couleur,
                                                         b.image,
                                                         b.masquer_texte,
                                                         b.type,
                                                         b.element_id,
                                                         a.nom_article AS nom_article,
                                                         m.nom         AS nom_menu,
                                                         f.nom         AS nom_formule,
                                                         c.nom         AS nom_clavier,
                                                         fn.nom        AS nom_fonction,
                                                         u.nom         AS nom_utilisateur,
                                                         r.nom         AS nom_reglement,
                                                         cm.texte      AS nom_commentaire
                                                  FROM bouton_clavier b
                                                           LEFT JOIN article a ON b.type = 'article' AND b.element_id = a.id
                                                           LEFT JOIN menu m ON b.type = 'menu' AND b.element_id = m.id
                                                           LEFT JOIN formule f ON b.type = 'formule' AND b.element_id = f.id
                                                           LEFT JOIN clavier c ON b.type = 'clavier' AND b.element_id = c.id
                                                           LEFT JOIN fonction fn ON b.type = 'fonction' AND b.element_id = fn.id
                                                           LEFT JOIN utilisateur u ON b.type = 'utilisateur' AND b.element_id = u.id
                                                           LEFT JOIN reglement r ON b.type = 'reglement' AND b.element_id = r.id
                                                           LEFT JOIN commentaire cm ON b.type = 'commentaire' AND b.element_id = cm.id
                                                  WHERE b.clavier_id = :clavier_id
                                                  '''), {'clavier_id': clavier_id}).mappings().all()

                result = []
                for pos in range(1, 56):
                    bouton = next((dict(b) for b in boutons if b['position'] == pos), None)
                    if not bouton:
                        bouton = {
                            "position": pos,
                            "label": f"Vide {pos}",
                            "couleur": "#e0e0e0",
                            "image": None,
                            "masquer_texte": False,
                            "type": "vide",
                            "element_id": None
                        }
                    result.append(bouton)

                return jsonify(result)

            except Exception as e:
                print("Erreur dans /clavier/boutons :", e)
                return jsonify({'error': 'Erreur interne'}), 500

    # route pour supprimer un clavier
    @clavier_bp.route('/clavier/supprimer/<int:id>', methods=['POST'])
    def supprimer_clavier(id):
        clavier = Clavier.query.get_or_404(id)

        # Supprimer d'abord les boutons liés
        BoutonClavier.query.filter_by(clavier_id=id).delete()

        # Puis supprimer le clavier
        db.session.delete(clavier)
        db.session.commit()

        return redirect(url_for('clavier_bp.programmation_claviers', message="Clavier supprimé"))

        # Fonction pour la gestion des reglements.

    @app.route('/programmer/reglements', methods=['GET'])
    def programmation_reglements():
        reglements = Reglement.query.all()
        reglement_id = request.args.get('edit', type=int)
        reglement = Reglement.query.get(reglement_id) if reglement_id else None
        return render_template('programmation_reglements.html', reglements=reglements, reglement=reglement)

    @app.route('/programmer/reglements/save', methods=['POST'])
    def save_reglement():
        reglement_id = request.form.get('reglement_id')
        nom = request.form.get('nom')
        valeur_programmee = request.form.get('valeur_programmee') == 'on'
        montant = request.form.get('montant', type=float) if valeur_programmee else None

        reglement_connecte = request.form.get('reglement_connecte') == 'on'
        saisie_quantite = request.form.get('saisie_quantite') == 'on'
        saisie_montant = request.form.get('saisie_montant') == 'on'
        pas_de_rendu = request.form.get('pas_de_rendu') == 'on'
        pourboire = request.form.get('pourboire') == 'on'
        avoir = request.form.get('avoir') == 'on'

        if reglement_id:
            reglement = Reglement.query.get_or_404(int(reglement_id))
        else:
            reglement = Reglement()

        reglement.nom = nom
        reglement.montant = montant
        reglement.reglement_connecte = reglement_connecte
        reglement.saisie_quantite = saisie_quantite
        reglement.saisie_montant = saisie_montant
        reglement.valeur_programmee = valeur_programmee
        reglement.pas_de_rendu = pas_de_rendu
        reglement.pourboire = pourboire
        reglement.avoir = avoir

        db.session.add(reglement)
        db.session.commit()

        return redirect(url_for('programmation_reglements'))

    @app.route('/programmer/reglements/delete/<int:id>')
    def delete_reglement(id):
        reglement = Reglement.query.get_or_404(id)
        desaffecter_boutons('reglement', id)
        db.session.delete(reglement)
        db.session.commit()
        return redirect(url_for('programmation_reglements'))

    @app.route('/programmation/tva', methods=['POST'])
    def add_tva():
        label = request.form.get('label')
        taux = request.form.get('taux')
        if label and taux:
            db.session.add(Tva(label=label, taux=taux))
            db.session.commit()
        return redirect('/programmation/elements')

    @app.route('/programmation/groupes', methods=['POST'])
    def add_groupe():
        nom = request.form.get('nom')
        if nom:
            db.session.add(Groupe(nom=nom))
            db.session.commit()
        return redirect('/programmation/elements')

    @app.route('/programmation/familles', methods=['POST'])
    def add_famille():
        nom = request.form.get('nom')
        if nom:
            db.session.add(Famille(nom=nom))
            db.session.commit()
        return redirect('/programmation/elements')

    @app.route('/programmation/sousfamilles', methods=['POST'])
    def add_sous_famille():
        nom = request.form.get('nom')
        if nom:
            db.session.add(SousFamille(nom=nom))
            db.session.commit()
        return redirect('/programmation/elements')

    @app.route('/programmation/reglements', methods=['POST'])
    def add_reglement():
        mode = request.form.get('mode')
        if mode:
            db.session.add(Reglement(mode=mode))
            db.session.commit()
        return redirect('/programmation/elements')

    @app.route('/programmation/commentaires', methods=['POST'])
    def add_commentaire():
        texte = request.form.get('texte')
        if texte:
            db.session.add(Commentaire(texte=texte))
            db.session.commit()
        return redirect('/programmation/elements')

    @app.route('/programmation/menus', methods=['POST'])
    def add_menu():
        nom = request.form.get('nom')
        if nom:
            db.session.add(Menu(nom=nom))
            db.session.commit()
        return redirect('/programmation/elements')

    @app.route('/programmation/formules', methods=['POST'])
    def add_formule():
        nom = request.form.get('nom')
        if nom:
            db.session.add(Formule(nom=nom))
            db.session.commit()
        return redirect('/programmation/elements')

    @app.route('/programmer/articles/save', methods=['POST'])
    def save_article():
        form = request.form
        article_id = form.get('id')
        article = Article.query.get(article_id) if article_id else Article()

        article.nom_article = form.get('nom_article')
        for i in range(1, 5):
            setattr(article, f'prix_{i}', float(form.get(f'prix_{i}', 0) or 0))
        article.tva_id = form.get('tva_id')
        article.groupe_id = form.get('groupe_id') or None
        article.famille_id = form.get('famille_id') or None
        article.sous_famille_id = form.get('sous_famille_id') or None

        # Champs booléens
        flags = ['prix_manuel', 'vendu_au_poids', 'avec_code_barre', 'eligible_fidelite',
                 'retour_autorise', 'avoir_autorise', 'gere_stock', 'vendu_en_negatif', 'hors_ca',
                 'est_formule', 'composant_menu', 'composant_formule',
                 'appel_commentaire', 'imprimable_preparation', 'invisible_telecommande',
                 'vente_a_distance', 'gere_heure', 'depot_vente', 'gere_sav']
        for flag in flags:
            setattr(article, flag, flag in form)

        # Traitement du champ commentaire_id
        appel_commentaire = 'appel_commentaire' in form
        commentaire_id = form.get('commentaire_id', type=int)
        article.commentaire_id = commentaire_id if appel_commentaire else None

        db.session.add(article)
        db.session.commit()
        return redirect(url_for('programmation_articles'))

    @app.route('/programmer/articles/delete/<int:id>')
    def delete_article(id):
        article = Article.query.get_or_404(id)

        # 1. Désaffecter les boutons du clavier
        desaffecter_boutons('article', id)

        # 2. Supprimer les références dans FormuleComposant
        FormuleComposant.query.filter_by(article_id=id).delete()

        # 4. Supprimer l'article
        db.session.delete(article)
        db.session.commit()

        return redirect(url_for('programmation_articles'))


class CommentaireElement:
    pass


def register_programmation_routes(app):
    @app.route('/programmer/articles', methods=['GET'])
    def programmation_articles():
        # Récupération des listes nécessaires
        groupes = Groupe.query.all()
        familles = Famille.query.all()
        sous_familles = SousFamille.query.all()
        tva_options = Tva.query.all()
        commentaires = Commentaire.query.all()

        # Gestion du filtre ou d'un article à modifier
        article_id = request.args.get('id', type=int)
        article = Article.query.get(article_id) if article_id else None

        # Filtrage si nécessaire
        query = Article.query
        for champ in ['groupe', 'famille', 'sous_famille']:
            valeur = request.args.get(champ)
            if valeur:
                query = query.filter(getattr(Article, f"{champ}_id") == int(valeur))
        articles = query.all()

        return render_template('programmation_articles.html',
                               article=article,
                               articles=articles,
                               groupes=groupes,
                               familles=familles,
                               sous_familles=sous_familles,
                               tva_options=tva_options,
                               commentaires=commentaires)

    @app.route('/programmer/groupes', methods=['GET'])
    def programmation_groupes():
        groupes = Groupe.query.all()

        groupe_id = request.args.get('id', type=int)
        groupe = Groupe.query.get(groupe_id) if groupe_id else None

        # ⚠️ Bien distinguer : familles par groupe_id, articles par groupe_id
        familles = Famille.query.filter_by(groupe_id=groupe_id).all() if groupe_id else []
        articles = Article.query.filter_by(groupe_id=groupe_id).all() if groupe_id else []

        return render_template("programmation_groupes.html", groupes=groupes, groupe=groupe, familles=familles,
                               articles=articles)

    @app.route('/programmer/groupes/save', methods=['POST'])
    def save_groupe():
        nom = request.form.get("nom")
        if nom:
            g = Groupe(nom=nom)
            db.session.add(g)
            db.session.commit()
        return redirect(url_for("programmation_groupes"))

    @app.route('/programmer/familles', methods=['GET'])
    def programmation_familles():
        familles = Famille.query.all()
        famille_id = request.args.get('famille_id', type=int)
        articles = Article.query.filter_by(famille_id=famille_id).all() if famille_id else []
        return render_template("programmation_familles.html", familles=familles, articles=articles)

    @app.route('/programmer/familles/save', methods=['POST'])
    def save_famille():
        nom = request.form.get('nom')
        if nom:
            famille = Famille(nom=nom)
            db.session.add(famille)
            db.session.commit()
        return redirect(url_for('programmation_familles'))

    @app.route('/programmer/sous-familles', methods=['GET'])
    def programmation_sous_familles():
        sous_familles = SousFamille.query.all()
        sous_famille_id = request.args.get('sous_famille_id', type=int)
        articles = Article.query.filter_by(sous_famille_id=sous_famille_id).all() if sous_famille_id else []
        return render_template("programmation_sous_familles.html", sous_familles=sous_familles, articles=articles)

    @app.route('/programmer/sous-familles/save', methods=['POST'])
    def save_sous_famille():
        nom = request.form.get('nom')
        if nom:
            sous_famille = SousFamille(nom=nom)
            db.session.add(sous_famille)
            db.session.commit()
        return redirect(url_for('programmation_sous_familles'))

    # Affichage de la page de programmation des TVA
    @app.route('/programmer/tva', methods=['GET'])
    def programmation_tva():
        tvas = Tva.query.all()
        tva_id = request.args.get('tva_id', type=int)
        tva = Tva.query.get(tva_id) if tva_id else None
        articles = Article.query.filter_by(tva_id=tva_id).all() if tva_id else []
        return render_template('programmation_tva.html', tvas=tvas, tva=tva, articles=articles)

    # Sauvegarde d’une nouvelle TVA ou modification d’une TVA existante
    @app.route('/programmer/tva/save', methods=['POST'])
    def save_tva():
        tva_id = request.form.get('tva_id')
        label = request.form.get('label')
        taux = request.form.get('taux')

        if not label or not taux:
            return redirect(url_for('programmation_tva'))

        try:
            taux = float(taux)
        except ValueError:
            return redirect(url_for('programmation_tva'))

        if tva_id:
            tva = Tva.query.get(int(tva_id))
            if tva:
                tva.label = label
                tva.taux = taux
        else:
            tva = Tva(label=label, taux=taux)
            db.session.add(tva)

        db.session.commit()
        return redirect(url_for('programmation_tva'))

    @app.route('/programmer/menus', methods=['GET'])
    def programmation_menus():
        menus = Menu.query.all()
        menu_id = request.args.get('menu_id', type=int)
        menu = Menu.query.get(menu_id) if menu_id else None
        pages = MenuPage.query.filter_by(menu_id=menu.id).all() if menu else []
        articles = Article.query.filter_by(composant_menu=True).all()
        return render_template('programmation_menus.html', menus=menus, menu=menu, pages=pages, articles=articles)

    @app.route('/programmer/menus/save', methods=['POST'])
    def save_menu():
        menu_id = request.form.get('menu_id')
        nom = request.form.get('nom')

        if menu_id:
            menu = Menu.query.get(int(menu_id))
            if menu:
                menu.nom = nom
        else:
            menu = Menu(nom=nom)
            db.session.add(menu)

        db.session.commit()
        return redirect(url_for('programmation_menus', menu_id=menu.id))

    @app.route('/programmer/menus/<int:menu_id>/add_page', methods=['POST'])
    def add_menu_page(menu_id):
        nom_page = request.form.get('nom_page')
        if nom_page:
            nouvelle_page = MenuPage(menu_id=menu_id, nom_page=nom_page)
            db.session.add(nouvelle_page)
            db.session.commit()
        return redirect(url_for('programmation_menus', menu_id=menu_id))

    @app.route('/programmer/menus/delete/<int:id>')
    def delete_menu(id):
        menu = Menu.query.get_or_404(id)

        # 1. Désaffecter les boutons qui utilisent ce menu
        desaffecter_boutons('menu', id)

        # 2. Supprimer les articles liés aux pages du menu (si relation directe)
        for page in menu.pages:
            page.articles.clear()  # relation many-to-many, si définie
            db.session.delete(page)

        # 3. Supprimer le menu lui-même
        db.session.delete(menu)
        db.session.commit()

        return redirect(url_for('programmation_menus'))

    @app.route('/programmer/menus/page/save', methods=['POST'])
    def save_menu_page():
        menu_id = request.form.get('menu_id')
        nom_page = request.form.get('nom_page')

        if menu_id and nom_page:
            nouvelle_page = MenuPage(menu_id=menu_id, nom_page=nom_page)
            db.session.add(nouvelle_page)
            db.session.commit()

        return redirect(url_for('programmation_menus', menu_id=menu_id))

    @app.route('/programmer/menus/assign_article', methods=['POST'])
    def assign_article_to_page():
        page_id = request.form.get('page_id', type=int)
        article_id = request.form.get('article_id', type=int)
        page = MenuPage.query.get(page_id)
        article = Article.query.get(article_id)
        if page and article and article.composant_menu:
            if article not in page.articles:
                page.articles.append(article)
                db.session.commit()
        return redirect(url_for('programmation_menus', menu_id=page.menu_id))

    @app.route('/programmer/menus/retirer_article', methods=['POST'])
    def retirer_article_menu():
        page_id = request.form.get('page_id', type=int)
        article_id = request.form.get('article_id', type=int)
        page = MenuPage.query.get(page_id)
        article = Article.query.get(article_id)
        if page and article and article in page.articles:
            page.articles.remove(article)
            db.session.commit()
        return redirect(url_for('programmation_menus', menu_id=page.menu_id))

    # Page principale de programmation des commentaires
    @app.route('/programmer/commentaires', methods=['GET'])
    def programmation_commentaires():
        commentaires = Commentaire.query.all()
        commentaire_id = request.args.get('commentaire_id', type=int)
        commentaire = Commentaire.query.get(commentaire_id) if commentaire_id else None
        return render_template('programmation_commentaires.html', commentaires=commentaires, commentaire=commentaire)

    # Enregistrer ou modifier un commentaire
    @app.route('/programmer/commentaires/save', methods=['POST'])
    def save_commentaire():
        commentaire_id = request.form.get('id')
        nom = request.form.get('nom')

        commentaire = Commentaire.query.get(commentaire_id) if commentaire_id else Commentaire()
        commentaire.nom = nom

        db.session.add(commentaire)
        db.session.commit()
        return redirect(url_for('programmation_commentaires', commentaire_id=commentaire.id))

    # Ajouter un élément à un commentaire
    @app.route('/programmer/commentaires/<int:commentaire_id>/add_element', methods=['POST'])
    def add_element_commentaire(commentaire_id):
        nom = request.form.get('element_nom')
        if nom:
            element = ElementCommentaire(nom=nom, commentaire_id=commentaire_id)
            db.session.add(element)
            db.session.commit()
        return redirect(url_for('programmation_commentaires', commentaire_id=commentaire_id))

    # Supprimer un élément
    @app.route('/programmer/commentaires/<int:commentaire_id>/delete_element/<int:element_id>')
    def delete_commentaire(commentaire_id, element_id):
        element = CommentaireElement.query.get_or_404(element_id)
        desaffecter_boutons('element', id)
        db.session.delete(element)
        db.session.commit()
        return redirect(url_for('programmation_commentaires', commentaire_id=commentaire_id))

    @app.route('/programmer/formules', methods=['GET'])
    def programmation_formules():
        formule_id = request.args.get('formule_id', type=int)
        formules = Formule.query.all()
        formule = Formule.query.get(formule_id) if formule_id else None
        composants = [fc.article for fc in formule.composants] if formule else []

        articles = Article.query.filter_by(composant_formule=True).all()

        return render_template("programmation_formules.html",
                               formules=formules,
                               formule=formule,
                               composants=composants,
                               articles=articles)

    @app.route('/programmer/formules/save', methods=['POST'])
    def save_formule():
        form = request.form
        formule_id = form.get('id')
        formule = Formule.query.get(formule_id) if formule_id else Formule()
        formule.nom = form.get('nom')
        formule.prix = float(form.get('prix') or 0)

        if not formule_id:
            db.session.add(formule)
        db.session.commit()
        return redirect(url_for('programmation_formules', formule_id=formule.id))

    @app.route('/programmer/formules/<int:formule_id>/add_composant', methods=['POST'])
    def add_composant_formule(formule_id):
        article_id = request.form.get('article_id', type=int)
        if article_id:
            composant = FormuleComposant(formule_id=formule_id, article_id=article_id)
            db.session.add(composant)
            db.session.commit()
        return redirect(url_for('programmation_formules', formule_id=formule_id))

    @app.route('/programmer/formules/<int:composant_id>/delete_composant')
    def delete_composant_formule(composant_id):
        composant = FormuleComposant.query.get_or_404(composant_id)
        formule_id = composant.formule_id
        db.session.delete(composant)
        db.session.commit()
        return redirect(url_for('programmation_formules', formule_id=formule_id))

    @app.route("/programmation/formules/supprimer_composant")
    def remove_composant_formule():
        formule_id = request.args.get("formule_id")
        article_id = request.args.get("article_id")

        formule = Formule.query.get(formule_id)
        article = Article.query.get(article_id)

        if formule and article:
            formule.composants.remove(article)
            db.session.commit()

        return redirect(url_for('programmation_formules', formule_id=formule_id))

    @app.route('/programmer/formules/delete/<int:formule_id>')
    def delete_formule(formule_id):
        formule = Formule.query.get_or_404(id)
        desaffecter_boutons('formule', id)
        db.session.delete(formule)
        db.session.commit()
        return redirect(url_for('programmation_formules'))

# Configuration du ticket de caisse
    @app.route('/configuration/ticket', methods=['GET'])
    def configuration_ticket():
        config = TicketConfig.query.first()
        if not config:
            config = TicketConfig()
            db.session.add(config)
            db.session.commit()
        return render_template('configuration.html', config=config)

    @app.route('/configuration/ticket/save', methods=['POST'])
    def save_ticket_config():
        config = TicketConfig.query.first()
        if not config:
            config = TicketConfig()
            db.session.add(config)

        form = request.form
        config.nom_commerce = form.get('nom_commerce')
        config.adresse = form.get('adresse')
        config.siret = form.get('siret')
        config.tva_intra = form.get('tva_intra')
        config.entete_ligne1 = form.get('entete_ligne1')
        config.entete_ligne2 = form.get('entete_ligne2')
        config.pied_ligne1 = form.get('pied_ligne1')
        config.pied_ligne2 = form.get('pied_ligne2')
        config.pied_ligne3 = form.get('pied_ligne3')
        config.pied_ligne4 = form.get('pied_ligne4')

        db.session.commit()
        return redirect(url_for('configuration_ticket'))

# Configuration des utilisateurs


    @app.route('/configuration/utilisateurs/save', methods=['POST'])
    def save_utilisateur():
        form = request.form
        id = form.get('id', type=int)
        utilisateur = Utilisateur.query.get(id) if id else Utilisateur()

        utilisateur.nom = form.get('nom')
        utilisateur.code = form.get('code')
        utilisateur.profil_id = form.get('profil_id') or None
        utilisateur.clavier_id = form.get('clavier_id') or None
        utilisateur.mode_vente = form.get('mode_vente')
        utilisateur.imprimante_id = form.get('imprimante_id') or None

        db.session.add(utilisateur)
        db.session.commit()

        return redirect(url_for('configuration_page'))

    @app.route('/configuration/utilisateurs/delete/<int:id>', methods=['GET'])
    def delete_utilisateur(id):
        utilisateur = Utilisateur.query.get_or_404(id)
        desaffecter_boutons('utilisateur', id)
        db.session.delete(utilisateur)
        db.session.commit()
        return redirect(url_for('configuration_page'))

# Configuration des profils
    config_bp = Blueprint('config', __name__)
    @config_bp.route("/configuration/profils")
    def configuration_profils():
        profils = Profil.query.all()
        return render_template("configuration_profils.html", profils=profils)

    @app.route('/configuration_profil')
    def configuration_profil():
        profils = Profil.query.all()
        utilisateurs = Utilisateur.query.all()
        return render_template('configuration.html', profils=profils, utilisateurs=utilisateurs)

    @config_bp.route("/configuration/profils/save", methods=["POST"])
    def save_profil():
        form = request.form
        profil_id = form.get("id")

        if profil_id:
            profil = Profil.query.get(profil_id)
        else:
            profil = Profil()

        profil.nom = form["nom"]
        # Checkboxes booléennes
        for field in Profil.__table__.columns.keys():
            if field != "id" and field != "nom":
                setattr(profil, field, form.get(field) == "on")

        db.session.add(profil)
        db.session.commit()
        return redirect(url_for("config.configuration_profils"))

    @config_bp.route("/configuration/profils/delete/<int:id>")
    def delete_profil(id):
        profil = Profil.query.get_or_404(id)
        db.session.delete(profil)
        db.session.commit()
        return redirect(url_for("config.configuration_profils"))

    @app.route('/configuration/profils/save', methods=['POST'])
    def save_profil():
        id = request.form.get('id')
        profil = Profil.query.get(id) if id else Profil()

        profil.nom = request.form.get('nom')

        # Accès
        profil.acces_vente = 'acces_vente' in request.form
        profil.acces_programmation = 'acces_programmation' in request.form
        profil.acces_gestion = 'acces_gestion' in request.form
        profil.acces_configuration = 'acces_configuration' in request.form
        profil.acces_clients = 'acces_clients' in request.form

        # Autorisations
        profil.autorise_offert = 'autorise_offert' in request.form
        profil.autorise_annuler_ligne = 'autorise_annuler_ligne' in request.form
        profil.autorise_annuler_avant_enc = 'autorise_annuler_avant_enc' in request.form
        profil.autorise_annuler_apres_enc = 'autorise_annuler_apres_enc' in request.form
        profil.autorise_annuler_attente = 'autorise_annuler_attente' in request.form
        profil.autorise_remises = 'autorise_remises' in request.form
        profil.autorise_changement_tarif = 'autorise_changement_tarif' in request.form
        profil.autorise_mise_attente = 'autorise_mise_attente' in request.form
        profil.autorise_transfert_table = 'autorise_transfert_table' in request.form
        profil.autorise_transfert_compte = 'autorise_transfert_compte' in request.form
        profil.autorise_modif_couverts = 'autorise_modif_couverts' in request.form

        # Créations
        profil.creation_utilisateur = 'creation_utilisateur' in request.form
        profil.creation_client = 'creation_client' in request.form
        profil.creation_carte = 'creation_carte' in request.form
        profil.creation_avoir = 'creation_avoir' in request.form

        # Modifications
        profil.modif_utilisateur = 'modif_utilisateur' in request.form
        profil.modif_client = 'modif_client' in request.form
        profil.modif_carte = 'modif_carte' in request.form
        profil.modif_avoir = 'modif_avoir' in request.form

        # Suppressions
        profil.suppr_utilisateur = 'suppr_utilisateur' in request.form
        profil.suppr_client = 'suppr_client' in request.form
        profil.suppr_carte = 'suppr_carte' in request.form
        profil.suppr_avoir = 'suppr_avoir' in request.form

        if not id:
            db.session.add(profil)

        db.session.commit()
        return redirect(url_for('configuration'))

    @app.route('/configuration/imprimantes/save', methods=['POST'])
    def save_imprimante():
        nom = request.form.get('nom')
        emplacement = request.form.get('emplacement')
        type_impr = request.form.get('type')

        imprimante = Imprimante(nom=nom, emplacement=emplacement, type=type_impr)
        db.session.add(imprimante)
        db.session.commit()
        return redirect(url_for('configuration_imprimantes'))

    @app.route('/configuration/peripheriques/imprimantes/delete/<int:id>', methods=['POST'])
    def delete_imprimante(id):
        imprimante = Imprimante.query.get_or_404(id)
        db.session.delete(imprimante)
        db.session.commit()
        return redirect(url_for('configuration_imprimantes'))

    @app.route('/configuration/peripheriques/imprimantes', methods=['GET', 'POST'])
    def configuration_imprimantes():
        if request.method == 'POST':
            id_ = request.form.get('id')
            nom = request.form.get('nom')
            type_impr = request.form.get('type')
            nom_windows = request.form.get('nom_windows')
            port_com = request.form.get('port_com')
            vitesse = request.form.get('vitesse')
            bit_donnee = request.form.get('bit_donnee')
            bit_arret = request.form.get('bit_arret')
            parite = request.form.get('parite')
            controle_flux = request.form.get('controle_flux')

            if id_:
                imprimante = Imprimante.query.get(id_)
            else:
                imprimante = Imprimante()

            imprimante.nom = nom
            imprimante.type = type_impr
            imprimante.nom_windows = nom_windows
            imprimante.port_com = int(port_com) if port_com else None
            imprimante.vitesse = vitesse
            imprimante.bit_donnee = bit_donnee
            imprimante.bit_arret = bit_arret
            imprimante.parite = parite
            imprimante.controle_flux = controle_flux

            db.session.add(imprimante)
            db.session.commit()
            return redirect(url_for('configuration_imprimantes'))

        imprimantes = Imprimante.query.all()
        imprimantes_windows = get_windows_printers()  # si tu utilises win32print
        return render_template('configuration_imprimantes.html', imprimantes=imprimantes, imprimante=None,
                               imprimantes_windows=imprimantes_windows)

    @app.route('/configuration/peripheriques/imprimantes/edit/<int:id>')
    def edit_imprimante(id):
        imprimante = Imprimante.query.get_or_404(id)
        imprimantes = Imprimante.query.all()
        return render_template('configuration_imprimantes.html', imprimantes=imprimantes, imprimante=imprimante)

