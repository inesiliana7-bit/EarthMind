import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from core.simulation_engine import FutureSimulationEngine
from UI.future_simulation import render_future_simulation

from connectors.gnews import get_news
from core.adaptive_engine import AdaptiveEngine
from core.ai_engine import EarthMindAI
from core.data_fusion import collect_all_sources
from core.gemini_brain import GeminiBrain
brain = GeminiBrain()
from core.report_generator import generate_report
from core.adaptive_engine import AdaptiveEngine
from UI.styles import MAIN_CSS
import monitoring

monitor = monitoring.GlobalMonitoring()

from dotenv import load_dotenv
import os
import ast

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

adaptive_ai = AdaptiveEngine(API_KEY)

countries_df = pd.read_csv("countries.csv")
country_profiles_df = pd.read_csv("country_profiles.csv")
memory_df = pd.read_csv("global_memory.csv")
print(memory_df["Problem_EN"].unique())
problems_df = pd.read_csv("problem_dictionary.csv")
earthmind_ai = EarthMindAI(
    memory_df,
    problems_df,
    API_KEY
)

import inspect

print("Module:", monitoring.__file__)
print("Signature:", inspect.signature(monitoring.GlobalMonitoring.detect_global_problem))
print("Source:")
print(inspect.getsource(monitoring.GlobalMonitoring.detect_global_problem))

st.set_page_config(page_title="EarthMind", layout="wide")

st.markdown(
    f"<style>{MAIN_CSS}</style>",
    unsafe_allow_html=True
)

import streamlit as st

left_space, logo_col, title_col, right_space = st.columns([1.5, 1, 4, 1.5])

with logo_col:
    st.image("assets/logo.png", width=180)

with title_col:
    st.markdown("""
        <div class="title">EarthMind</div>
    <style>
    .title {
        font-size: 100px;
        font-weight: bold;
        color: #0f4c5c;
        font-family: "Georgia";
        margin:0;
        padding-top:15px;}
    </style>

    </div>
    """, unsafe_allow_html=True)

st.markdown("""
    <div class="subtitle">نتعلم من الأمس، نحاكي اليوم، لنحمي الغد</div>
<style>
@import url('https://fonts.googleapis.com/css2?family=Reem+Kufi:wght@500&display=swap');
.subtitle {
    font-family: 'Reem Kufi', sans-serif;
    font-size: 45px;
    color: #1b6b7a;
    letter-spacing: 1px;
    text-align:center;
    margin-top: 15px;
    margin-bottom: 55px;
}
</style>""",unsafe_allow_html=True)


st.markdown("""
    <div class="card">
    <h3>scientific Vision | الرؤية العلمية</h3>
    أول منصة رقمية عالمية تهدف إلى تحويل خبرات البشرية إلى حلول قابلة للتكيف محلياً،
    ومحاكاة آثار القرارات المستقبلية قبل تنفيذها بما يسهم في حماية مستقبل الأرض</div>
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap');
.card {
    background: white;
    padding: 25px;
    margin-left: auto;
    margin-right: auto;
    max-width: 800px;
    border-radius: 15px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    margin-bottom: 55px;

    font-family: 'Tajawal', sans-serif;
    font-size: 20px;
    color: #1c3c4c;
    line-height: 2;
    text-align: center;}
</style>""",unsafe_allow_html=True)

# القائمة الجانبية
st.sidebar.title("EarthMind")

page = st.sidebar.radio(
    "Navigation | التنقل",
    [
        "Home | الرئيسية",
        "Future Simulation | المحاكاة المستقبلية",
        "Reports | التقارير"
    ]
)

st.markdown("""
    <div class="glob_title">Global Observer | المرصد العالمي</div>
""", unsafe_allow_html=True)


# Countries Database | قاعدة بيانات الدول

countries = (
    countries_df[["Country_EN", "Country_AR"]]
    .drop_duplicates()
    .sort_values("Country_EN")
)

selected_country = st.selectbox(

    "Select Country | اختر الدولة",

    countries_df["Country_EN"] + " | " + countries_df["Country_AR"]

)

selected_country_row = countries[

    countries["Country_EN"] +
    " | " +
    countries["Country_AR"]

    == selected_country

].iloc[0]

country_en = selected_country_row["Country_EN"]

country_ar = selected_country_row["Country_AR"]

if "analysis_completed" not in st.session_state:
    st.session_state.analysis_completed = False

# زر التحليل

