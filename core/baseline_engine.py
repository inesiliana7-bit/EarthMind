from core.utils import encode, clamp

from core.encoders import *

class BaselineEngine:

    def __init__(self, country):

        self.country = country

    def build(self):

        return {

            "gdp": self.gdp(),

            "inflation": self.inflation(),

            "employment": self.employment(),

            "investment": self.investment(),

            "air": self.air(),

            "water": self.water(),

            "carbon": self.carbon(),

            "forest": self.forest(),

            "health": self.health(),

            "education": self.education(),

            "poverty": self.poverty(),

            "life": self.life(),

            "roads": self.roads(),

            "electricity": self.electricity(),

            "internet": self.internet(),

            "housing": self.housing()

        }

    def gdp(self):

        score = (

            encode(self.country["Development_Level"], DEVELOPMENT_SCORE) * 0.22 +

            encode(self.country["Economy"], ECONOMY_SCORE) * 0.20 +

            encode(self.country["Technology"], TECHNOLOGY_SCORE) * 0.12 +

            encode(self.country["Infrastructure"], INFRASTRUCTURE_SCORE) * 0.12 +

            encode(self.country["Income_Level"], INCOME_SCORE) * 0.12 +

            encode(self.country["Digitalization"], DIGITAL_SCORE) * 0.10 +

            encode(self.country["Government"], GOVERNMENT_SCORE) * 0.07 +

            encode(self.country["Political_Stability"], STABILITY_SCORE) * 0.05

        )

        return round(clamp(score),1)


    def employment(self):

        score = (

            encode(self.country["Education"], EDUCATION_SCORE)*0.30 +

            encode(self.country["Economy"], ECONOMY_SCORE)*0.25 +

            encode(self.country["Technology"], TECHNOLOGY_SCORE)*0.20 +

            encode(self.country["Infrastructure"], INFRASTRUCTURE_SCORE)*0.15 +

            encode(self.country["Political_Stability"], STABILITY_SCORE)*0.10

        )

        return round(clamp(score),1)

    def investment(self):

        score=(

            encode(self.country["Government"],GOVERNMENT_SCORE)*0.25 +

            encode(self.country["Political_Stability"],STABILITY_SCORE)*0.25 +

            encode(self.country["Infrastructure"],INFRASTRUCTURE_SCORE)*0.20 +

            encode(self.country["Technology"],TECHNOLOGY_SCORE)*0.15 +

            encode(self.country["Natural_Resources"],RESOURCE_SCORE)*0.15

        )

        return round(clamp(score),1)

    def inflation(self):

        score = (

            100 -

            (

                self.gdp()*0.60 +

                self.investment()*0.20 +

                self.employment()*0.20

            )

        )

        return round(clamp(score),1)

    def air(self):

        score = (

            (100 - encode(self.country["Carbon_Emissions"], CARBON_SCORE))*0.40 +

            encode(self.country["Natural_Resources"], RESOURCE_SCORE)*0.20 +

            encode(self.country["Energy"], ENERGY_SCORE)*0.20 +

            encode(self.country["Climate"], CLIMATE_SCORE)*0.20

        )

        return round(clamp(score),1)

    def water(self):

        score = (

            encode(self.country["Water"], WATER_SCORE)*0.50 +

            encode(self.country["Climate"], CLIMATE_SCORE)*0.20 +

            encode(self.country["Infrastructure"], INFRASTRUCTURE_SCORE)*0.15 +

            encode(self.country["Government"], GOVERNMENT_SCORE)*0.15

        )

        return round(clamp(score),1)

    def carbon(self):

        score = (

            encode(self.country["Carbon_Emissions"], CARBON_SCORE)*0.70 +

            (100-encode(self.country["Energy"], ENERGY_SCORE))*0.30

        )

        return round(clamp(score),1)

    def forest(self):

        score = (

            encode(self.country["Natural_Resources"], RESOURCE_SCORE)*0.35 +

            encode(self.country["Climate"], CLIMATE_SCORE)*0.25 +

            encode(self.country["Government"], GOVERNMENT_SCORE)*0.20 +

            encode(self.country["Water"], WATER_SCORE)*0.20

        )

        return round(clamp(score),1)

    def health(self):

        score = (

            encode(self.country["Healthcare"], HEALTH_SCORE)*0.40 +

            encode(self.country["Income_Level"], INCOME_SCORE)*0.20 +

            encode(self.country["Infrastructure"], INFRASTRUCTURE_SCORE)*0.20 +

            encode(self.country["Education"], EDUCATION_SCORE)*0.20

        )

        return round(clamp(score),1)

    def education(self):

        score = (

            encode(self.country["Education"], EDUCATION_SCORE)*0.45 +

            encode(self.country["Technology"], TECHNOLOGY_SCORE)*0.20 +

            encode(self.country["Digitalization"], DIGITAL_SCORE)*0.15 +

            encode(self.country["Income_Level"], INCOME_SCORE)*0.20

        )

        return round(clamp(score),1)

    def poverty(self):

        score = (

            100 -

            (

                self.gdp()*0.40 +

                self.employment()*0.30 +

                self.education()*0.15 +

                self.health()*0.15

            )

        )

        return round(clamp(score),1)

    def life(self):

        score = (

            self.health()*0.25 +

            self.education()*0.20 +

            self.gdp()*0.20 +

            self.air()*0.10 +

            self.water()*0.10 +

            self.housing()*0.15

        )

        return round(clamp(score),1)

    def roads(self):

        score = (

            encode(self.country["Infrastructure"], INFRASTRUCTURE_SCORE)*0.60 +

            encode(self.country["Government"], GOVERNMENT_SCORE)*0.20 +

            encode(self.country["Income_Level"], INCOME_SCORE)*0.20

        )

        return round(clamp(score),1)

    def electricity(self):

        score = (

            encode(self.country["Energy"], ENERGY_SCORE)*0.50 +

            encode(self.country["Infrastructure"], INFRASTRUCTURE_SCORE)*0.30 +

            encode(self.country["Government"], GOVERNMENT_SCORE)*0.20

        )

        return round(clamp(score),1)

    def internet(self):

        score = (

            encode(self.country["Digitalization"], DIGITAL_SCORE)*0.50 +

            encode(self.country["Technology"], TECHNOLOGY_SCORE)*0.30 +

            encode(self.country["Infrastructure"], INFRASTRUCTURE_SCORE)*0.20

        )

        return round(clamp(score),1)

    def housing(self):

        score = (

            encode(self.country["Infrastructure"], INFRASTRUCTURE_SCORE)*0.35 +

            encode(self.country["Income_Level"], INCOME_SCORE)*0.25 +

            encode(self.country["Government"], GOVERNMENT_SCORE)*0.20 +

            encode(self.country["Urbanization"], URBANIZATION_SCORE)*0.20

        )

        return round(clamp(score),1)

    