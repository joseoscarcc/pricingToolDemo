from app.extensions import db


class marcas_places(db.Model):
    place_id = db.Column(db.Integer, primary_key=True)
    cre_id = db.Column(db.Text)
    brand = db.Column(db.Text)
    cp = db.Column(db.Text)
    x = db.Column(db.Float)
    y = db.Column(db.Float)
    es_norte = db.Column(db.Text)
    municipio = db.Column(db.Text)
    estado = db.Column(db.Text)
    terminal = db.Column(db.Text)
    brand_2 = db.Column(db.Text)

def get_unique_estados():
    unique_estados = db.session.query(marcas_places.estado).distinct().all()
    estados = [estado[0] for estado in unique_estados]
    return estados