from .db  import db

class TipoMov(db.Model):

    @property
    def nombre(self):
        return self.dscrpcion_tpo


    __tablename__ = "tipomov"

    tpo_mvnto = db.Column(db.SmallInteger, primary_key=True)
    dscrpcion_tpo = db.Column(db.String(40), nullable=False)
    estdo_tpo = db.Column(db.String(1), nullable=False)


