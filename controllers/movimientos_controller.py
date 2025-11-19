# controllers/movimientos_controller.py
from flask import Blueprint, request, jsonify
from services.movimiento_service import MovimientoService
from schemas.movimiento_schema import MovimientoSchema

from models.movimiento import Movimiento

movimientos_bp = Blueprint("movimientos_bp", __name__, url_prefix="/api/movimientos")

mov_schema = MovimientoSchema()
mov_schema_many = MovimientoSchema(many=True)

@movimientos_bp.route("/", methods=["POST"])
def registrar():
    json_data = request.get_json()
    errors = mov_schema.validate(json_data)
    if errors:
        return jsonify(errors), 400

    mov, error = MovimientoService.registrar_movimiento(json_data)
    if error:
        return jsonify({"error": error}), 400

    return mov_schema.dump(mov), 201

# kardex por elemento (paginado)
@movimientos_bp.route("/kardex/<int:elemento_id>", methods=["GET"])
def kardex(elemento_id):
    # params: page, per_page
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

# historial con filtro por tipo y rango de fechas
@movimientos_bp.route("/search", methods=["GET"])
def search():
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

# revertir movimiento
@movimientos_bp.route("/<int:mov_id>/revert", methods=["POST"])
def revert(mov_id):
    data = request.get_json() or {}
    usuario = data.get("usuario_id", 0)
    mov, error = MovimientoService.revertir_movimiento(mov_id, usuario)
    if error:
        return jsonify({"error": error}), 400
    return mov_schema.dump(mov), 201
