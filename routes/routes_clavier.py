from flask import render_template, request, redirect, url_for, jsonify
from models import db
from models.article import Article
from models.clavier import Clavier, ClavierBouton
from models.bouton_clavier import BoutonClavier

def register_clavier_routes(app):

    @app.route('/programmer/claviers', methods=['GET'])
    def afficher_claviers():
        claviers = Clavier.query.all()
        clavier_id = request.args.get('clavier_id', type=int)

        if clavier_id:
            clavier = Clavier.query.get(clavier_id)
        elif claviers:
            clavier = claviers[0]
        else:
            clavier = None

        boutons = {}
        if clavier:
            boutons_bruts = BoutonClavier.query.filter_by(clavier_id=clavier.id).all()
            boutons = {b.position: b.to_dict() for b in boutons_bruts}

        return render_template('programmation_claviers.html', claviers=claviers, clavier=clavier, boutons=boutons)

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


