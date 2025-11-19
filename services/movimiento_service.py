# services/movimiento_service.py
from models.movimiento import Movimiento
from models.elemento import Elemento
from models.tipomov import TipoMov
from models.db import db
from sqlalchemy import select
from decimal import Decimal, InvalidOperation

# Define qué tipos son entradas y cuáles salidas
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

        # validaciones básicas
        if data.get("cntdad_elemnto", 0) <= 0:
            return None, "La cantidad debe ser mayor a 0"

        # Abrimos transacción explícita
        try:
            with db.session.begin():
                # 1) bloquear fila del elemento para este ID
                stmt = select(Elemento).where(Elemento.id == data["id_elmnto"]).with_for_update()
                row = db.session.execute(stmt).scalars().first()
                elemento = row

                if not elemento:
                    return None, "Elemento no encontrado"

                if elemento.estdo_elmnto == 'I':
                    return None, "Elemento inactivo; imposible realizar movimiento"

                tipo = data["tpo_mvnto"]
                cantidad = int(data["cntdad_elemnto"])
                costo_unit = _to_decimal(data["costo_untario"])

                stock_anterior = elemento.exstncia_elemnto or 0

                # Lógica de costo promedio ponderado (para entradas)
                # asumimos que elemento.costo_venta es el costo promedio actual
                costo_actual = _to_decimal(elemento.costo_venta or 0)

                valor_total = (costo_unit * Decimal(cantidad)).quantize(Decimal("0.01"))

                # ENTRADAS: actualizamos existencia y recalculamos costo promedio ponderado
                if tipo in ENTRADAS:
                    nueva_existencia = stock_anterior + cantidad

                    # Si no hay stock previo, el costo promedio es el costo_unit
                    if stock_anterior <= 0:
                        costo_promedio = costo_unit
                    else:
                        # promedio ponderado: (costo_actual*stock_anterior + costo_unit*cantidad) / nueva_existencia
                        costo_promedio = ((costo_actual * Decimal(stock_anterior)) + (costo_unit * Decimal(cantidad))) / Decimal(nueva_existencia)

                    elemento.exstncia_elemnto = nueva_existencia
                    elemento.costo_venta = costo_promedio.quantize(Decimal("0.01"))

                # SALIDAS: verificamos stock y descontamos; el costo por salida puede usar costo_promedio actual
                elif tipo in SALIDAS:
                    if stock_anterior < cantidad:
                        return None, "Stock insuficiente para realizar la salida"
                    nueva_existencia = stock_anterior - cantidad
                    elemento.exstncia_elemnto = nueva_existencia
                    # no cambiamos costo_venta en salidas en esquema de promedio, costo_venta se mantiene
                else:
                    return None, "Tipo de movimiento inválido"

                # crear registro de movimiento con stock antes y después
                mov = Movimiento(
                    id_elmnto = data["id_elmnto"],
                    tpo_mvnto = tipo,
                    cntdad_elemnto = cantidad,
                    costo_untario = costo_unit,
                    valor_total = valor_total,
                    id_usrio = data.get("id_usrio", 0),
                    obsrvaciones_mvnto = data.get("obsrvaciones_mvnto", ""),
                    stock_anterior = stock_anterior,
                    stock_nuevo = nueva_existencia,
                    estdo_mvnto = 'A'
                )

                db.session.add(mov)
                # elemento ya está en sesión por with_for_update
                # commit al salir del with db.session.begin()

                return mov, None

        except Exception as e:
            db.session.rollback()
            return None, str(e)

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

                # inverso: si original fue entrada -> hacemos salida; si fue salida -> entrada
                original_tipo = mov.tpo_mvnto
                cantidad = mov.cntdad_elemnto
                costo_unit = _to_decimal(mov.costo_untario)

                if original_tipo in ENTRADAS:
                    # revertir entrada -> restar stock
                    if elemento.exstncia_elemnto < cantidad:
                        return None, "No es posible revertir: stock actual menor que la cantidad a quitar"
                    nuevo_stock = elemento.exstncia_elemnto - cantidad
                elif original_tipo in SALIDAS:
                    # revertir salida -> sumar stock
                    nuevo_stock = elemento.exstncia_elemnto + cantidad
                else:
                    return None, "Tipo de movimiento no válido"

                stock_anterior = elemento.exstncia_elemnto
                elemento.exstncia_elemnto = nuevo_stock

                valor_total = (costo_unit * Decimal(cantidad)).quantize(Decimal("0.01"))

                # crear movimiento inverso con una referencia
                mov_inverso = Movimiento(
                    id_elmnto = mov.id_elmnto,
                    tpo_mvnto = (1 if original_tipo in SALIDAS else 5),  # map: salida->entrada(tipo 1), entrada->salida(tipo 5) (ajusta según tu mapeo)
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

                # marcar movimiento original como revertido
                mov.estdo_mvnto = 'R'

                return mov_inverso, None

        except Exception as e:
            db.session.rollback()
            return None, str(e)
