from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file, flash
from models import db, article, Groupe, Famille, SousFamille, tva
from models.article import db
from models.article import Article
from models.clavier import Clavier
from models.bouton_clavier import BoutonClavier
from models.tva import Tva
from models.Groupe import Groupe
from models.Famille import Famille
from models.SousFamille import SousFamille
from models.reglement import Reglement
from models.commentaire import Commentaire
from models.menu import Menu
from models.formule import Formule
from models.fonction import Fonction
from models.utilisateur import Utilisateur
from models.menu import Menu
from models.menu_page import MenuPage
import json
from datetime import datetime
from io import BytesIO

def register_routes(app):

    @app.route('/programmation/elements', methods=['GET'])
    def show_programmation_elements():
        return render_template('programmation_elements.html')

    # Route pour afficher la programmation des claviers
    @app.route('/programmer/claviers')
    def programmation_claviers():
        claviers = Clavier.query.all()
        clavier_id = request.args.get('clavier_id', type=int)
        clavier = Clavier.query.get(clavier_id) if clavier_id else claviers[0] if claviers else None

        boutons = {
            b.position: {
                'type': b.type,
                'element_id': b.element_id,
                'label': b.label,
                'couleur': b.couleur,
                'image': b.image,
                'masquer_texte': b.masquer_texte
            } for b in clavier.boutons
        } if clavier else {}

        return render_template('programmation_claviers.html', claviers=claviers, clavier=clavier, boutons=boutons)

    # Route pour créer un clavier
    @app.route('/clavier/creer', methods=['POST'])
    def creer_clavier():
        nom = request.form.get('nom')
        if nom:
            clavier = Clavier(nom=nom)
            db.session.add(clavier)
            db.session.commit()
        return redirect(url_for('programmation_claviers', message='Clavier créé'))

    # Route pour réinitialiser tous les boutons d'un clavier
    @app.route('/clavier/reset')
    def reset_clavier():
        clavier_id = request.args.get('clavier_id', type=int)
        clavier = Clavier.query.get(clavier_id)
        if clavier:
            BoutonClavier.query.filter_by(clavier_id=clavier.id).delete()
            db.session.commit()
        return redirect(url_for('programmation_claviers', message='Clavier réinitialisé', clavier_id=clavier_id))

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
        return redirect(url_for('programmation_claviers', message='Clavier dupliqué', clavier_id=nouveau.id))

    # Route pour exporter les boutons d'un clavier
    @app.route('/clavier/export/<int:id>')
    def export_clavier(id):
        clavier = Clavier.query.get_or_404(id)

        boutons = [
            {
                'position': b.position,
                'type': b.type,
                'element_id': b.element_id,
                'label': b.label,
                'couleur': b.couleur,
                'image': b.image,
                'masquer_texte': b.masquer_texte
            }
            for b in clavier.boutons  # ← boucle correcte ici
        ]

        export_json = json.dumps({
            'clavier_id': clavier.id,
            'clavier_nom': clavier.nom,
            'boutons': boutons
        }, ensure_ascii=False, indent=2)

        return send_file(
            BytesIO(export_json.encode('utf-8')),
            mimetype='application/json',
            as_attachment=True,
            download_name=f'clavier_{id}_export.json'
        )

    # Route pour importer des boutons dans un clavier
    from flask import request, redirect, url_for, flash
    import json

    @app.route('/clavier/import/<int:id>', methods=['POST'])
    def import_clavier(id):
        fichier = request.files.get('file')

        if not fichier or fichier.filename == '':
            flash("Aucun fichier sélectionné.")
            return redirect(url_for('afficher_claviers'))

        try:
            contenu = fichier.read().decode('utf-8')
            json_data = json.loads(contenu)
            boutons = json_data.get('boutons', [])

        except Exception as e:
            flash("Erreur lors du chargement du fichier JSON : " + str(e))
            return redirect(url_for('afficher_claviers'))

        # Supprimer les boutons existants du clavier
        BoutonClavier.query.filter_by(clavier_id=id).delete()

        for b in boutons:
            bouton = BoutonClavier(
                clavier_id=id,
                position=b.get('position'),
                type=b.get('type'),
                element_id=b.get('element_id'),
                label=b.get('label'),
                couleur=b.get('couleur', '#e0e0e0'),
                image=b.get('image', ''),
                masquer_texte=b.get('masquer_texte', False)
            )
            db.session.add(bouton)

        db.session.commit()
        flash("Importation réussie.")
        return redirect(url_for('afficher_claviers', clavier_id=id))

    # Route pour supprimer un bouton spécifique d'un clavier
    @app.route('/clavier/effacer_bouton/', methods=['POST'])
    def effacer_bouton():
        position = int(request.form.get('effacerPosition'))
        clavier_id = int(request.args.get('clavier_id', 1))
        bouton = BoutonClavier.query.filter_by(clavier_id=clavier_id, position=position).first()
        if bouton:
            db.session.delete(bouton)
            db.session.commit()
        return redirect(url_for('afficher_claviers', clavier_id=clavier_id))

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
        return redirect(url_for('afficher_claviers', clavier_id=clavier_id))

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
                 'est_menu', 'est_formule', 'composant_menu', 'composant_formulaire',
                 'appel_commentaire', 'imprimable_preparation', 'invisible_telecommande',
                 'vente_a_distance', 'gere_heure', 'depot_vente', 'gere_sav']
        for flag in flags:
            setattr(article, flag, flag in form)

        db.session.add(article)
        db.session.commit()
        return redirect(url_for('programmation_articles'))

    @app.route('/programmer/articles/delete/<int:id>')
    def delete_article(id):
        article = Article.query.get_or_404(id)
        db.session.delete(article)
        db.session.commit()
        return redirect(url_for('programmation_articles'))

def register_programmation_routes(app):
    @app.route('/programmer/articles', methods=['GET'])
    def programmation_articles():

        article_id = request.args.get('id')
        filtre_groupe = request.args.get('groupe')
        filtre_famille = request.args.get('famille')
        filtre_sous_famille = request.args.get('sous_famille')

        article = Article.query.get(article_id) if article_id else None

        query = Article.query
        if filtre_groupe:
            query = query.filter_by(groupe_id=filtre_groupe)
        if filtre_famille:
            query = query.filter_by(famille_id=filtre_famille)
        if filtre_sous_famille:
            query = query.filter_by(sous_famille_id=filtre_sous_famille)

        articles = query.all()

        return render_template(
            'programmation_articles.html',
            articles=articles,
            article=article,
            tva_options=Tva.query.all(),
            groupes=Groupe.query.all(),
            familles=Famille.query.all(),
            sous_familles=SousFamille.query.all()
        )

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

    @app.route('/programmer/menus/add_page', methods=['POST'])
    def add_menu_page():
        menu_id = request.form.get('menu_id', type=int)
        page_nom = request.form.get('page_nom')
        if menu_id and page_nom:
            page = MenuPage(nom=page_nom, menu_id=menu_id)
            db.session.add(page)
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
