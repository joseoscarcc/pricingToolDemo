from flask import Blueprint

bp = Blueprint('ieps', __name__)

from app.ieps import routes