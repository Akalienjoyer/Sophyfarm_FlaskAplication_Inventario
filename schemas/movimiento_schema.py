from marshmallow import Schema, fields, validate

class MovimientoSchema(Schema):
    id = fields.Int(dump_only=True)
    id_elmnto = fields.Int(required=True)
    tpo_mvnto = fields.Int(required=True, validate=validate.OneOf([1,2,3,4,5,6,7]))
    cntdad_elemnto = fields.Int(required=True)
    costo_untario = fields.Decimal(required=True, as_string=True)
    valor_total = fields.Decimal(as_string=True, dump_only=True)
    fcha_mvnto = fields.DateTime(dump_only=True)
    id_usrio = fields.Int(required=True)
    estdo_mvnto = fields.Str(dump_only=True)
    obsrvaciones_mvnto = fields.Str()
    stock_anterior = fields.Int(dump_only=True)
    stock_nuevo = fields.Int(dump_only=True)
    reversed_from = fields.Int(dump_only=True)
    tipo_nombre = fields.Method("get_tipo_nombre")
    elemento_nombre = fields.Method("get_elemento_nombre")

    def get_elemento_nombre(self, obj):
        return obj.elemento.nmbre_elemnto if obj.elemento else None


    def get_tipo_nombre(self, obj):
        return obj.tipo.nombre if obj.tipo else None
