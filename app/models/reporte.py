from datetime import datetime, timedelta
from app.extensions import db
from sqlalchemy import func, cast, Integer
from sqlalchemy.types import Numeric
from app.models.configuracion import marcas_places
from app.models.precios import precios_site

def promedio_last_7_days(estados=None):
    # Calculate the date range for the last 7 days
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=6)

    end_date_01 = start_date - timedelta(days=7)
    start_date_01 = end_date_01 - timedelta(days=6)

    if estados != None:
        # Query and calculate the average prices by product and estado
        averages = db.session.query(
            precios_site.product,
            cast(func.avg(precios_site.prices), Numeric(8, 2)).label("Promedio"),
            cast(func.min(precios_site.prices), Numeric(8, 2)).label("Minimo"),
            cast(func.max(precios_site.prices), Numeric(8, 2)).label("Maximo")
        ).join(
            marcas_places, cast(precios_site.place_id, Integer) == cast(marcas_places.place_id, Integer)
        ).filter(
            precios_site.date >= start_date,
            precios_site.date <= end_date,
            marcas_places.es_norte != "Si",
            marcas_places.estado == estados
        ).group_by(
            precios_site.product,
        ).all()

        averages_01 = db.session.query(
            precios_site.product,
            cast(func.avg(precios_site.prices), Numeric(8, 2)).label("Promedio"),
            cast(func.min(precios_site.prices), Numeric(8, 2)).label("Minimo"),
            cast(func.max(precios_site.prices), Numeric(8, 2)).label("Maximo")
        ).join(
            marcas_places, cast(precios_site.place_id, Integer) == cast(marcas_places.place_id, Integer)
        ).filter(
            precios_site.date >= start_date_01,
            precios_site.date <= end_date_01,
            marcas_places.es_norte != "Si",
            marcas_places.estado == estados
        ).group_by(
            precios_site.product,
        ).all()
    else:
        # Calculate the average prices by product for all types of terminals (Pais)
        averages = db.session.query(
            precios_site.product,
            cast(func.avg(precios_site.prices), Numeric(8, 2)).label("Promedio"),
            cast(func.min(precios_site.prices), Numeric(8, 2)).label("Minimo"),
            cast(func.max(precios_site.prices), Numeric(8, 2)).label("Maximo")
        ).join( 
            marcas_places, cast(precios_site.place_id, Integer) == cast(marcas_places.place_id, Integer)
        ).filter(
            precios_site.date >= start_date,
            precios_site.date <= end_date,
            marcas_places.es_norte != "Si"
        ).group_by(
            precios_site.product
        ).all()

        averages_01 = db.session.query(
            precios_site.product,
            cast(func.avg(precios_site.prices), Numeric(8, 2)).label("Promedio"),
            cast(func.min(precios_site.prices), Numeric(8, 2)).label("Minimo"),
            cast(func.max(precios_site.prices), Numeric(8, 2)).label("Maximo")
        ).join( 
            marcas_places, cast(precios_site.place_id, Integer) == cast(marcas_places.place_id, Integer)
        ).filter(
            precios_site.date >= start_date_01,
            precios_site.date <= end_date_01,
            marcas_places.es_norte != "Si"
        ).group_by(
            precios_site.product
        ).all()
    
    result = []
    for product, average, minimum, maximum in averages:
        for product_01, average_01, minimum_01, maximum_01 in averages_01:
            if product == product_01:
                result.append({
                    'product': product,
                    'average_01' : average_01,
                    'average': average,
                    'minimum': minimum,
                    'maximum': maximum
                })
    
    return result

