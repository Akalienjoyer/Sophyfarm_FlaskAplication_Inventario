from flask import Blueprint, request, jsonify
from services.elemento_service import ElementoService
from schemas.elemento_schema import ElementoSchema

elemento_bp = Blueprint("elemento_bp", __name__)
schema = ElementoSchema()
schema_many = ElementoSchema(many=True)

@elemento_bp.route("/", methods=["GET"])
def get_all():
    """
    Obtener todos los elementos
    ---
    tags:
      - Elementos
    responses:
      200:
        description: Lista de elementos
        schema:
          type: array
          items:
            $ref: '#/definitions/Elemento'
    """
    elems = ElementoService.get_all()
    return jsonify(schema_many.dump(elems)), 200

@elemento_bp.route("/<int:id>", methods=["GET"])
def get_by_id(id):
    """
    Obtener un elemento por id
    ---
    tags:
      - Elementos
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Elemento encontrado
        schema:
          $ref: '#/definitions/Elemento'
      404:
        description: No encontrado
    """
    elem = ElementoService.get_by_id(id)
    if not elem:
        return jsonify({"error": "Elemento no encontrado"}), 404
    return jsonify(schema.dump(elem)), 200

@elemento_bp.route("/", methods=["POST", "OPTIONS"])
def create():
    """
    Crear un nuevo elemento
    ---
    tags:
      - Elementos
    parameters:
      - in: body
        name: body
        schema:
          id: Elemento
          required:
            - sku_elemnto
            - nmbre_elemnto
          properties:
            sku_elemnto:
              type: string
            nmbre_elemnto:
              type: string
            exstncia_elemnto:
              type: integer
    responses:
      201:
        description: Elemento creado exitosamente
      400:
        description: Error de validación
    """
    
    if request.method == "OPTIONS":
        return {}, 200  

    data = request.json
    elem, error = ElementoService.create(data)
    if error:
        return jsonify({"error": error}), 400
    return jsonify(schema.dump(elem)), 201

@elemento_bp.route("/<int:id>", methods=["PUT"])
def update(id):
    """
    Actualizar un elemento
    ---
    tags:
      - Elementos
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          $ref: '#/definitions/ElementoInput'
    responses:
      200:
        description: Elemento actualizado
        schema:
          $ref: '#/definitions/Elemento'
      400:
        description: Error
      404:
        description: No encontrado
    """
    data = request.json
    elem, error = ElementoService.update(id, data)
    if error:
        return jsonify({"error": error}), 400
    return jsonify(schema.dump(elem)), 200

@elemento_bp.route("/<int:id>", methods=["DELETE"])
def delete(id):
    """
    Borrado lógico de un elemento
    ---
    tags:
      - Elementos
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Marcado como inactivo
      400:
        description: Error
    """
    elem, error = ElementoService.delete(id)
    if error:
        return jsonify({"error": error}), 400
    return jsonify({"mensaje": "Elemento marcado como inactivo"}), 200

@elemento_bp.route("/<int:id>/force", methods=["DELETE"])
def force_delete(id):
    """
    Borrado físico (permanente)
    ---
    tags:
      - Elementos
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Eliminado permanentemente
      400:
        description: Error
    """
    ok, error = ElementoService.force_delete(id)
    if error:
        return jsonify({"error": error}), 400
    return jsonify({"mensaje": "Elemento eliminado permanentemente"}), 200



