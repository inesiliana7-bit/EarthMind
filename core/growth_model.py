import math


class GrowthModel:

    @staticmethod
    def simulate(
        baseline,
        impact,
        years,
        sector_factor
    ):

        values = []

        current = float(baseline)

        for year in range(len(years)):

            progress = 1 - math.exp(-0.40 * year)

            growth = impact * sector_factor * progress

            current = current + growth

            current = max(0, min(current, 100))

            values.append(round(current, 2))

        return values