import pandas as pd

print(">>> Monitoring loaded successfully <<<")


class GlobalMonitoring:

    def __init__(self):
        self.problem_db = pd.read_csv("problem_dictionary.csv")

    def detect_global_problem(self, news, country=None):
        """
        Detect the most relevant CURRENT problem affecting the target country.

        Rules:
        - Ignore old news outside the recent time window.
        - Prefer articles explicitly related to the target country.
        - Require more than one keyword signal.
        - Do not invent a problem when evidence is insufficient.
        """

        if not news or not country:
            return "Unknown problem"

        from datetime import datetime, timedelta, timezone

        country = str(country).strip().lower()

        # Only consider recent news.
        recent_limit = datetime.now(timezone.utc) - timedelta(days=30)

        relevant_news = []

        for article in news:

            title = str(article.get("title", "") or "")
            description = str(article.get("description", "") or "")
            article_country = str(article.get("country", "") or "")

            text = f"{title} {description} {article_country}".lower()

            # ---------------------------------------------------------
            # 1. Check whether the article is recent
            # ---------------------------------------------------------

            published_at = (
                article.get("publishedAt")
                or article.get("published_at")
                or article.get("date")
            )

            is_recent = True

            if published_at:

                try:

                    published_at = str(published_at).replace(
                        "Z",
                        "+00:00"
                    )

                    published_date = datetime.fromisoformat(
                        published_at
                    )

                    if published_date.tzinfo is None:
                        published_date = published_date.replace(
                            tzinfo=timezone.utc
                        )

                    is_recent = published_date >= recent_limit

                except (ValueError, TypeError):

                    # If the date cannot be parsed,
                    # keep the article rather than throwing an error.

                    is_recent = True

            if not is_recent:
                continue

            # ---------------------------------------------------------
            # 2. Check whether the article is related to the country
            # ---------------------------------------------------------

            if country not in text:
                continue

            relevant_news.append(article)

        # No sufficiently recent country-related news
        if not relevant_news:
            return "Unknown problem"

        # -------------------------------------------------------------
        # 3. Build text ONLY from recent country-related news
        # -------------------------------------------------------------

        text = " ".join(
            (
                str(article.get("title", "") or "")
                + " "
                + str(article.get("description", "") or "")
                + " "
                + str(article.get("problem", "") or "")
            )
            for article in relevant_news
        ).lower()

        # -------------------------------------------------------------
        # 4. Score every problem in the dictionary
        # -------------------------------------------------------------

        scores = {}

        for _, row in self.problem_db.iterrows():

            problem_name = str(
                row["Problem_EN"]
            ).strip()

            keywords_raw = str(
                row["Keywords_EN"] or ""
            )

            keywords = [
                keyword.strip().lower()
                for keyword in keywords_raw.split(";")
                if keyword.strip()
            ]

            score = 0

            for keyword in keywords:

                if keyword in text:
                    score += 1

            scores[problem_name] = score

        # -------------------------------------------------------------
        # 5. Select the strongest CURRENT problem
        # -------------------------------------------------------------

        if not scores:
            return "Unknown problem"

        best_problem = max(
            scores,
            key=scores.get
        )

        best_score = scores[best_problem]

        # One weak keyword is not enough
        # to declare a national crisis.

        if best_score < 2:
            return "Unknown problem"

        return best_problem