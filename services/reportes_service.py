# services/reportes_service.py
from models.elemento import Elemento
from models.movimiento import Movimiento
from utils.pdf_utils import generar_pdf
from sqlalchemy import asc, desc

class ReportesService:

    @staticmethod
    def reporte_elementos():
        elementos = Elemento.query.order_by(asc(Elemento.id)).all()

        encabezados = [
            "ID", "SKU", "Nombre", "Descripción", "Stock", "Precio", "Estado"
        ]

        filas = [
            [
                e.id,
                e.sku_elemnto,
                e.nmbre_elemnto,
                e.dscrpcion_elemnto,
                e.exstncia_elemnto,
                f"${e.precio_venta_ac:,.2f}",
                "Activo" if e.estdo_elmnto == "A" else "Inactivo"
            ]
            for e in elementos
        ]

        return generar_pdf("Reporte de Elementos", encabezados, filas)

    @staticmethod
    def reporte_movimientos_por_tipo(tipo):
        movimientos = Movimiento.query.filter_by(tpo_mvnto=tipo)\
                                     .order_by(desc(Movimiento.fcha_mvnto)).all()

        encabezados = [
            "Fecha", "Tipo", "Cantidad", "Costo", "Stock Ant.", "Stock Nuevo", "Observación"
        ]

        filas = [
            [
                m.fcha_mvnto.strftime("%Y-%m-%d"),
                m.tipo.nombre if m.tipo else m.tpo_mvnto,
                m.cntdad_elemnto,
                f"${m.costo_untario:,.2f}",
                m.stock_anterior,
                m.stock_nuevo,
                m.obsrvaciones_mvnto
            ]
            for m in movimientos
        ]

        return generar_pdf(f"Movimientos Tipo {tipo}", encabezados, filas)

    @staticmethod
    def reporte_kardex(elemento_id):
        movimientos = Movimiento.query.filter_by(id_elmnto=elemento_id)\
                                     .order_by(desc(Movimiento.fcha_mvnto)).all()

        encabezados = [
            "Fecha", "Tipo", "Cant.", "Costo", "Stock Ant.", "Stock Nuevo", "Obs"
        ]

        filas = [
            [
                m.fcha_mvnto.strftime("%Y-%m-%d %H:%M"),
                m.tipo.nombre if m.tipo else m.tpo_mvnto,
                m.cntdad_elemnto,
                f"${m.costo_untario:,.2f}", 
                m.stock_anterior,
                m.stock_nuevo,
                m.obsrvaciones_mvnto,
            ]
            for m in movimientos
        ]

        return generar_pdf(f"Kardex Elemento {elemento_id}", encabezados, filas)
