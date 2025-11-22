from .db import db
from datetime import datetime
from .tipomov import TipoMov # Agregado para asegurar la disponibilidad del modelo TipoMov

class Movimiento(db.Model):
    __tablename__ = "mvmnto_invntario"

    id = db.Column(db.Integer, primary_key=True)
    id_elmnto = db.Column(db.Integer, db.ForeignKey("elemento.id"), nullable=False)

    # FK CORRECTA: Apunta a la PK en tipomov (que es tpo_mvnto)
    tpo_mvnto = db.Column(db.SmallInteger, db.ForeignKey("tipomov.tpo_mvnto"), nullable=False)

    cntdad_elemnto = db.Column(db.Integer, nullable=False)
    costo_untario = db.Column(db.Numeric(10,0), nullable=False)
    fcha_mvnto = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    id_usrio = db.Column(db.SmallInteger, nullable=False)
    estdo_mvnto = db.Column(db.String(1), nullable=False)
    obsrvaciones_mvnto = db.Column(db.String(80), nullable=False)

    stock_anterior = db.Column(db.Integer)
    stock_nuevo = db.Column(db.Integer)
    valor_total = db.Column(db.Numeric(14,2))

    reversed_from = db.Column(db.Integer, db.ForeignKey("mvmnto_invntario.id"))

    elemento = db.relationship("Elemento", backref="movimientos")

    tipo = db.relationship(
        "TipoMov",
        # Ya no especificamos 'lazy', se usa "select" por defecto.
    )