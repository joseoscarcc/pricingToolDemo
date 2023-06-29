from flask import Blueprint

bp = Blueprint('reporte', __name__)


from app.reporte import routes