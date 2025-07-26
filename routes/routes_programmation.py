# routes/routes_programmation.py

from flask import (
    render_template, request, redirect, url_for, flash,
    jsonify, send_file, Blueprint
)
from extensions import db
import json, io
from io import BytesIO

# Modèles génériques
from models.article import Article
from models.Groupe import Groupe
from models.Famille import Famille
from models.SousFamille import SousFamille
from models.tva import Tva
from models.reglement import Reglement
from models.commentaire import Commentaire, ElementCommentaire
from models.menu import Menu
from models.menu_page import MenuPage
from models.formule import Formule, FormuleComposant

# Modèles Claviers Produits / Fonctions
from models.clavier_produit import ClavierProduit, BoutonProduit
from models.clavier_fonction import ClavierFonction, BoutonFonction


def register_programmation_routes(app):

    # ─── CLAVIERS PRODUITS ────────────────────────────────────────────────

    @app.route('/programmer/produits/claviers', methods=['GET', 'POST'])
    def claviers_produits():
        if request.method == 'POST':
            nom = request.form.get('nom', '').strip()
            if nom:
                c = ClavierProduit(nom=nom)
                db.session.add(c); db.session.commit()
                flash(f"Clavier produit « {nom} » créé.", "success")
                return redirect(url_for('claviers_produits',
                                        clavier_id=c.id))
        claviers = ClavierProduit.query.order_by(ClavierProduit.nom).all()
        cid      = request.args.get('clavier_id', type=int)
        clavier  = (ClavierProduit.query.get(cid)
                    if cid else (claviers[0] if claviers else None))
        return render_template(
            'programmation_claviers.html',
            claviers=claviers,
            clavier=clavier,
            is_fonction=False,
            message=request.args.get('message'),
            message_type=request.args.get('message_type')
        )

    @app.route('/programmer/produits/claviers/<int:id>/supprimer', methods=['POST'])
    def supprimer_clavier_produit(id):
        c = ClavierProduit.query.get_or_404(id)
        db.session.delete(c); db.session.commit()
        flash(f"Clavier produit « {c.nom} » supprimé.", "warning")
        return redirect(url_for('claviers_produits'))

    @app.route('/programmer/produits/boutons/<int:clavier_id>')
    def boutons_produits(clavier_id):
        bts = BoutonProduit.query.filter_by(clavier_id=clavier_id).all()
        return jsonify([{
            'id':            b.id,
            'position':      b.position,
            'nom':           getattr(b, 'label', None),
            'couleur':       b.couleur,
            'text_color':    b.text_color,
            'image':         b.image,
            'masquer_texte': b.masquer_texte
        } for b in bts])

    @app.route('/programmer/produits/boutons/effacer', methods=['POST'])
    def effacer_bouton_produit():
        cid = request.args.get('clavier_id', type=int)
        pos = request.form.get('effacerPosition', type=int)
        if cid and pos:
            BoutonProduit.query.filter_by(
                clavier_id=cid, position=pos
            ).delete()
            db.session.commit()
            flash(f"Bouton position {pos} effacé.", "info")
        return redirect(url_for('claviers_produits', clavier_id=cid))

    @app.route('/programmer/produits/lignes/effacer', methods=['POST'])
    def effacer_ligne_produit():
        cid   = request.args.get('clavier_id', type=int)
        ligne = request.form.get('effacerLigne', type=int)
        if cid and ligne:
            start = (ligne - 1) * 5 + 1
            end   = ligne * 5
            BoutonProduit.query.filter(
                BoutonProduit.clavier_id == cid,
                BoutonProduit.position.between(start, end)
            ).delete(synchronize_session=False)
            db.session.commit()
            flash(f"Ligne {ligne} effacée.", "info")
        return redirect(url_for('claviers_produits', clavier_id=cid))


    # ─── CLAVIERS FONCTIONS ───────────────────────────────────────────────

    @app.route('/programmer/fonctions/claviers', methods=['GET', 'POST'])
    def claviers_fonctions():
        if request.method == 'POST':
            nom = request.form.get('nom', '').strip()
            if nom:
                c = ClavierFonction(nom=nom)
                db.session.add(c); db.session.commit()
                flash(f"Clavier fonction « {nom} » créé.", "success")
                return redirect(url_for('claviers_fonctions',
                                        clavier_id=c.id))
        claviers = ClavierFonction.query.order_by(ClavierFonction.nom).all()
        cid      = request.args.get('clavier_id', type=int)
        clavier  = (ClavierFonction.query.get(cid)
                    if cid else (claviers[0] if claviers else None))
        return render_template(
            'programmation_claviers.html',
            claviers=claviers,
            clavier=clavier,
            is_fonction=True,
            message=request.args.get('message'),
            message_type=request.args.get('message_type')
        )

    @app.route('/programmer/fonctions/claviers/<int:id>/supprimer', methods=['POST'])
    def supprimer_clavier_fonction(id):
        c = ClavierFonction.query.get_or_404(id)
        db.session.delete(c); db.session.commit()
        flash(f"Clavier fonction « {c.nom} » supprimé.", "warning")
        return redirect(url_for('claviers_fonctions'))

    @app.route('/programmer/fonctions/boutons/<int:clavier_id>')
    def boutons_fonctions(clavier_id):
        bts = BoutonFonction.query.filter_by(
            clavier_id=clavier_id
        ).all()
        return jsonify([{
            'id':            b.id,
            'position':      b.position,
            'nom':           getattr(b, 'label', None),
            'couleur':       b.couleur,
            'text_color':    b.text_color,
            'image':         b.image,
            'masquer_texte': b.masquer_texte
        } for b in bts])

    @app.route('/programmer/fonctions/boutons/effacer', methods=['POST'])
    def effacer_bouton_fonction():
        cid = request.args.get('clavier_id', type=int)
        pos = request.form.get('effacerPosition', type=int)
        if cid and pos:
            BoutonFonction.query.filter_by(
                clavier_id=cid, position=pos
            ).delete()
            db.session.commit()
            flash(f"Bouton position {pos} effacé.", "info")
        return redirect(url_for('claviers_fonctions', clavier_id=cid))

    @app.route('/programmer/fonctions/lignes/effacer', methods=['POST'])
    def effacer_ligne_fonction():
        cid   = request.args.get('clavier_id', type=int)
        ligne = request.form.get('effacerLigne', type=int)
        if cid and ligne:
            start = (ligne - 1) * 4 + 1
            end   = ligne * 4
            BoutonFonction.query.filter(
                BoutonFonction.clavier_id == cid,
                BoutonFonction.position.between(start, end)
            ).delete(synchronize_session=False)
            db.session.commit()
            flash(f"Ligne {ligne} effacée.", "info")
        return redirect(url_for('claviers_fonctions', clavier_id=cid))


    # ─── ÉLÉMENTS DE PROGRAMMATION GÉNÉRIQUES ────────────────────────────

    @app.route('/programmer/elements')
    def programmation_elements():
        return render_template('programmation_elements.html')

    @app.route('/programmer/articles', methods=['GET','POST'])
    def programmation_articles():
        # … code inchangé de gestion des articles …
        pass

    @app.route('/programmer/groupes', methods=['GET','POST'])
    def programmation_groupes():
        # … code génération, filtres…
        pass

    @app.route('/programmer/familles', methods=['GET','POST'])
    def programmation_familles():
        pass

    @app.route('/programmer/sousfamilles', methods=['GET','POST'])
    def programmation_sousfamilles():
        pass

    @app.route('/programmer/tva', methods=['GET','POST'])
    def programmation_tva():
        pass

    @app.route('/programmer/reglements', methods=['GET','POST'])
    def programmation_reglements():
        pass

    @app.route('/programmer/commentaires', methods=['GET','POST'])
    def programmation_commentaires():
        pass

    @app.route('/programmer/menus', methods=['GET','POST'])
    def programmation_menus():
        pass

    @app.route('/programmer/menus/add_page', methods=['POST'])
    def add_menu_page():
        pass

    @app.route('/programmer/formules', methods=['GET','POST'])
    def programmation_formules():
        pass

    @app.route('/programmer/formules/<int:composant_id>/delete_composant')
    def delete_composant_formule(composant_id):
        pass

    @app.route('/programmer/formules/delete/<int:formule_id>')
    def delete_formule(formule_id):
        pass


    # ─── CONFIGURATION TICKET, UTILISATEURS, PROFILS, IMPRIMANTES ────────

    @app.route('/configuration/ticket', methods=['GET','POST'])
    def configuration_ticket():
        pass

    @app.route('/configuration/utilisateurs', methods=['GET','POST'])
    def configuration_utilisateurs():
        pass

    @app.route('/configuration/profils', methods=['GET','POST'])
    def configuration_profils():
        pass

    @app.route('/configuration/imprimantes', methods=['GET','POST'])
    def configuration_imprimantes():
        pass

    # … autres routes de configuration …

