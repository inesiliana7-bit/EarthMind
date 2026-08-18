import streamlit as st
import plotly.graph_objects as go


# =====================================================
# Future Simulation UI
# =====================================================

def render_future_simulation(
    simulation_data,
    years
):

    # -----------------------------
    # Session State
    # -----------------------------

    if "future_mode" not in st.session_state:
        st.session_state.future_mode = None

    if "graph_category" not in st.session_state:
        st.session_state.graph_category = "economy"

    if "selected_metric" not in st.session_state:
        st.session_state.selected_metric = None

    # =====================================================
    # TITLE
    # =====================================================

    st.markdown("""
    <div class="solution-card">

    <div class="solution-title">
    Future Simulation | المحاكاة المستقبلية
    </div>

    <div class="solution-text">

    Explore how the country may evolve after implementing
    the adaptive solution.

    استكشف كيف يمكن أن يتطور وضع الدولة بعد تطبيق
    الحل المتكيف.

    </div>

    </div>
    """, unsafe_allow_html=True)

    # =====================================================
    # MAIN BUTTONS
    # =====================================================

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "Graphical Analysis | الدراسة البيانية",
            use_container_width=True,
            key="future_graphs"
        ):
            st.session_state.future_mode = "graphs"
            st.rerun()

    with col2:

        if st.button(
            "See Your Country's Future | شاهد مستقبل وطنك",
            use_container_width=True,
            key="future_country"
        ):
            st.session_state.future_mode = "future"
            st.rerun()


    # =====================================================
    # ROUTING
    # =================================================

    if st.session_state.future_mode == "graphs":
        render_graphs(simulation_data, years)
        return

    if st.session_state.future_mode == "future":
        render_future_country()
        return


def render_graphs(
    simulation_data,
    years
):

    st.markdown("""
    <div class="solution-card">

    <div class="solution-title">
    Future Performance Analysis | تحليل الأداء المستقبلي
    </div>

    <div class="solution-text">

    Select a strategic sector to analyze future performance
    after implementing the adaptive solution.

    اختر قطاعاً استراتيجياً لتحليل الأداء المستقبلي
    بعد تطبيق الحل المتكيف.

    </div>

    </div>
    """, unsafe_allow_html=True)

    # ===============================
    # TOP CATEGORIES
    # ===============================

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        if st.button(
            "Economy\nالاقتصاد",
            use_container_width=True,
            key="eco"
        ):
            st.session_state.graph_category = "economy"
            st.rerun()

    with c2:

        if st.button(
            "Environment\nالبيئة",
            use_container_width=True,
            key="env"
        ):
            st.session_state.graph_category = "environment"
            st.rerun()

    with c3:

        if st.button(
            "Society\nالمجتمع",
            use_container_width=True,
            key="soc"
        ):
            st.session_state.graph_category = "society"
            st.rerun()

    with c4:

        if st.button(
            "Infrastructure\nالبنية التحتية",
            use_container_width=True,
            key="infra"
        ):
            st.session_state.graph_category = "infrastructure"
            st.rerun()

    st.divider()

    left, right = st.columns([1,3])

    # ==================================================
    # LEFT PANEL
    # ==================================================

    with left:

        category = st.session_state.graph_category

        if category == "economy":

            st.markdown("### Economy\n### الاقتصاد")

            if st.button("GDP\nالناتج المحلي", use_container_width=True):
                st.session_state.selected_metric = "gdp"
                st.rerun()

            if st.button("Inflation\nالتضخم", use_container_width=True):
                st.session_state.selected_metric = "inflation"
                st.rerun()

            if st.button("Employment\nالتوظيف", use_container_width=True):
                st.session_state.selected_metric = "employment"
                st.rerun()

            if st.button("Investment\nالاستثمار", use_container_width=True):
                st.session_state.selected_metric = "investment"
                st.rerun()

        elif category == "environment":

            st.markdown("### Environment\n### البيئة")

            if st.button("Air Quality\nجودة الهواء", use_container_width=True):
                st.session_state.selected_metric = "air"
                st.rerun()

            if st.button("Water\nالمياه", use_container_width=True):
                st.session_state.selected_metric = "water"
                st.rerun()

            if st.button("Carbon\nالكربون", use_container_width=True):
                st.session_state.selected_metric = "carbon"
                st.rerun()

            if st.button("Forest\nالغابات", use_container_width=True):
                st.session_state.selected_metric = "forest"

        elif category == "society":

            st.markdown("### Society\n### المجتمع")

            if st.button("Healthcare\nالصحة", use_container_width=True):
                st.session_state.selected_metric = "health"
                st.rerun()

            if st.button("Education\nالتعليم", use_container_width=True):
                st.session_state.selected_metric = "education"
                st.rerun()

            if st.button("Poverty\nالفقر", use_container_width=True):
                st.session_state.selected_metric = "poverty"
                st.rerun()

            if st.button("Quality of Life\nجودة الحياة", use_container_width=True):
                st.session_state.selected_metric = "life"
                st.rerun()

        else:

            st.markdown("### Infrastructure\n### البنية التحتية")

            if st.button("Roads\nالطرق", use_container_width=True):
                st.session_state.selected_metric = "roads"
                st.rerun()

            if st.button("Electricity\nالكهرباء", use_container_width=True):
                st.session_state.selected_metric = "electricity"
                st.rerun()

            if st.button("Internet\nالإنترنت", use_container_width=True):
                st.session_state.selected_metric = "internet"
                st.rerun()

            if st.button("Housing\nالإسكان", use_container_width=True):
                st.session_state.selected_metric = "housing"
                st.rerun()

    # ==================================================
    # RIGHT PANEL
    # ==================================================

    with right:

        if st.session_state.selected_metric is None:

            st.info(
                "Select an indicator to display the future simulation.\n\n"
                "اختر مؤشراً لعرض المحاكاة المستقبلية."
            )

        else:

            create_future_chart(
                st.session_state.selected_metric,
                simulation_data,
                years
            )

            return


