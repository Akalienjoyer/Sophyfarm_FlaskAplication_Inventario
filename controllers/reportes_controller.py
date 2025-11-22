from flask import Blueprint, send_file, request
from services.reportes_service import ReportesService

reportes_bp = Blueprint("reportes_bp", __name__, url_prefix="/api/reportes")


@reportes_bp.route("/elementos", methods=["GET"])
def elementos_pdf():
    """
    Generar un reporte PDF de todos los elementos
    ---
    tags:
      - Reportes
    responses:
      200:
        description: Archivo PDF con el reporte de elementos.
        content:
          application/pdf:
            schema:
              type: string
              format: binary
    """
    pdf_buffer = ReportesService.reporte_elementos()
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name="reporte_elementos.pdf",
        mimetype="application/pdf"
    )


@reportes_bp.route("/movimientos", methods=["GET"])
def movimientos_pdf():
    """
    Generar un reporte PDF de movimientos filtrados por tipo
    ---
    tags:
      - Reportes
    parameters:
      - name: tpo_mvnto
        in: query
        type: integer
        required: true
        description: ID del tipo de movimiento a reportar (Ej. 1 para Compra).
    responses:
      200:
        description: Archivo PDF con el reporte de movimientos por tipo.
        content:
          application/pdf:
            schema:
              type: string
              format: binary
    """
    tipo = request.args.get("tpo_mvnto", type=int)
    pdf_buffer = ReportesService.reporte_movimientos_por_tipo(tipo)
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f"reporte_movimientos_tipo_{tipo}.pdf",
        mimetype="application/pdf"
    )


@reportes_bp.route("/kardex/<int:elemento_id>", methods=["GET"])
def kardex_pdf(elemento_id):
    """
    Generar un reporte PDF de Kardex para un elemento específico
    ---
    tags:
      - Reportes
    parameters:
      - name: elemento_id
        in: path
        type: integer
        required: true
        description: ID del elemento para el cual generar el Kardex.
    responses:
      200:
        description: Archivo PDF con el reporte Kardex del elemento.
        content:
          application/pdf:
            schema:
              type: string
              format: binary
    """
    pdf_buffer = ReportesService.reporte_kardex(elemento_id)
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f"kardex_elemento_{elemento_id}.pdf",
        mimetype="application/pdf"
    )