# models/movimiento.py
from .db import db
from datetime import datetime

class Movimiento(db.Model):
    __tablename__ = "mvmnto_invntario"

    id = db.Column(db.Integer, primary_key=True)
    id_elmnto = db.Column(db.Integer, db.ForeignKey("elemento.id"), nullable=False)
    tpo_mvnto = db.Column(db.SmallInteger, db.ForeignKey("tipomov.id"), nullable=False)
    cntdad_elemnto = db.Column(db.Integer, nullable=False)
    costo_untario = db.Column(db.Numeric(10,2), nullable=False)
    valor_total = db.Column(db.Numeric(14,2))
    fcha_mvnto = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    id_usrio = db.Column(db.SmallInteger, nullable=False)
    estdo_mvnto = db.Column(db.String(1), default="A", nullable=False)  # A=activo, R=revertido, C=anulado
    obsrvaciones_mvnto = db.Column(db.String(200))
    stock_anterior = db.Column(db.Integer)
    stock_nuevo = db.Column(db.Integer)
    reversed_from = db.Column(db.Integer, db.ForeignKey("mvmnto_invntario.id"), nullable=True)

    elemento = db.relationship("Elemento", backref="movimientos")
    tipo = db.relationship("TipoMov", backref="movimientos")
