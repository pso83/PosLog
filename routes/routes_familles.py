from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Groupe, Famille, SousFamille

familles_bp = Blueprint('familles_bp', __name__)

@familles_bp.route('/parametrage/familles')
def gestion_familles():
    groupes = Groupe.query.all()
    familles = Famille.query.all()
    sous_familles = SousFamille.query.all()
    return render_template('parametrage_familles.html', groupes=groupes, familles=familles, sous_familles=sous_familles)

@familles_bp.route('/parametrage/familles/save', methods=['POST'])
def save_famille():
    type_ = request.form['type']
    nom = request.form['nom']
    parent_id = request.form.get('parent_id')

    if type_ == 'groupe':
        db.session.add(Groupe(nom=nom))
    elif type_ == 'famille':
        db.session.add(Famille(nom=nom, groupe_id=parent_id))
    elif type_ == 'sous_famille':
        db.session.add(SousFamille(nom=nom, famille_id=parent_id))

    db.session.commit()
    return redirect(url_for('familles_bp.gestion_familles'))