def create_future_chart(
    metric,
    simulation_data,
    years
):

    metric_titles = {

        "gdp": ("Gross Domestic Product", "الناتج المحلي الإجمالي"),
        "inflation": ("Inflation Rate", "معدل التضخم"),
        "employment": ("Employment Rate", "معدل التوظيف"),
        "investment": ("Investment Level", "مستوى الاستثمار"),

        "air": ("Air Quality", "جودة الهواء"),
        "water": ("Water Resources", "الموارد المائية"),
        "carbon": ("Carbon Emissions", "انبعاثات الكربون"),
        "forest": ("Forest Coverage", "الغطاء الغابي"),

        "health": ("Healthcare", "الرعاية الصحية"),
        "education": ("Education", "التعليم"),
        "poverty": ("Poverty Rate", "معدل الفقر"),
        "life": ("Quality of Life", "جودة الحياة"),

        "roads": ("Road Network", "شبكة الطرق"),
        "electricity": ("Electricity Access", "الوصول إلى الكهرباء"),
        "internet": ("Digital Connectivity", "الاتصال الرقمي"),
        "housing": ("Housing", "الإسكان")

    }

    title_en, title_ar = metric_titles.get(
        metric,
        ("Indicator", "المؤشر")
    )

    current_data = {}

    for key, value in simulation_data["baseline"].items():
        current_data[key] = [value] * len(years)

    fig = go.Figure()

    # الوضع الحالي

    fig.add_trace(

        go.Scatter(

            x=years,

            y=current_data[metric],

            mode="lines",

            name="Current Situation",

            line=dict(

                color="#A0AEC0",

                width=3,

                dash="dash"

            )

        )

    )

    # بعد تطبيق الحل

    fig.add_trace(

        go.Scatter(

            x=years,

            y=simulation_data["simulation"][metric],

            mode="lines",

            name="Adaptive Scenario",

            line=dict(

                color="#0F4C81",

                width=4

            )

        )

    )

    fig.update_layout(

        title=dict(

            text=f"{title_en}<br><sup>{title_ar}</sup>",

            x=0.5

        ),

        template="plotly_white",

        height=560,

        hovermode="x unified",

        paper_bgcolor="white",

        plot_bgcolor="white",

        legend=dict(

            orientation="h",

            y=1.08,

            x=1,

            xanchor="right"

        ),

        margin=dict(

            l=30,

            r=30,

            t=90,

            b=30

        ),

        font=dict(

            family="Segoe UI",

            size=15

        ),

        xaxis=dict(

            title="Years | السنوات",

            showgrid=True,

            gridcolor="#ECECEC"

        ),

        yaxis=dict(

            title="Performance Index | مؤشر الأداء",

            range=[0,100],

            showgrid=True,

            gridcolor="#ECECEC"

        )

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    EXPLANATIONS = {

        "gdp": """
    Artificial Intelligence Analysis

    The adaptive strategy is projected to stimulate economic productivity,
    increase national competitiveness,
    and accelerate sustainable GDP growth.

    تحليل الذكاء الاصطناعي

    يتوقع أن يؤدي الحل المتكيف إلى
    رفع الإنتاجية الاقتصادية،
    وزيادة تنافسية الدولة،
    وتحقيق نمو مستدام للناتج المحلي.
    """,

        "inflation": """
    Artificial Intelligence Analysis

    Inflation is expected to stabilize gradually as
    economic efficiency improves and
    resource management becomes smarter.

    تحليل الذكاء الاصطناعي

    يتوقع انخفاض التضخم تدريجياً
    بفضل تحسين الكفاءة الاقتصادية
    وإدارة الموارد بشكل أكثر ذكاءً.
    """,

        "employment": """
    Artificial Intelligence Analysis

    The adaptive solution creates new economic opportunities,
    increasing employment
    while improving workforce productivity.

    تحليل الذكاء الاصطناعي

    يتوقع ارتفاع معدلات التوظيف
    نتيجة خلق فرص اقتصادية جديدة
    وزيادة إنتاجية القوى العاملة.
    """,

        "investment": """
    Artificial Intelligence Analysis

    Higher institutional confidence and
    improved governance attract
    additional domestic and foreign investments.

    تحليل الذكاء الاصطناعي

    يزيد الحل من ثقة المستثمرين،
    ويجذب استثمارات محلية وأجنبية جديدة.
    """,

        "air": """
    Artificial Intelligence Analysis

    Environmental policies supported by AI
    gradually improve air quality
    and reduce pollution.

    تحليل الذكاء الاصطناعي

    يساعد الحل على تحسين جودة الهواء
    وتقليل مستويات التلوث تدريجياً.
    """,

        "carbon": """
    Artificial Intelligence Analysis

    Carbon emissions decrease as
    renewable energy and
    resource optimization expand.

    تحليل الذكاء الاصطناعي

    تنخفض انبعاثات الكربون
    مع التوسع في الطاقة النظيفة
    وتحسين إدارة الموارد.
    """,

        "water": """
    Artificial Intelligence Analysis

    Water sustainability improves through
    efficient allocation,
    monitoring,
    and conservation.

    تحليل الذكاء الاصطناعي

    يتوقع تحسن استدامة المياه
    بفضل الإدارة الذكية
    وترشيد الاستهلاك.
    """,

        "forest": """
    Artificial Intelligence Analysis

    Forest preservation and restoration
    increase biodiversity
    and environmental resilience.

    تحليل الذكاء الاصطناعي

    يساعد الحل على زيادة الغطاء الغابي
    وتحسين التوازن البيئي.
    """,

        "health": """
    Artificial Intelligence Analysis

    Healthcare quality improves through
    better planning,
    resource allocation,
    and predictive services.

    تحليل الذكاء الاصطناعي

    يتوقع تحسن جودة الخدمات الصحية
    وزيادة كفاءة النظام الصحي.
    """,

        "education": """
    Artificial Intelligence Analysis

    Educational performance improves
    thanks to digital transformation,
    AI-assisted learning,
    and resource optimization.

    تحليل الذكاء الاصطناعي

    يتوقع ارتفاع جودة التعليم
    بفضل التحول الرقمي
    والتعلم المدعوم بالذكاء الاصطناعي.
    """,

        "poverty": """
    Artificial Intelligence Analysis

    Poverty gradually declines
    as economic opportunities expand
    and social programs become more effective.

    تحليل الذكاء الاصطناعي

    يتوقع انخفاض معدلات الفقر
    مع تحسن الاقتصاد
    وزيادة فعالية البرامج الاجتماعية.
    """,

        "life": """
    Artificial Intelligence Analysis

    Overall quality of life increases
    through balanced improvements
    across all national sectors.

    تحليل الذكاء الاصطناعي

    يتوقع تحسن جودة الحياة
    بفضل التطور المتوازن
    في مختلف القطاعات.
    """,

        "roads": """
    Artificial Intelligence Analysis

    Infrastructure modernization
    improves mobility,
    trade,
    and regional connectivity.

    تحليل الذكاء الاصطناعي

    يتوقع تحسن البنية التحتية
    وتسهيل النقل
    وزيادة الترابط الاقتصادي.
    """,

        "electricity": """
    Artificial Intelligence Analysis

    Electricity access becomes more reliable
    through intelligent energy management
    and renewable integration.

    تحليل الذكاء الاصطناعي

    يتوقع تحسن استقرار الكهرباء
    وزيادة الاعتماد على الطاقة النظيفة.
    """,

        "internet": """
    Artificial Intelligence Analysis

    Digital connectivity expands rapidly,
    supporting innovation,
    education,
    and economic growth.

    تحليل الذكاء الاصطناعي

    يتوقع توسع الاتصال الرقمي
    ودعم الابتكار
    والتعليم والاقتصاد.
    """,

        "housing": """
    Artificial Intelligence Analysis

    Urban planning becomes more efficient,
    leading to sustainable
    housing development.

    تحليل الذكاء الاصطناعي

    يتوقع تحسن قطاع الإسكان
    بفضل التخطيط الحضري الذكي.
    """
    }

    st.markdown(
        f"""
    <div class="solution-card">

    <div class="solution-title">
    Explainable AI | تفسير الذكاء الاصطناعي
    </div>

    <div class="solution-text">
    {EXPLANATIONS.get(metric)}
    </div>

    </div>
    """,
        unsafe_allow_html=True
    )

    # ============================================
    # KPI Dashboard
    # ============================================

    current_value = current_data[metric][-1]

    future_value = simulation_data["simulation"][metric][-1]

    improvement = future_value - current_value

    growth = (improvement / current_value) * 100

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(

            label="Current Situation | الوضع الحالي",

            value=f"{current_value:.1f}"

        )

    with c2:

        st.metric(

            label="Projected Value | القيمة المتوقعة",

            value=f"{future_value:.1f}",

            delta=f"+{improvement:.1f}"

        )

    with c3:

        st.metric(

            label="Growth Rate | معدل النمو",

            value=f"{growth:.1f}%"

        )

    st.markdown(
    """
    ### Interpretation | تفسير النتائج

    The adaptive solution is expected to improve this indicator over the simulation period according to the country's characteristics and implementation capacity.

    من المتوقع أن يؤدي تطبيق الحل المتكيف إلى تحسين هذا المؤشر تدريجياً وفق خصائص الدولة وقدرتها على تنفيذ الحل.
    """
    )

    st.info(

    """
    Prediction Confidence

    ثقة التنبؤ

    91%

    The prediction is generated using the country's profile,
    baseline indicators and adaptive solution.

    تم إنشاء التوقع اعتمادًا على ملف الدولة
    والمؤشرات الأساسية والحل المتكيف.
    """
    )

def render_future_country():

    st.markdown("""
    <div class="solution-card">

        <div class="solution-title">
        Future Country Vision | رؤية مستقبلية للدولة
        </div>

        <div class="solution-text">

        AI-generated visualization showing how the country may
        look after successfully implementing the adaptive solution.

        تصور مستقبلي مولد بالذكاء الاصطناعي يوضح كيف قد تصبح
        الدولة بعد التطبيق الناجح للحل المتكيف.

        </div>

    </div>
    """, unsafe_allow_html=True)

    st.info(
        """
The future image will be generated after the adaptive solution
is successfully implemented.

سيتم إنشاء الصورة المستقبلية للدولة بعد تطبيق الحل المتكيف.
"""
    )

    image_placeholder = st.empty()

    image_placeholder.markdown(
        """
<div style="

height:420px;

border:2px dashed #C7D2FE;

border-radius:18px;

display:flex;

justify-content:center;

align-items:center;

font-size:20px;

color:#64748B;

background:#F8FAFC;

">

Future AI Visualization

التصور المستقبلي للدولة

</div>
""",
unsafe_allow_html=True)

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Expected Quality\nالجودة المتوقعة",
            "High"
        )

    with col2:

        st.metric(
            "Prediction Horizon\nالأفق الزمني",
            "10 Years"
        )

    with col3:

        st.metric(
            "AI Confidence\nثقة الذكاء الاصطناعي",
            "92%"
        )