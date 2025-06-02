from models import db

class MenuPage(db.Model):
    __tablename__ = 'menu_pages'
    id = db.Column(db.Integer, primary_key=True)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'))
    nom_page = db.Column(db.String(100), nullable=False)

    menu = db.relationship("Menu", back_populates="pages")
    articles = db.relationship(
        "Article",
        secondary="menu_page_articles",
        back_populates="menu_pages"
    )


