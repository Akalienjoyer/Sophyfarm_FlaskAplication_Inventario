from flask import Blueprint, request, jsonify
from services.elemento_service import ElementoService
from schemas.elemento_schema import ElementoSchema

elemento_bp = Blueprint("elemento_bp", __name__)
schema = ElementoSchema()
schema_many = ElementoSchema(many=True)

@elemento_bp.route("/", methods=["GET"])
def get_all():
    elems = ElementoService.get_all()
    return jsonify(schema_many.dump(elems)), 200

@elemento_bp.route("/<int:id>", methods=["GET"])
def get_by_id(id):
    elem = ElementoService.get_by_id(id)
    if not elem:
        return jsonify({"error": "Elemento no encontrado"}), 404
    return jsonify(schema.dump(elem)), 200

@elemento_bp.route("/", methods=["POST"])
def create():
    data = request.json
    elem, error = ElementoService.create(data)
    if error:
        return jsonify({"error": error}), 400
    return jsonify(schema.dump(elem)), 201

@elemento_bp.route("/<int:id>", methods=["PUT"])
def update(id):
    data = request.json
    elem, error = ElementoService.update(id, data)
    if error:
        return jsonify({"error": error}), 400
    return jsonify(schema.dump(elem)), 200

@elemento_bp.route("/<int:id>", methods=["DELETE"])
def delete(id):
    elem, error = ElementoService.delete(id)
    if error:
        return jsonify({"error": error}), 400
    return jsonify({"mensaje": "Elemento marcado como inactivo"}), 200
