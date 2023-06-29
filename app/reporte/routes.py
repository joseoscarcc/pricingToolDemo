from flask import render_template,jsonify,request
from app.reporte import bp
from app.extensions import db
import pandas as pd
import numpy as np
from app.models.auth import login_required
from app.models.reporte import promedio_last_7_days
from app.models.configuracion import get_unique_estados
import json

@bp.route('/', methods=['GET', 'POST'])
@login_required
def index(estado=None):
    title="Dashboard Reporte"
    if request.method == 'POST':
        estado = request.form.get('estado')

    averages = promedio_last_7_days(estado)
    
    return render_template('reporte/reporte.html', title=title, averages = averages)

@bp.route('/estados/', methods=['GET'])
def estados():
    unique_estados = get_unique_estados()
    print(unique_estados)

    return jsonify({'estados': unique_estados})