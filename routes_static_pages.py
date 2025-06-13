from flask import render_template

def register_static_pages(app):
    @app.route('/vente')
    def vente():
        return render_template('vente.html')

    @app.route('/programmer')
    def programmer():
        return render_template('programmation.html')

    @app.route('/gestion')
    def gestion():
        return render_template('gestion.html')

    @app.route('/stocks')
    def stocks():
        return render_template('stocks.html')
