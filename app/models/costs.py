from app.extensions import db
from unidecode import unidecode
from sqlalchemy import asc
from datetime import datetime, timedelta


class costos_pemex(db.Model):
    id_terminal = db.Column(db.Integer, primary_key=True)
    terminal = db.Column(db.Text)
    precio_tar = db.Column(db.Float)
    producto = db.Column(db.Text)
    date = db.Column(db.Date)

def terminales():
    unique_terminals = db.session.query(costos_pemex.id_terminal, costos_pemex.terminal).distinct().all()
    #terminal_list = [unidecode(terminal[0]) for terminal in unique_terminals]
    terminal_list = [{'id_terminal': terminal[0], 'terminal': unidecode(terminal[1])} for terminal in unique_terminals]
    return terminal_list

def get_terminal_info(terminal):
    # Get the latest date available for the selected terminal
    latest_date = db.session.query(db.func.max(costos_pemex.date)).scalar()

    # Get the information for the latest date
    latest_info = db.session.query(costos_pemex.precio_tar, costos_pemex.producto).filter(
        costos_pemex.id_terminal == terminal,
        costos_pemex.date == latest_date
    ).all()

    # Calculate the date before the latest date
    previous_date = latest_date - timedelta(days=1)

    # Get the information for the previous date
    previous_info = db.session.query(costos_pemex.precio_tar, costos_pemex.producto).filter(
        costos_pemex.id_terminal == terminal,
        costos_pemex.date == previous_date
    ).all()

    for price, product in latest_info:
        if product == 'diesel':
            hoy_diesel_price = round(price / 1000, 2)
        elif product == 'regular':
            hoy_regular_price = round(price / 1000, 2)
        elif product == 'premium':
            hoy_premium_price = round(price / 1000, 2)

    # Find ayer diesel and regular prices
    for price, product in previous_info:
        if product == 'diesel':
            ayer_diesel_price = round(price / 1000, 2)
        elif product == 'regular':
            ayer_regular_price = round(price / 1000, 2)
        elif product == 'premium':
            ayer_premium_price = round(price / 1000, 2)

    result = {
        "hoy": latest_date,
        "ayer": previous_date,
        "hoy_diesel_price": hoy_diesel_price,
        "ayer_diesel_price": ayer_diesel_price,
        "hoy_regular_price": hoy_regular_price,
        "ayer_regular_price": ayer_regular_price,
        "hoy_premium_price": hoy_premium_price,
        "ayer_premium_price":ayer_premium_price
    }

    return result

def get_terminal_data(terminal):
    today = datetime.now().date()
    past_90_days = today - timedelta(days=90)

    # Query the database to retrieve the data for the specified terminal within the past 90 days
    data = db.session.query(costos_pemex.precio_tar, costos_pemex.producto, costos_pemex.date) \
                   .filter(costos_pemex.id_terminal == terminal, costos_pemex.date >= past_90_days) \
                   .order_by(asc(costos_pemex.date)) \
                   .all()
    #print(data)
    # Prepare the response as JSON
    response = []
    for items in data:
        response.append({
            'precio_tar': round(items.precio_tar/1000,2),
            'producto': items.producto,
            'date': items.date.strftime('%Y-%m-%d')
        })
    return response
