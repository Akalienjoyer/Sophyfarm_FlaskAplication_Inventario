from models.db import db
from models.elemento import Elemento

class ElementoService:

    @staticmethod
    def get_all():
        return Elemento.query.all()

    @staticmethod
    def get_by_id(id):
        return Elemento.query.get(id)

    @staticmethod
    def create(data):
        try:
            nuevo = Elemento(**data)
            db.session.add(nuevo)
            db.session.commit()
            return nuevo, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def update(id, data):
        elem = Elemento.query.get(id)
        if not elem:
            return None, "Elemento no encontrado"

        try:
            for key, value in data.items():
                setattr(elem, key, value)
            db.session.commit()
            return elem, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def delete(id):
        elem = Elemento.query.get(id)
        if not elem:
            return None, "Elemento no encontrado"

        try:
            elem.estdo_elmnto = "I"  # borrado lógico
            db.session.commit()
            return elem, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)
        

    @staticmethod
    def force_delete(id):
        elem = Elemento.query.get(id)
        if not elem:
            return None, "Elemento no encontrado"

        try:
            db.session.delete(elem)  # Elimina físicamente
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)

