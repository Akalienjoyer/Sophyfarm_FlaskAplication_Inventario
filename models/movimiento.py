from .db import db
from datetime import datetime

class Tipomov(db.Model):
    __tablename__ = 'tipomov'

    tpo_mvnto = db.Column(db.SmallInteger, primary_key=True)
    dscrpcion_tpo = db.Column(db.String(40), nullable=False)
    estdo_tpo = db.Column(db.String(1), nullable=False)

class MvmntoInvntario(db.Model):
    __tablename__ = 'mvmnto_invntario'

    id = db.Column(db.SmallInteger, primary_key=True)
    id_elmnto = db.Column(db.Integer, db.ForeignKey('elemento.id'), nullable=False)
    tpo_mvnto = db.Column(db.SmallInteger, db.ForeignKey('tipomov.tpo_mvnto'), nullable=False)
    cntdad_elemnto = db.Column(db.Integer, nullable=False)
    costo_untario = db.Column(db.Numeric(10,0), nullable=False)
    fcha_mvnto = db.Column(db.DateTime, nullable=False)
    id_usrio = db.Column(db.SmallInteger, nullable=False)
    estdo_mvnto = db.Column(db.String(1), nullable=False)
    obsrvaciones_mvnto = db.Column(db.String(40), nullable=False)

    elemento = db.relationship('Elemento')
    tipo = db.relationship('Tipomov')