if st.button(
    "Run Global Intelligence Analysis | تشغيل التحليل العالمي",
    key="run_ai"
):

    sources = collect_all_sources(country_en)

    all_events = []

    # أخبار GNews
    if sources["news"]:
        all_events.extend(sources["news"])

    # أحداث NASA
    if sources["nasa"]:
        all_events.extend(sources["nasa"])

    print("================================")
    print("Country:", country_en)

    for event in all_events:
        print(event)

    print("================================")

    analysis = brain.analyze(
        country_en,
        sources["news"],
        sources["nasa"],
        problems_df["Problem_EN"].unique().tolist()
    )
    
    if analysis is None:
        st.error("AI analysis failed | فشل تحليل الذكاء الاصطناعي")
        st.stop()

    problem = analysis.get(
        "primary_problem",
        analysis.get("problem", "Unknown problem")
    )

    print("=" * 60)
    print("Problem from Gemini =", repr(problem))
    print("=" * 60)

    if problem == "SERVICE_BUSY":
        st.warning(
            " Gemini servers are currently busy.\n\n"
            "Please try again in a few moments.\n\n"
            " خوادم جيميني مشغولة حاليا، حاول بعد قليل  "
        )
        st.stop()

    if problem == "QUOTA_EXCEEDED":
        st.error(
            " Gemini free quota exceeded.\n\n"
            " لقد استهلكت الحصة اليومية المجانية لـجيميني"
        )
        st.stop()

    print("=" * 50)
    print("ANALYSIS =", analysis)
    print("=" * 50)

    print("Analysis =", analysis)

    if analysis is None:
        problem = "Unknown problem"
    else:
        problem = analysis.get(
            "primary_problem",
            analysis.get("problem", "Unknown problem")
        )

    print("STEP A")

    best_solution = earthmind_ai.choose_best_solution(problem)

    if best_solution is None:

        st.error(
            "No solution found | لا يوجد حل في قاعدة البيانات"
        )

        st.stop()

    adaptive_ai = AdaptiveEngine(API_KEY)

    print("Country selected:", country_en)
    print(country_profiles_df["Country"].tolist())

    country_match = country_profiles_df[
        country_profiles_df["Country"].str.strip().str.casefold()
        == country_en.strip().casefold()
    ]

    if country_match.empty:
        st.error(f"Country '{country_en}' not found in country_profiles.csv")
        st.stop()

    country_info = country_match.iloc[0].to_dict()

    print("STEP B")
    print(best_solution)

    adaptive_result = adaptive_ai.adapt_solution(
        country_info,
        analysis,
        best_solution
    )

    print("STEP C")

    print("STEP D")


    print("Gemini:", repr(problem))
    print("Database:")
    print(memory_df["Problem_EN"].tolist())

    print("=" * 50)
    print("Detected problem:", repr(problem))
    print("=" * 50)

    for p in memory_df["Problem_EN"]:
        print(repr(p))


    print("=" * 60)
    print("Best solution =", best_solution)
    print("=" * 60)

    
    if best_solution is None:

        st.error(
            "No solution found | لا يوجد حل في قاعدة البيانات"
        )

    else:

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"""
            <div class="metric-card">
            <div class="metric-title">
            Detected Problem | المشكلة المكتشفة
            </div>
            <div class="metric-value">
                {analysis.get("primary_problem", analysis.get("problem", "Unknown problem"))}<br>
                {analysis.get("primary_problem_ar", "غير معروف")}
            </div>
            </div>
            """, unsafe_allow_html=True)
    
        with col2:
            st.markdown(f"""
            <div class="metric-card">
            <div class="metric-title">
            Reference Country | الدولة المرجعية
            </div>

            <div class="metric-value">
            {best_solution["Country_EN"]}<br>
            {best_solution["Country_AR"]}
            </div>
            </div>
            """, unsafe_allow_html=True)

        

        st.markdown(f"""
        <div class="solution-card">

        <div class="solution-title">
        Recommended Solution | الحل المرجعي
        </div>

        <div class="solution-text">
        {best_solution["Solution_EN"]}
        <br>
        {best_solution["Solution_AR"]}
        </div>

        </div>
        """, unsafe_allow_html=True)


        st.markdown("""
        <div class="solution-card">

        <div class="solution-title">
        Adaptive Solution | الحل المتكيف
        </div>

        <div class="bilingual-grid">

        <div class="language-panel">
        <div class="language-label">ENGLISH</div>
        <div class="solution-text">
            {solution_en}
        </div>
        </div>

        <div class="language-panel arabic-panel">
        <div class="language-label">العربية</div>
        <div class="solution-text">
            {solution_ar}
        </div>
        </div>

        </div>
        </div>
        """.format(
            solution_en=adaptive_result["adaptive_solution_en"].replace(
                "\n", "<br>"
            ),
            solution_ar=adaptive_result["adaptive_solution_ar"].replace(
                "\n", "<br>"
            )
        ), unsafe_allow_html=True)

        print("========== CHECK ==========")
        print(adaptive_result)
        print(type(adaptive_result))
        print("===========================")

        
        col3, col4 = st.columns(2)
  
        with col3:
            st.markdown(f"""
            <div class="metric-card"> 
            <div class="metric-title">
            Estimated Success Rate | نسبة النجاح المتوقعة
            </div>
    
            <div class="metric-value">
            {adaptive_result["estimated_success"]}%
            </div>
            </div>

            """, unsafe_allow_html=True)
  
        with col4:
            st.markdown(f"""
            <div class="metric-card">
            <div class="metric-title">
            Estimated Implementation Time | مدة التنفيذ المتوقعة
            </div>
  
            <div class="metric-value">
            {adaptive_result["estimated_duration"]} Years
            </div>
            </div>
            """, unsafe_allow_html=True)

    simulation_engine = FutureSimulationEngine()

    simulation_data = simulation_engine.simulate(
        country_info,
        adaptive_result
    )

    st.session_state.analysis = analysis
    st.session_state.best_solution = best_solution
    st.session_state.adaptive_result = adaptive_result
    st.session_state.country_info = country_info

    st.session_state.simulation_data = simulation_data
    st.session_state.simulation_years = simulation_data["years"]

    st.session_state.analysis_completed = True

    st.subheader(
        "AI Intelligence Report | تقرير الذكاء الاصطناعي"
    )

    report = generate_report(
        country_en,
        country_ar,
        analysis,
        best_solution,
        len(sources["news"]),
        len(sources["nasa"]),
        len(all_events)
    )
    with st.expander(
        "📑 AI Intelligence Report | تقرير الذكاء الاصطناعي",
        expanded=False
    ):
        st.markdown(
            report,
            unsafe_allow_html=True
        )
