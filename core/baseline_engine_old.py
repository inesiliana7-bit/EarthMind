from core.utils import score



class BaselineEngine:

    def __init__(self, country):

        self.country = country

    def build(self):

        baseline = {

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

        return baseline

    def gdp(self):

        value = (

            score(self.country["Budget_Level"])*0.25

            +

            score(self.country["Development_Level"])*0.20

            +

            score(self.country["Technology"])*0.15

            +

            score(self.country["Infrastructure"])*0.15

            +

            score(self.country["Income_Level"])*0.15

            +

            score(self.country["Digitalization"])*0.10

        )

        return round(value,1)

    def employment(self):

        value = (

            score(self.country["Education"])*0.30

            +

            score(self.country["Technology"])*0.20

            +

            score(self.country["Economy"])*0.20

            +

            score(self.country["Infrastructure"])*0.20

            +

            score(self.country["Political_Stability"])*0.10

        )

        return round(value,1)

    def investment(self):

        value = (

            score(self.country["Budget_Level"])*0.25

            +

            score(self.country["Government"])*0.20

            +

            score(self.country["Political_Stability"])*0.30

            +

            score(self.country["Digitalization"])*0.15

            +

            score(self.country["Infrastructure"])*0.10

        )

        return round(value,1)

    def life(self):

        value = (

            self.health()

            +

            self.education()

            +

            self.employment()

        ) / 3

        return round(value,1)