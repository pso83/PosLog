from . import db

class Menu(db.Model):
    __tablename__ = 'menu'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)

    pages = db.relationship("MenuPage", back_populates="menu", cascade="all, delete-orphan")

menu_page_articles = db.Table(
    'menu_page_articles',
    db.Column('menu_page_id', db.Integer, db.ForeignKey('menu_pages.id'), primary_key=True),
    db.Column('article_id', db.Integer, db.ForeignKey('articles.id'), primary_key=True)
)