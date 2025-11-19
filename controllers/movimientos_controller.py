from flask import Blueprint, request, jsonify
from services.movimiento_service import MovimientoService
from schemas.movimiento_schema import MovimientoSchema

from models.movimiento import Movimiento

movimientos_bp = Blueprint("movimientos_bp", __name__, url_prefix="/api/movimientos")

mov_schema = MovimientoSchema()
mov_schema_many = MovimientoSchema(many=True)

@movimientos_bp.route("/", methods=["POST"])
def registrar():
    """
    Registrar movimiento de inventario
    ---
    tags:
      - Movimientos
    parameters:
      - name: body
        in: body
        required: true
        schema:
          $ref: '#/definitions/MovimientoInput'
    responses:
      201:
        description: Movimiento creado
        schema:
          $ref: '#/definitions/Movimiento'
      400:
        description: Error de negocio o validación
    """
    json_data = request.get_json()
    errors = mov_schema.validate(json_data)
    if errors:
        return jsonify(errors), 400

    mov, error = MovimientoService.registrar_movimiento(json_data)
    if error:
        return jsonify({"error": error}), 400

    return mov_schema.dump(mov), 201

@movimientos_bp.route("/kardex/<int:elemento_id>", methods=["GET"])
def kardex(elemento_id):
    """
    Kardex por elemento (paginado)
    ---
    tags:
      - Movimientos
    parameters:
      - name: elemento_id
        in: path
        type: integer
        required: true
      - name: page
        in: query
        type: integer
      - name: per_page
        in: query
        type: integer
    responses:
      200:
        description: Resultados paginados de movimientos del elemento
        schema:
          type: object
    """
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 50))
    q = Movimiento.query.filter_by(id_elmnto=elemento_id).order_by(Movimiento.fcha_mvnto.desc())
    pag = q.paginate(page=page, per_page=per_page, error_out=False)
    items = pag.items
    return jsonify({
        "total": pag.total,
        "page": page,
        "per_page": per_page,
        "items": mov_schema_many.dump(items)
    }), 200

@movimientos_bp.route("/search", methods=["GET"])
def search():
    """
    Buscar movimientos por filtros (tipo, fechas)
    ---
    tags:
      - Movimientos
    parameters:
      - name: tpo_mvnto
        in: query
        type: integer
      - name: desde
        in: query
        type: string
        description: fecha desde (YYYY-MM-DD)
      - name: hasta
        in: query
        type: string
        description: fecha hasta (YYYY-MM-DD)
      - name: page
        in: query
        type: integer
      - name: per_page
        in: query
        type: integer
    responses:
      200:
        description: Resultados paginados
    """
    tipo = request.args.get("tpo_mvnto", type=int)
    desde = request.args.get("desde")  # 'YYYY-MM-DD'
    hasta = request.args.get("hasta")
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 50))

    q = Movimiento.query
    if tipo:
        q = q.filter_by(tpo_mvnto=tipo)
    if desde:
        q = q.filter(Movimiento.fcha_mvnto >= desde)
    if hasta:
        q = q.filter(Movimiento.fcha_mvnto <= hasta)

    q = q.order_by(Movimiento.fcha_mvnto.desc())
    pag = q.paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        "total": pag.total,
        "page": page,
        "per_page": per_page,
        "items": mov_schema_many.dump(pag.items)
    }), 200

@movimientos_bp.route("/<int:mov_id>/revert", methods=["POST"])
def revert(mov_id):
    """
    Revertir movimiento (crea movimiento inverso)
    ---
    tags:
      - Movimientos
    parameters:
      - name: mov_id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        schema:
          properties:
            usuario_id:
              type: integer
    responses:
      201:
        description: Movimiento de reversión creado
        schema:
          $ref: '#/definitions/Movimiento'
      400:
        description: Error
    """
    data = request.get_json() or {}
    usuario = data.get("usuario_id", 0)
    mov, error = MovimientoService.revertir_movimiento(mov_id, usuario)
    if error:
        return jsonify({"error": error}), 400
    return mov_schema.dump(mov), 201
