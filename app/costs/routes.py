from flask import render_template, jsonify, flash, request
from app.costs import bp
from app.extensions import db
from app.models.auth import login_required
from app.models.costs import costos_pemex, terminales, get_terminal_info, get_terminal_data
import plotly.graph_objects as go
from sqlalchemy import cast, Integer
import pandas as pd
import plotly
import plotly.express as px
import json
import numpy as np
from datetime import datetime, timedelta
import json

@bp.route('/', methods=['GET', 'POST'])
@login_required
def index(terminal_value=None):
    title="Dashboard Costos"

    if request.method == 'POST':
        terminal_value = int(request.form.get('terminal'))
        
    if terminal_value is None:
         terminal_value = 699

    costos = get_terminal_info(terminal_value)
    regular = {
        "hoy": costos['hoy_regular_price'],
        "ayer": costos['ayer_regular_price']
    }
    premium = {
        "hoy": costos['hoy_premium_price'],
        "ayer": costos['ayer_premium_price']
    }
    diesel = {
        "hoy":costos['hoy_diesel_price'],
        "ayer":costos['ayer_diesel_price']
    }
    fechas = {
        "hoy":str(costos['hoy']),
        "ayer":str(costos['ayer'])
    }

    grafica = get_terminal_data(terminal_value)

    regular_grafica = [row['precio_tar'] for row in grafica if row['producto'] == 'regular']
    premium_grafica = [row['precio_tar'] for row in grafica if row['producto'] == 'premium']
    diesel_grafica = [row['precio_tar'] for row in grafica if row['producto'] == 'diesel']
    fechas_grafica = [row['date'] for row in grafica if row['producto'] == 'regular']
    # Render the template and pass the JSON data to it
    return render_template('costs/costs.html', title=title,
                           regular = json.dumps(regular), 
                           premium=json.dumps(premium),
                           diesel=json.dumps(diesel),
                           fechas=json.dumps(fechas),
                           regular_grafica=json.dumps(regular_grafica),
                           premium_grafica=json.dumps(premium_grafica),
                           diesel_grafica=json.dumps(diesel_grafica),
                           fecha_grafica=json.dumps(fechas_grafica))

@bp.route('/terminales/', methods=['GET'])
@login_required
def get_terminales():
    Terminales = terminales()
    return jsonify({'terminales': Terminales}), 200, {'Content-Type': 'application/json; charset=utf-8'}
