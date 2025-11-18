from .db import db

class Elemento(db.Model):
    __tablename__ = 'elemento'

    id = db.Column(db.Integer, primary_key=True)
    sku_elemnto = db.Column(db.String(20), nullable=False)
    nmbre_elemnto = db.Column(db.String(40), nullable=False)
    dscrpcion_elemnto = db.Column(db.String(60), nullable=False)
    lote_elemnto = db.Column(db.String(60), nullable=False)
    ctgria_elemnto = db.Column(db.SmallInteger, nullable=False)
    und_elemnto = db.Column(db.SmallInteger, nullable=False)
    exstncia_elemnto = db.Column(db.Integer, nullable=False)
    prsntacion_elemnto = db.Column(db.String(80), nullable=False)
    lbrtorio_elemnto = db.Column(db.String(60), nullable=False)
    cntrolado_elemnto = db.Column(db.String(1), nullable=False)
    bdga_elemnto = db.Column(db.Integer, nullable=False)
    precio_venta_ac = db.Column(db.Numeric(10,0), nullable=False)
    precio_venta_an = db.Column(db.Numeric(10,0), nullable=False)
    costo_venta = db.Column(db.Numeric(10,0), nullable=False)
    mrgen_utldad = db.Column(db.Float, nullable=False)
    tiene_iva = db.Column(db.String(1), nullable=False)
    stock_minimo = db.Column(db.Integer, nullable=False)
    stock_maximo = db.Column(db.Integer, nullable=False)
    estdo_elmnto = db.Column(db.String(1), nullable=False)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
