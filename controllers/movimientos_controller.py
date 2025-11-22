import traceback
from flask import Blueprint, request, jsonify
from services.movimiento_service import MovimientoService
from schemas.movimiento_schema import MovimientoSchema
from models.movimiento import Movimiento
from flask_cors import cross_origin

movimientos_bp = Blueprint("movimientos_bp", __name__)

mov_schema = MovimientoSchema()
mov_schema_many = MovimientoSchema(many=True)


@movimientos_bp.route("/", methods=["POST"], strict_slashes=False)
@cross_origin(supports_credentials=True)
def registrar():
    """
    Registrar un nuevo movimiento (Entrada o Salida)
    ---
    tags:
      - Movimientos
    parameters:
      - in: body
        name: body
        schema:
          id: MovimientoInput
          required:
            - id_elmnto
            - tpo_mvnto
            - cntdad_elemnto
          properties:
            id_elmnto:
              type: integer
              description: ID del elemento al que aplica el movimiento.
            tpo_mvnto:
              type: integer
              description: Tipo de movimiento (1-4 para entradas, 5-7 para salidas).
            cntdad_elemnto:
              type: integer
              description: Cantidad de elementos del movimiento.
            costo_untario:
              type: number
              format: float
              description: Costo unitario del movimiento (requerido para entradas).
            id_usrio:
              type: integer
              description: ID del usuario que registra el movimiento.
            obsrvaciones_mvnto:
              type: string
              description: Observaciones adicionales del movimiento.
    responses:
      201:
        description: Movimiento registrado exitosamente
        schema:
          $ref: '#/definitions/Movimiento'
      400:
        description: Error de validación o stock insuficiente
      500:
        description: Error interno del servidor
    """
    try:
        json_data = request.json
        print("\n--- INICIO DEPURACIÓN ---")
        print("Datos JSON recibidos:", json_data) 
        
        if json_data is None:
            
            error_msg = "Error: La solicitud no contiene datos JSON o el Content-Type no es application/json."
            print(error_msg)
            print("--- FIN DEPURACIÓN ---\n")
            return jsonify({"error": error_msg}), 400

        
        mov, error = MovimientoService.registrar_movimiento(json_data)

        if error:
            print("Error en Service:", error)
            print("--- FIN DEPURACIÓN ---\n")
            return jsonify({"error": error}), 400
        
    
        print("Movimiento registrado exitosamente.")
        print("--- FIN DEPURACIÓN ---\n")
        return jsonify(mov_schema.dump(mov)), 201
        
    except Exception as e:

        traceback.print_exc() 
        print(f"\nFATAL ERROR 500 CAPTURADO: {e}")
        print("--- FIN DEPURACIÓN ---\n")
        return jsonify({"error": f"Error interno del servidor al procesar el movimiento: {e}"}), 500


@movimientos_bp.route("/kardex/<int:elemento_id>", methods=["GET"])
@cross_origin()
def kardex(elemento_id):
    """
    Obtener el historial de movimientos (Kardex) para un elemento
    ---
    tags:
      - Movimientos
    parameters:
      - name: elemento_id
        in: path
        type: integer
        required: true
        description: ID del elemento para el cual obtener el Kardex.
      - name: page
        in: query
        type: integer
        default: 1
        description: Número de página para la paginación.
      - name: per_page
        in: query
        type: integer
        default: 50
        description: Cantidad de elementos por página.
    responses:
      200:
        description: Lista paginada del historial de movimientos del elemento
        schema:
          type: object
          properties:
            total:
              type: integer
              description: Número total de movimientos.
            page:
              type: integer
              description: Número de página actual.
            per_page:
              type: integer
              description: Elementos por página.
            items:
              type: array
              items:
                $ref: '#/definitions/Movimiento'
    """
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 50))
    
    q = Movimiento.query.filter_by(id_elmnto=elemento_id)\
                        .order_by(Movimiento.fcha_mvnto.desc())
                        
    pag = q.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "total": pag.total,
        "page": page,
        "per_page": per_page,
        "items": mov_schema_many.dump(pag.items)
    }), 200


@movimientos_bp.route("/search", methods=["GET"])
@cross_origin()
def search():
    """
    Buscar movimientos con filtros de tipo y rango de fechas
    ---
    tags:
      - Movimientos
    parameters:
      - name: tpo_mvnto
        in: query
        type: integer
        required: false
        description: Filtrar por ID de tipo de movimiento.
      - name: desde
        in: query
        type: string
        format: date
        required: false
        description: Fecha de inicio del rango (YYYY-MM-DD).
      - name: hasta
        in: query
        type: string
        format: date
        required: false
        description: Fecha de fin del rango (YYYY-MM-DD).
      - name: page
        in: query
        type: integer
        default: 1
        description: Número de página para la paginación.
      - name: per_page
        in: query
        type: integer
        default: 50
        description: Cantidad de elementos por página.
    responses:
      200:
        description: Lista paginada de movimientos filtrados
        schema:
          type: object
          properties:
            total:
              type: integer
              description: Número total de movimientos.
            page:
              type: integer
              description: Número de página actual.
            per_page:
              type: integer
              description: Elementos por página.
            items:
              type: array
              items:
                $ref: '#/definitions/Movimiento'
    """
    tipo = request.args.get("tpo_mvnto", type=int)
    desde = request.args.get("desde")
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
@cross_origin()
def revert(mov_id):
    """
    Revertir un movimiento existente
    ---
    tags:
      - Movimientos
    parameters:
      - name: mov_id
        in: path
        type: integer
        required: true
        description: ID del movimiento a revertir.
      - in: body
        name: body
        schema:
          type: object
          properties:
            usuario_id:
              type: integer
              description: ID del usuario que realiza la reversión.
    responses:
      201:
        description: Movimiento de reversión creado exitosamente
        schema:
          $ref: '#/definitions/Movimiento'
      400:
        description: Error al revertir (movimiento no activo, stock insuficiente, etc.)
    """
    data = request.get_json() or {}
    usuario = data.get("usuario_id", 0)

    mov, error = MovimientoService.revertir_movimiento(mov_id, usuario)
    if error:
        return jsonify({"error": error}), 400

    return mov_schema.dump(mov), 201