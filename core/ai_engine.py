import pandas as pd
from difflib import get_close_matches
from google import genai


class EarthMindAI:

    
    def __init__(self, memory_df, problems_df, api_key):

        self.memory_df = memory_df
        self.problems_df = problems_df
        self.client = genai.Client(api_key=api_key)

    def choose_best_reference(self, problem, candidates):

        prompt = f"""
You are EarthMind.

Detected problem:

{problem}

Below are all available reference cases.

{candidates.to_string(index=False)}

Choose ONLY ONE reference that best solves a problem similar to the detected one.

Consider:

- semantic similarity
- root cause
- affected sector
- infrastructure
- economy
- security
- environment

Return ONLY the exact Problem_EN.
"""

        try:

            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

        except Exception as e:

            print("="*60)
            print("GEMINI CONNECTION ERROR")
            print(type(e))
            print(e)
            print("="*60)

            return candidates.iloc[0]
            
        chosen_problem = response.text.strip()

        selected = candidates[
            candidates["Problem_EN"] == chosen_problem
        ]

        if not selected.empty:
            return selected.iloc[0]

        return candidates.iloc[0]

    def detect_problem(self, problem_name):

        filtered = self.memory_df[
            self.memory_df["Problem_EN"].astype(str).str.strip().str.lower()
            == str(problem_name).strip().lower()
        ]

        return filtered

    from difflib import get_close_matches

    def normalize_problem(self, problem_name):

        problems = self.memory_df["Problem_EN"].unique().tolist()

        # تطابق مباشر
        if problem_name in problems:
            return problem_name

        # أقرب اسم
        match = get_close_matches(
            problem_name,
            problems,
            n=1,
            cutoff=0.55
        )

        if match:
            print("Matched:", problem_name, "→", match[0])
            return match[0]

        return problem_name

    

    def ask_gemini_for_best_match(self, detected_problem, available_problems):

        prompt = f"""
You are the semantic matching engine of EarthMind.

Detected problem:
{detected_problem}

Existing Global Memory problems:

{chr(10).join("- " + p for p in available_problems)}

Your goal is NOT to match words.

Your goal is to identify which existing problem represents the SAME REAL-WORLD ISSUE.

Semantic matching rules:

- Think about the underlying crisis.
- Ignore wording differences.
- Prefer the same sector.
- Do NOT choose because two problems share one word.
- If the detected problem is broad, choose the most representative existing problem.
- NEVER invent a new name.
- Return EXACTLY one problem from the list.
- Return ONLY the problem name.

Answer:
"""

        try:

            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            match = response.text.strip()

            for p in available_problems:
                if p.casefold() == match.casefold():
                    return p

            print("Gemini returned:", match)
            return None

        except Exception as e:
            print(e)
            return None


    def choose_best_solution(self, problem_name):

        print("=" * 60)
        print("EARTHMIND SOLUTION MATCHING")
        print("Problem received:", repr(problem_name))
        print("=" * 60)

        # ---------------------------------
        # 1. Normalize the received problem
        # ---------------------------------

        if problem_name is None:
            return None

        problem_name = str(problem_name)
        problem_name = (
            problem_name
            .replace("\ufeff", "")
            .replace("\n", " ")
            .replace("\r", " ")
            .strip()
        )

        # ---------------------------------
        # 2. Problem aliases
        # ---------------------------------

        problem_aliases = {
            "Flood": "Flood Risk",
            "Floods": "Flood Risk",

            "Wildfire": "Wildfires",
            "Wildfires": "Wildfires",

            "Cyclone": "Cyclones",
            "Cyclones": "Cyclones",

            "Hurricane": "Hurricanes",
            "Hurricanes": "Hurricanes",

            "Heat Wave": "Heat Waves",
            "Heat Waves": "Heat Waves",

            "Trade Disruption": "Supply Chain Disruption",

            "Migration": "Migration",
            "Misinformation": "Misinformation",
            "Smuggling": "Smuggling",
            "Armed Conflict": "Armed Conflict",
            "Terrorism": "Terrorism",
            "Economic Crisis": "Economic Crisis",
            "Corruption": "Corruption",
            "Electricity Crisis": "Electricity Crisis",
            "Water Management": "Water Management",
            "Climate Resilience": "Climate Resilience",
            "Forest Protection": "Forest Protection",
            "Marine Protection": "Marine Protection",
            "Industrial Pollution": "Industrial Pollution",
            "Urban Mobility": "Urban Mobility",
            "Traffic Congestion": "Traffic Congestion",
            "Border Conflict": "Armed Conflict",
            "Border Tensions": "Armed Conflict",
            "Infrastructure Failure": "Infrastructure",
            "Infrastructure Collapse": "Infrastructure",
            "Infrastructure Damage": "Infrastructure",

            "Power Outage": "Electricity Crisis",
            "Energy Shortage": "Energy Security",

            "Cyber Attack": "Cybersecurity",
            "Fake News": "Misinformation",

            "Financial Collapse": "Financial Crisis",
            "Economic Downturn": "Economic Crisis",
        }

        detected_problem = problem_name
        search_problem = problem_aliases.get(
            detected_problem,
            detected_problem
        )

        # ---------------------------------
        # 3. Normalize database column
        # ---------------------------------

        memory = self.memory_df.copy()

        memory["Problem_EN_NORMALIZED"] = (
            memory["Problem_EN"]
            .astype(str)
            .str.replace("\ufeff", "", regex=False)
            .str.replace("\n", " ", regex=False)
            .str.replace("\r", " ", regex=False)
            .str.strip()
            .str.casefold()
        )

        target = search_problem.casefold()

        print("Searching for:", repr(search_problem))
        print("Normalized target:", repr(target))

        # ---------------------------------
        # 4. Exact matching
        # ---------------------------------

        filtered = memory[
            memory["Problem_EN_NORMALIZED"] == target
        ]

        print(
            "Number of exact matching solutions:",
            len(filtered)
        )

        # ---------------------------------
        # 5. If no exact match, try
        #    partial/contains matching
        # ---------------------------------

        # ---------------------------------
        # 5. If no exact match, ask Gemini
        # ---------------------------------

        if filtered.empty:

            available = (
                memory["Problem_EN"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )

            matched_problem = self.ask_gemini_for_best_match(
                detected_problem,
                available
            )

            print("Gemini selected:", matched_problem)

            if matched_problem is not None:

                target = matched_problem.casefold()

                filtered = memory[
                    memory["Problem_EN_NORMALIZED"] == target
                ]

            else:

                filtered = pd.DataFrame()

        # ---------------------------------
        # 6. Still nothing?
        # ---------------------------------

        if filtered.empty:

            print("No exact match.")
            print("Gemini is selecting the closest reference...")

            return self.choose_best_reference(
                detected_problem,
                memory
    )

        # ---------------------------------
        # 7. Select highest success rate
        # ---------------------------------

        filtered["Success_Rate"] = pd.to_numeric(
            filtered["Success_Rate"],
            errors="coerce"
        )

        # إذا وجد حل واحد فقط
        if len(filtered) == 1:
            return filtered.iloc[0]

        # إذا وجد عدة حلول
        best_solution = self.choose_best_reference(
            detected_problem,
            filtered
        )

        print("=" * 60)
        print("✅ SOLUTION FOUND")
        print(
            "Problem:",
            best_solution["Problem_EN"]
        )
        print(
            "Solution:",
            best_solution["Solution_EN"]
        )
        print(
            "Reference Country:",
            best_solution["Country_EN"]
        )
        print(
            "Success Rate:",
            best_solution["Success_Rate"]
        )
        print("=" * 60)

        return best_solution

    def search_by_country(self, country):

        return self.memory_df[
            self.memory_df["Country_EN"] == country
        ]

    def search_by_sector(self, sector):

        return self.memory_df[
            self.memory_df["Sector_EN"] == sector
        ]

    def global_statistics(self):

        return {

            "Countries":
            self.memory_df["Country_EN"].nunique(),

            "Problems":
            self.memory_df["Problem_EN"].nunique(),

            "Solutions":
            self.memory_df["Solution_EN"].nunique()

        }