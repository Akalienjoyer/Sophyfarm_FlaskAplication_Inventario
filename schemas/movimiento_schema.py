from marshmallow import Schema, fields

class MovimientoSchema(Schema):
    id = fields.Int(dump_only=True)
    id_elmnto = fields.Int(required=True)
    tpo_mvnto = fields.Int(required=True)
    cntdad_elemnto = fields.Int(required=True)
    costo_untario = fields.Decimal(as_string=True)
    fcha_mvnto = fields.DateTime()
    id_usrio = fields.Int()
    obsrvaciones_mvnto = fields.Str()
