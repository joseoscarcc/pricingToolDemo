from app.extensions import db
from sqlalchemy import and_, case, func

class precios_site(db.Model):
    __tablename__ = 'precios_site'

    place_id = db.Column(db.Text, primary_key=True)
    prices = db.Column(db.Float(8))
    product = db.Column(db.Text)
    date = db.Column(db.Date)

    # Define the foreign key relationship to demo_competencia
    demo_competencia_id = db.Column(db.Integer, db.ForeignKey('demo_competencia.place_id'))


class demo_competencia(db.Model):
    __tablename__ = 'demo_competencia'

    id_micromercado = db.Column(db.Integer, primary_key=True)
    id_estacion = db.Column(db.Integer)
    place_id = db.Column(db.Integer)
    cre_id = db.Column(db.Text)
    marca = db.Column(db.Text)
    distancia = db.Column(db.Float)
    x = db.Column(db.Float)
    y = db.Column(db.Float)
    compite_a = db.Column(db.Integer)

    # Define the one-to-many relationship to precios_site
    precios = db.relationship('precios_site', backref='demo_competencia')

class demo_sites(db.Model):
    place_id = db.Column(db.Integer, primary_key=True)
    cre_id = db.Column(db.Text)
    nombre = db.Column(db.Text)
    rfc = db.Column(db.Text)
    x = db.Column(db.Float)
    y = db.Column(db.Float)
    municipio = db.Column(db.Text)
    estado = db.Column(db.Text)
    terminal = db.Column(db.Text)
    marca = db.Column(db.Text)
    address = db.Column(db.Text)
    geolocation = db.Column(db.Text)
    codigo_postal = db.Column(db.Text)
    es_norte = db.Column(db.Text)

def round_float(value):
    if isinstance(value, float):
        return round(value, 2)
    else:
        return value

def get_site_data():
    result = demo_sites.query.with_entities(
        demo_sites.place_id,
        demo_sites.cre_id,
        demo_sites.marca,
        demo_sites.municipio
    ).all()

    site_list = []
    for row in result:
        place_id = row.place_id
        cre_id = row.cre_id
        marca = row.marca
        municipio = row.municipio

        site_data = {
            'place_id': place_id,
            'cre_id': cre_id,
            'marca': marca,
            'municipio': municipio
        }

        site_list.append(site_data)

    return site_list

def get_unique_municipios():
    result = demo_sites.query.with_entities(demo_sites.municipio).distinct().all()
    municipios = [row[0] for row in result]
    return municipios

def get_site_data_by_municipio(municipio):
    result = demo_sites.query.with_entities(demo_sites.place_id).filter_by(municipio=municipio).all()
    place_ids = [row[0] for row in result]
    return place_ids

def get_place_id_by_cre_id(target_cre_id):
    site = demo_sites.query.filter_by(cre_id=target_cre_id).first()

    return site.place_id

def get_data_table():
    latest_date = db.session.query(func.max(precios_site.date)).scalar()
    hoy = get_precios_competencia(latest_date)
    dia_anterior = db.session.query(func.max(precios_site.date) - 1).scalar()
    ayer = get_precios_competencia(dia_anterior)
    return hoy

def get_precios_competencia(fecha):
    
    given_date = fecha
    coalesce_value = '-'
    round_digits = 2    

    result = db.session.query(
        demo_competencia.id_micromercado,
        demo_competencia.id_estacion,
        demo_competencia.cre_id,
        demo_competencia.place_id,
        demo_competencia.marca,
        func.coalesce(
            func.max(case((precios_site.product == 'regular', func.cast(precios_site.prices, db.Text))), else_="-"),
            "-"
        ).label('regular_prices'),
        func.coalesce(
            func.max(case((precios_site.product == 'premium', func.cast(precios_site.prices, db.Text))), else_="-"),
            "-"
        ).label('premium_prices'),
        func.coalesce(
            func.max(case((precios_site.product == 'diesel', func.cast(precios_site.prices, db.Text))), else_="-"),
            "-"
        ).label('diesel_prices')
    ).outerjoin(
        precios_site,
        and_(
            func.cast(demo_competencia.place_id, db.Text) == precios_site.place_id,
            precios_site.date == given_date
        )
    ).group_by(
        demo_competencia.id_micromercado,
        demo_competencia.id_estacion,
        demo_competencia.cre_id,
        demo_competencia.place_id,
        demo_competencia.marca
    ).order_by(
        demo_competencia.id_micromercado,
        demo_competencia.id_estacion
    ).all()

    return result

    
