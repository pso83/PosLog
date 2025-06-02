from flask import render_template, request, redirect
from flask import Flask
from extensions import db # déjà en place
from models.clavier import Clavier
from models.tva import Tva
from models.Groupe import Groupe
from models.Famille import Famille
from models.SousFamille import SousFamille
from models.reglement import Reglement
from models.commentaire import Commentaire
from models.menu import Menu
from models.formule import Formule

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)

@app.route('/programmation/elements', methods=['GET'])
def show_programmation_elements():
    return render_template('programmation_elements.html')
