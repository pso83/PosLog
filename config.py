import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://devlog:123456Sou_log@194.164.60.164:3306/ma_caisse'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'cle-secrete'
