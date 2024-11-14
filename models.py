from flask import current_app
from enum import Enum
import logging

log = logging.getLogger()

class PowerplantTypes(Enum):
    GASFIRED = "gasfired"
    TURBOJET = "turbojet"
    WINDTURBINE = "windturbine"


class FuelsData:

    def __init__(self, gas, kerosine, co2, wind):
        self.gas = gas
        self.kerosine = kerosine
        self.co2 = co2
        self.wind = wind


class Powerplant:

    def __init__(self, name, type, efficiency, pmin, pmax):
        self.name = name
        self.type = type
        self.efficiency = efficiency
        self.pmin = pmin
        self.pmax = pmax
        self.score = None
    
    def get_max_power_to_generate(self, load, fuels_data: FuelsData, round_decimal_digits = 1):
        if self.type == PowerplantTypes.WINDTURBINE.value:
            max_power_to_generate = fuels_data.wind/100 * max(min(self.pmax, load), self.pmin)
        else:
            max_power_to_generate = max(min(self.pmax, load), self.pmin)
        # round to round_decimal_digits
        return round(max_power_to_generate, round_decimal_digits)
        
    def set_powerplant_scoring(self, load, fuels_data: FuelsData):
        """ For a certain 'load', the score is decided based on the hypothesis
        the powerplant can reach the 'load' value witout care for pmax.
        It reflects the price to reach the 'load' value, but if the 'load'
        is below 'pmin' then instead it reflect the price to reach get 'pmin'
        """
        if self.type == PowerplantTypes.WINDTURBINE.value:
            self.score = 0
        elif self.type == PowerplantTypes.TURBOJET.value:
            self.score = (
                fuels_data.kerosine/self.efficiency
                * max(load, self.pmin)
            )
        elif self.type == PowerplantTypes.GASFIRED.value:
            self.score = (
                fuels_data.gas/self.efficiency
                * max(load, self.pmin)
            )
            if current_app.config['C02_ALLOWANCES']: 
                self.score += max(load, self.pmin) * current_app.config['C02_EMISSON'] * fuels_data.co2
        else:
            raise ValueError(
                f"type {self.type} is not recognized \n"
                + f"Type allow {[type.value for type in PowerplantTypes]}"
            )