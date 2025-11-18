from flask import Blueprint, request, jsonify
from services.movimiento_service import MovimientoService
from schemas.movimiento_schema import MovimientoSchema

movimientos_bp = Blueprint('movimientos_bp', __name__)
schema = MovimientoSchema()

@movimientos_bp.route('/', methods=['POST'])
def create_movimiento():
    data = request.json
    errors = schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400
    mov, err = MovimientoService.create_movimiento(data)
    if err:
        return jsonify({"error": err}), 400
    return jsonify({"id": mov.id, "id_elmnto": mov.id_elmnto}), 201

@movimientos_bp.route('/elemento/<int:elemento_id>', methods=['GET'])
def list_movs_by_elemento(elemento_id):
    from models.movimiento import MvmntoInvntario
    # Directly query for speed
    movs = MvmntoInvntario.query.filter_by(id_elmnto=elemento_id).order_by(MvmntoInvntario.fcha_mvnto.desc()).all()
    return jsonify([{
        "id": m.id,
        "tpo_mvnto": m.tpo_mvnto,
        "cntdad_elemnto": m.cntdad_elemnto,
        "fcha_mvnto": m.fcha_mvnto.isoformat(),
        "obsrvaciones_mvnto": m.obsrvaciones_mvnto
    } for m in movs])
