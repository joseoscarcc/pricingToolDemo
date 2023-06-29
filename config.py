import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    mapbox_access_token = os.environ.get('mapbox_access_token')
    type_1 = os.environ.get('type_1')
    type_2 = os.environ.get('type_2')
    
