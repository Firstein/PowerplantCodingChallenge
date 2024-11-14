import logging
from flask import request, current_app
from flask_smorest import Blueprint, abort
from functools import cmp_to_key
from marshmallow import ValidationError
from models import FuelsData, Powerplant
from schemas import ProductionplanPostRequestBodySchema

log = logging.getLogger()
blp = Blueprint("productionplan", __name__, description="Calculate the production plan")


@blp.route("/productionplan", methods=['POST'])
def calculate_productionplan():
    try:
        schema = ProductionplanPostRequestBodySchema()
        productionplan_request_data = schema.load(request.get_json())
    except ValidationError as err:
        log.error(f"productionplan request body: {err}")
        abort(400, message=err.messages)

    log.debug(productionplan_request_data)

    load = productionplan_request_data["load"]
    fuels_data = FuelsData(**productionplan_request_data["fuels"])
    powerplants = [Powerplant(**powerplant) for powerplant in productionplan_request_data["powerplants"]]
    productionplan = []

    while load > 0 and len(powerplants) > 0:
        # scoring will change each time, because if the load remaining is too low
        # the pmin of a powerplan can make it now not cost efficien
        for powerplant in powerplants:
            powerplant.set_powerplant_scoring(load, fuels_data)
        powerplants = sorted(powerplants, key=cmp_to_key(lambda pp1, pp2: pp1.score - pp2.score))

        # get first powerplant, the best ranked and get the max of it
        powerplant = powerplants.pop(0)
        power = powerplant.get_max_power_to_generate(load, fuels_data)
        productionplan.append({"name": powerplant.name, "p": power})
        load -= power
    
    # Fill with not used powerplants
    for powerplant in powerplants:
        productionplan.append({"name": powerplant.name, "p": 0.0})
    
    return productionplan