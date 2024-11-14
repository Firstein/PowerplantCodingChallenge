from marshmallow import Schema, fields, validate
from models import PowerplantTypes


class FuelsDataSchema(Schema):
    gas = fields.Float(required=True, data_key="gas(euro/MWh)")
    kerosine = fields.Float(required=True, data_key="kerosine(euro/MWh)")
    co2 = fields.Float(required=True, data_key="co2(euro/ton)")
    wind = fields.Float(required=True, data_key="wind(%)")


class PowerplantSchema(Schema):
    name = fields.Str(required=True)
    type = fields.Str(required=True, validate=validate.OneOf([type.value for type in PowerplantTypes]))
    efficiency = fields.Float(required=True)
    pmin = fields.Float(required=True)
    pmax = fields.Float(required=True)


class ProductionplanPostRequestBodySchema(Schema):
    load = fields.Float(required=True)
    fuels = fields.Nested(FuelsDataSchema)
    powerplants = fields.List(fields.Nested(PowerplantSchema))