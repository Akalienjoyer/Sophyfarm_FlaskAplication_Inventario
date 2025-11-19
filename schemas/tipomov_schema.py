from marshmallow import Schema, fields

class TipoMovSchema(Schema):
    id = fields.Int(dump_only=True)
    dscrpcion_tpo = fields.Str(required=True)
    estdo_tpo = fields.Str(required=True)
