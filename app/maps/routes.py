from flask import render_template, jsonify, flash,request, redirect,url_for, session, current_app
from app.maps import bp
from app.extensions import db
from config import Config
from sqlalchemy import func, cast, Integer
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from app.models.precios import precios_site,demo_competencia,round_float,get_site_data,get_unique_municipios,get_site_data_by_municipio
from app.models.auth import login_required
import os


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index(municipio_value=None, product_value=None):
    title="Mapa Precios"

    if request.method == 'POST':
        municipio_value = request.form.get('municipio')
        product_value = request.form.get('product')

    if municipio_value is None:
         municipio_value = 'Rosario'
    if product_value is None:
        product_value = 'regular'
    
    if municipio_value == 'Hermosillo':
        citylat = 29.06933
        citylon = -110.9706
    elif municipio_value == "Merida":
        citylat = 20.94868
        citylon = -89.64977
    elif municipio_value == "Puebla":
        citylat = 19.0257
        citylon = -98.20509
    elif municipio_value == "Torreon":
        citylat = 25.54993
        citylon = -103.4232
    elif municipio_value == "Tijuana":
        citylat = 32.51887
        citylon = -117.0121
    elif municipio_value == "Cuahutemoc":
        citylat = 19.4191
        citylon = -99.1573
    elif municipio_value == "Rosario":
        citylat = 22.992528
        citylon = -105.860553

    place_ids = get_site_data_by_municipio(municipio_value)

    latest_date = (
        db.session.query(func.max(precios_site.date))
        .scalar()
    )

    results = (
        precios_site.query.join(demo_competencia, cast(precios_site.place_id, Integer) == demo_competencia.place_id)
        .filter(demo_competencia.compite_a.in_(place_ids))
        .filter(precios_site.product == product_value)
        .filter(precios_site.date == latest_date)
        .with_entities(
            demo_competencia.cre_id,
            demo_competencia.marca,
            precios_site.prices,
            demo_competencia.x,
            demo_competencia.y
        )
        .all()
    )

    rows = []
    
    for result in results:
        row = {
            'marca': result.marca,
            'cre_id': result.cre_id,
            'precio': result.prices,
            'x': result.x,
            'y': result.y,
        }
        row['text'] = '" '+row['marca'] + ' ' + row['cre_id'] + ', Precio: ' + str(row['precio'])+' "'
        rows.append(row)

    x_values = [row['x'] for row in rows]
    y_values = [row['y'] for row in rows]
    text_values = [row['text'] for row in rows]
    map_box = Config.mapbox_access_token
    return render_template('maps/mapa.html',title=title,
                           x = x_values,
                           y = y_values,
                           texto = text_values,
                           citylat=citylat,
                           citylon=citylon,
                           map_box = map_box)

@bp.route('/municipios/', methods=['GET'])
def get_municipios():
    municipios = get_unique_municipios()
    return jsonify({'municipios': municipios})

@bp.route('/data/', methods=['GET'])
@bp.route('/data/<int:municipio_value>/<string:product_value>', methods=['GET'])
@login_required
def data(municipio_value=None, product_value=None):

    if municipio_value is None:
         municipio_value = 'Hermosillo'
    if product_value is None:
        product_value = 'regular'

    place_ids = get_site_data_by_municipio(municipio_value)

    latest_date = (
        db.session.query(func.max(precios_site.date))
        .scalar()
    )

    results = (
        precios_site.query.join(demo_competencia, cast(precios_site.place_id, Integer) == demo_competencia.place_id)
        .filter(demo_competencia.compite_a.in_(place_ids))
        .filter(precios_site.product == product_value)
        .filter(precios_site.date == latest_date)
        .with_entities(
            demo_competencia.cre_id,
            demo_competencia.marca,
            precios_site.prices,
            demo_competencia.x,
            demo_competencia.y
        )
        .all()
    )

    rows = []
    
    for result in results:
        row = {
            'marca': result.marca,
            'cre_id': result.cre_id,
            'precio': result.prices,
            'x': result.x,
            'y': result.y,
        }
        row['text'] = row['marca'] + ' ' + row['cre_id'] + ', Precio: ' + str(row['precio'])
        rows.append(row)

    return jsonify({'data': rows })


