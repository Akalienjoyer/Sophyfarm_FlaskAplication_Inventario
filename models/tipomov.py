from .db  import db

class TipoMov(db.Model):
    __tablename__ = "tipomov"

    id = db.Column(db.SmallInteger, primary_key=True)
    dscrpcion_tpo = db.Column(db.String(40), nullable=False)
    estdo_tpo = db.Column(db.String(1), nullable=False)
