from models.movimiento import MvmntoInvntario, Tipomov
from models.elemento import Elemento
from models.db import db
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

class MovimientoService:

    @staticmethod
    def create_movimiento(data):
        """
        data: dict con id_elmnto, tpo_mvnto, cntdad_elemnto, costo_untario, id_usrio, obsrvaciones_mvnto
        Actualiza el stock del elemento según el tipo de movimiento:
        - Si tpo_mvnto es de entrada -> suma
        - Si tpo_mvnto es de salida -> resta
        (Definir qué tpo_mvnto son entradas/ salidas por convención)
        """
        try:
            elemento = Elemento.query.get(data['id_elmnto'])
            if not elemento:
                return None, "Elemento no encontrado"

            tpo = data['tpo_mvnto']
            cantidad = int(data['cntdad_elemnto'])

            # Definición simple: tipos pares -> entrada; impares -> salida
            # Mejor: consultar Tipomov si lo deseas.
            es_entrada = str(tpo) in ('2','3','7','1')  # ejemplo según tu script
            if es_entrada:
                elemento.exstncia_elemnto = (elemento.exstncia_elemnto or 0) + cantidad
            else:
                # verificar stock
                if (elemento.exstncia_elemnto or 0) < cantidad:
                    return None, "Stock insuficiente"
                elemento.exstncia_elemnto = elemento.exstncia_elemnto - cantidad

            movimiento = MvmntoInvntario(
                id_elmnto = data['id_elmnto'],
                tpo_mvnto = data['tpo_mvnto'],
                cntdad_elemnto = cantidad,
                costo_untario = data.get('costo_untario'),
                fcha_mvnto = data.get('fcha_mvnto') or datetime.utcnow(),
                id_usrio = data.get('id_usrio'),
                obsrvaciones_mvnto = data.get('obsrvaciones_mvnto'),
                estdo_mvnto = 'A'
            )
            db.session.add(movimiento)
            db.session.add(elemento)
            db.session.commit()
            return movimiento, None
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, str(e)
