from flask import Flask, render_template, request, redirect, url_for
from models import db
from models.article import db
from models.article import Article
from models.clavier import Clavier
from models.tva import Tva
from models.groupe import Groupe
from models.famille import Famille
from models.sous_famille import SousFamille
from models.reglement import Reglement
from models.commentaire import Commentaire
from models.menu import Menu
from models.formule import Formule


def register_routes(app):

    @app.route('/programmation/elements', methods=['GET'])
    def show_programmation_elements():
        return render_template('programmation_elements.html')

    @app.route('/programmation/claviers', methods=['POST'])
    def add_clavier():
        nom = request.form.get('nom')
        if nom:
            db.session.add(Clavier(nom=nom))
            db.session.commit()
        return redirect('/programmation/elements')

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
        nom = request.form.get('nom_article', '')
        prix1 = float(request.form.get('prix_1') or 0)
        prix2 = float(request.form.get('prix_2') or 0)
        prix3 = float(request.form.get('prix_3') or 0)
        prix4 = float(request.form.get('prix_4') or 0)
        tva_id = request.form.get('tva_id') or ''

        def checkbox(name): return name in request.form

        article = Article(
            nom_article=nom,
            prix_1=prix1,
            prix_2=prix2,
            prix_3=prix3,
            prix_4=prix4,
            tva_id=tva_id,
            prix_manuel=checkbox('prix_manuel'),
            vendu_au_poids=checkbox('vendu_au_poids'),
            avec_code_barre=checkbox('avec_code_barre'),
            eligible_fidelite=checkbox('eligible_fidelite'),
            retour_autorise=checkbox('retour_autorise'),
            avoir_autorise=checkbox('avoir_autorise'),
            gere_stock=checkbox('gere_stock'),
            vendu_en_negatif=checkbox('vendu_en_negatif'),
            hors_ca=checkbox('hors_ca'),
            est_menu=checkbox('est_menu'),
            est_formule=checkbox('est_formule'),
            composant_menu=checkbox('composant_menu'),
            composant_formulaire=checkbox('composant_formulaire'),
            appel_commentaire=checkbox('appel_commentaire'),
            imprimable_preparation=checkbox('imprimable_preparation'),
            invisible_telecommande=checkbox('invisible_telecommande'),
            vente_a_distance=checkbox('vente_a_distance'),
            gere_heure=checkbox('gere_heure'),
            depot_vente=checkbox('depot_vente'),
            gere_sav=checkbox('gere_sav')
        )

        db.session.add(article)
        db.session.commit()

        return redirect(url_for('programmation_articles'))

    @app.route('/programmer/articles')
    def programmation_articles():
        from models.article import Article
        from models.tva import Tva
        article_id = request.args.get('id')
        article = Article.query.get(article_id) if article_id else None
        articles = Article.query.all()
        tva_options = ['5.5', '10', '20']
        return render_template('programmation_articles.html', articles=articles, article=article,
                               tva_options=tva_options)
def register_programmation_routes(app):
    @app.route('/programmer/articles', methods=['GET'])
    def programmer_articles():
        print("📍 Route /programmer/articles appelée")
        articles = Article.query.all()
        tva_options = [str(t.taux) for t in Tva.query.all()]
        return render_template('programmation_articles.html', articles=articles, tva_options=tva_options)


