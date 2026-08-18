# ==========================================================
# EarthMind
# Shock Engine
# ==========================================================

import random


class ShockEngine:

    def __init__(self, seed=None):

        self.rng = random.Random(seed)

        self.events = [

            {
                "name": "Economic Crisis",
                "probability": 0.10,
                "effects": {
                    "gdp": -4,
                    "investment": -6,
                    "employment": -3,
                    "poverty": 4,
                    "inflation": 3
                }
            },

            {
                "name": "Technology Boom",
                "probability": 0.08,
                "effects": {
                    "gdp": 4,
                    "internet": 6,
                    "investment": 5,
                    "employment": 2
                }
            },

            {
                "name": "Climate Disaster",
                "probability": 0.08,
                "effects": {
                    "air": -4,
                    "water": -5,
                    "forest": -5,
                    "carbon": 4,
                    "gdp": -2
                }
            },

            {
                "name": "Healthcare Reform",
                "probability": 0.07,
                "effects": {
                    "health": 5,
                    "life": 3
                }
            }

        ]

    def apply(self, state):

        state = state.copy()

        triggered = []

        for event in self.events:

            if self.rng.random() < event["probability"]:

                triggered.append(
                    event["name"]
                )

                for metric, change in event["effects"].items():

                    if metric in state:

                        state[metric] += change

        for metric in state:

            state[metric] = max(
                0,
                min(
                    state[metric],
                    100
                )
            )

        return state, triggered