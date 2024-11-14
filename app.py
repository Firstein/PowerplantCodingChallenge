import logging
from flask import Flask
from flask_smorest import Api
from productionplan import blp as ProductionplanBlueprint


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s : %(message)s",
    datefmt="%m/%d/%y %I:%M:%S %p",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("test.log", "a"),
    ],
)


app = Flask(__name__)

app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Powerplant Coding Challenge REST API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["C02_ALLOWANCES"] = True
app.config['C02_EMISSON'] = 0.3 # (ton/MWh) how many ton of co2 created per 1 MWh generated


api = Api(app)

api.register_blueprint(ProductionplanBlueprint)