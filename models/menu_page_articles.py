from extensions import db

menu_page_articles = db.Table(
    'menu_page_articles',
    db.Column('menu_page_id', db.Integer, db.ForeignKey('menu_pages.id'), primary_key=True),
    db.Column('article_id', db.Integer, db.ForeignKey('articles.id'), primary_key=True)
)