if "adaptive_result" not in locals():
    adaptive_result = {
        "adaptive_solution_en": "No adaptive solution available.",
        "adaptive_solution_ar": "لا يوجد حل متكيف متاح حاليًا.",
        "estimated_success": 0,
        "estimated_duration": 0,
        "budget_level_en": "Unknown",
        "budget_level_ar": "غير متوفر",
        "adaptation_points_en": [],
        "adaptation_points_ar": []
    }
if page == "Home | الرئيسية":
    st.markdown("---")
    st.subheader("Earth Status Dashboard | لوحة حالة الأرض")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Climate Risk", "67%", "+3%")
    with col2:
        st.metric("Water Stress", "52%", "-1%")
    with col3:
        st.metric("Food Security", "81%", "+5%")
elif page == "Global Memory | الذاكرة العالمية":

    st.header("Global Memory | الذاكرة العالمية")

    country = st.selectbox(
        "Select Country | اختر الدولة",
        memory_df["Country_EN"]
    )

    result = memory_df[
        memory_df["Country_EN"] == country
    ]

    st.subheader(
        "Problem | المشكلة"
    )
    st.subheader(
        "Sector | القطاع"
    )
    st.subheader(
        "Success Rate | نسبة النجاح"
    )
    st.subheader(
        "Implementation Period | مدة التنفيذ"
    )

    st.info(
        str(result.iloc[0]["Implementation_Years"])
        + " Years | سنة"
    )
    st.metric(
        "Success Rate",
        tr(result.iloc[0]["Success_Rate"]) + "%"
    )
    st.info(
        result.iloc[0]["Sector_EN"]
        + " | " +
        result.iloc[0]["Sector_AR"]
    )
    st.info(
        result.iloc[0]["Problem_EN"]
        + " | " +
        result.iloc[0]["Problem_AR"]
    )

    st.subheader(
        "Solution | الحل"
    )

    st.success(
        result.iloc[0]["Solution_EN"]
        + " | " +
        result.iloc[0]["Solution_AR"]
    )

elif page == "Global Monitoring | الرصد العالمي":

    st.header("Global Monitoring | الرصد العالمي")

    problem = st.selectbox(
        "Problem Type | نوع المشكلة",
        [
            "Climate Change",
            "Water Scarcity",
            "Food Security",
            "Energy",
            "Pollution",
            "Health"
        ]
    )

    st.write("تحليل المشكلة عالمياً.")

elif page == "Future Simulation | المحاكاة المستقبلية":

    if st.session_state.get("analysis_completed", False):

        render_future_simulation(
            st.session_state.simulation_data,
            st.session_state.simulation_years
        )

    else:

        st.warning(
            "Run the Global Intelligence Analysis first.\n\n"
            "قم أولاً بتشغيل التحليل العالمي."
        )

elif page == "Adaptive Intelligence Engine | محرك الذكاء التكيفي":

    st.header("Adaptive Intelligence Engine | محرك الذكاء التكيفي")

    st.write(
        "اقتراح حلول قابلة للتكيف محلياً اعتماداً على الخبرات العالمية."
    )


