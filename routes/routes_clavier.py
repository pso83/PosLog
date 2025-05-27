from flask import render_template, request, redirect, url_for
from models import db
from models.article import Article
from models.clavier import Clavier, ClavierBouton

def register_clavier_routes(app):

    @app.route('/programmer/claviers', methods=['GET'])
    def afficher_claviers():
        clavier = Clavier.query.first()
        boutons = {b.position: b.article for b in clavier.boutons} if clavier else {}
        return render_template('programmation_claviers.html', clavier=clavier, boutons=boutons)

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

    @app.route('/programmer/claviers/assign/save', methods=['POST'])
    def enregistrer_bouton():
        clavier_id = int(request.form.get('clavier_id'))
        position = int(request.form.get('position'))
        article_id = int(request.form.get('article_id'))

        bouton = ClavierBouton.query.filter_by(clavier_id=clavier_id, position=position).first()
        if bouton:
            bouton.article_id = article_id
        else:
            bouton = ClavierBouton(clavier_id=clavier_id, position=position, article_id=article_id)
            db.session.add(bouton)

        db.session.commit()
        return redirect(url_for('afficher_claviers'))
