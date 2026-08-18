import pandas as pd

print(">>> Monitoring loaded successfully <<<")


class GlobalMonitoring:

    def __init__(self):
        self.problem_db = pd.read_csv("problem_dictionary.csv")


    def detect_global_problem(self, news):

        if not news:
            return "Unknown problem"

        text = " ".join(
            (
                article.get("title", "") + " " +
                article.get("description", "") + " " +
                article.get("problem", "")
            )
            for article in news
        ).lower()

        scores = {}
        
        for _, row in self.problem_db.iterrows():

            score = 0

            keywords = row["Keywords_EN"].split(";")

            for keyword in keywords:

                if keyword.strip().lower() in text:
                    score += 1

            scores[row["Problem_EN"]] = score

            best_problem = max(scores, key=scores.get)

            if scores[best_problem] == 0:
                return "Unknown problem"

        return best_problem


        return "Unknown problem"
