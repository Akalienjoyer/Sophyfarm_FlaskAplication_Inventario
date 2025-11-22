# services/movimiento_service.py
from models.movimiento import Movimiento
from models.elemento import Elemento
from models.tipomov import TipoMov
from models.db import db
from sqlalchemy import select
from decimal import Decimal, InvalidOperation
import traceback 

ENTRADAS = {1,2,3,4}
SALIDAS = {5,6,7}

def _to_decimal(value):
    try:
        return Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        return Decimal("0.00")

class MovimientoService:

    @staticmethod
    def registrar_movimiento(data):
        """
        data: dict con id_elmnto, tpo_mvnto, cntdad_elemnto, costo_untario, id_usrio, obsrvaciones_mvnto
        """
        
        try:
            elemento_id = int(data.get("id_elmnto"))
            tipo = int(data.get("tpo_mvnto"))
            cantidad = int(data.get("cntdad_elemnto"))
            
            costo_unit = _to_decimal(data.get("costo_untario"))
            
            usuario_id = int(data.get("id_usrio", 0))

        except (ValueError, TypeError) as e:
            return None, f"Error de formato de datos: La ID, Cantidad, Tipo de movimiento o Costo deben ser números válidos. Detalle: {e}"

        if cantidad <= 0:
            return None, "La cantidad debe ser mayor a 0"

        try:
            with db.session.begin():

                stmt = select(Elemento).where(Elemento.id == elemento_id).with_for_update()
                row = db.session.execute(stmt).scalars().first()
                elemento = row

                if not elemento:
                    return None, "Elemento no encontrado"

                if elemento.estdo_elmnto == 'I':
                    return None, "Elemento inactivo; imposible realizar movimiento"

                stock_anterior = elemento.exstncia_elemnto or 0


                costo_actual = _to_decimal(elemento.costo_venta or 0)

                valor_total = (costo_unit * Decimal(cantidad)).quantize(Decimal("0.01"))

                if tipo in ENTRADAS:
                    nueva_existencia = stock_anterior + cantidad

                    if stock_anterior <= 0:
                        costo_promedio = costo_unit
                    else:
                        costo_promedio = ((costo_actual * Decimal(stock_anterior)) + (costo_unit * Decimal(cantidad))) / Decimal(nueva_existencia)

                    elemento.exstncia_elemnto = nueva_existencia
                    elemento.costo_venta = costo_promedio.quantize(Decimal("0.01"))

                elif tipo in SALIDAS:
                    if stock_anterior < cantidad:
                        return None, "Stock insuficiente para realizar la salida"
                    nueva_existencia = stock_anterior - cantidad
                    elemento.exstncia_elemnto = nueva_existencia

                else:
                    return None, "Tipo de movimiento inválido"

                mov = Movimiento(
                    id_elmnto = elemento_id, 
                    tpo_mvnto = tipo,       
                    cntdad_elemnto = cantidad,
                    costo_untario = costo_unit,
                    valor_total = valor_total,
                    id_usrio = usuario_id,
                    obsrvaciones_mvnto = data.get("obsrvaciones_mvnto", ""),
                    stock_anterior = stock_anterior,
                    stock_nuevo = nueva_existencia,
                    estdo_mvnto = 'A'
                )

                db.session.add(mov)

                return mov, None

        except Exception as e:

            traceback.print_exc()
            db.session.rollback()
            return None, f"Error de procesamiento en DB: {e}"

    @staticmethod
    def revertir_movimiento(mov_id, usuario_id):
        """
        Revertir un movimiento existente:
        - Verifica que el movimiento exista y esté activo.
        - Crea un movimiento inverso (opuesto) que deshace el efecto en stock.
        - Marca el movimiento original como 'R' (revertido) y relaciona reversed_from.
        """
        try:
            with db.session.begin():
                mov = db.session.get(Movimiento, mov_id)
                if not mov:
                    return None, "Movimiento no encontrado"
                if mov.estdo_mvnto != 'A':
                    return None, "Movimiento no está activo y no puede revertirse"

                # bloquear elemento
                stmt = select(Elemento).where(Elemento.id == mov.id_elmnto).with_for_update()
                elemento = db.session.execute(stmt).scalars().first()
                if not elemento:
                    return None, "Elemento no encontrado"


                original_tipo = mov.tpo_mvnto
                cantidad = mov.cntdad_elemnto
                costo_unit = _to_decimal(mov.costo_untario)

                if original_tipo in ENTRADAS:
           
                    if elemento.exstncia_elemnto < cantidad:
                        return None, "No es posible revertir: stock actual menor que la cantidad a quitar"
                    nuevo_stock = elemento.exstncia_elemnto - cantidad
                elif original_tipo in SALIDAS:
         
                    nuevo_stock = elemento.exstncia_elemnto + cantidad
                else:
                    return None, "Tipo de movimiento no válido"

                stock_anterior = elemento.exstncia_elemnto
                elemento.exstncia_elemnto = nuevo_stock

                valor_total = (costo_unit * Decimal(cantidad)).quantize(Decimal("0.01"))

                mov_inverso = Movimiento(
                    id_elmnto = mov.id_elmnto,
                    tpo_mvnto = (1 if original_tipo in SALIDAS else 5),
                    cntdad_elemnto = cantidad,
                    costo_untario = costo_unit,
                    valor_total = valor_total,
                    id_usrio = usuario_id,
                    obsrvaciones_mvnto = f"Reversión de movimiento {mov.id}",
                    stock_anterior = stock_anterior,
                    stock_nuevo = nuevo_stock,
                    estdo_mvnto = 'A',
                    reversed_from = mov.id
                )

                db.session.add(mov_inverso)

                mov.estdo_mvnto = 'R'

                return mov_inverso, None

        except Exception as e:
            db.session.rollback()
            return None, str(e)