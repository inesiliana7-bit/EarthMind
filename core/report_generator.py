from datetime import datetime

REPORT_STYLE = """
<style>

body{
    font-family:Segoe UI,Arial,sans-serif;
    color:#222;
    line-height:1.8;
}

.report-title{
    font-size:60px;
    font-weight:700;
    font-family:'Playfair Display', serif;
    text-align:center;
    color:#123B70;
    margin-top:40px;
    margin-bottom:10px;
}

.report-subtitle{
    text-align:center;
    margin-bottom:35px;
    font-size:18px;
    text-align:center;
    color:#666;
    margin-bottom:50px;
}

.section{
    margin-top:45px;
    margin-bottom:45px;
}

.section-title{
    display:flex;
    justify-content:space-between;
    align-items:center;
    font-size:30px;
    font-weight:700;
    color:#123B70;
    margin-bottom:25px;
    padding-bottom:15px;
    border-bottom:1px solid #E5E7EB;
    font-family:'Playfair Display', serif;
    font-family:
    "Georgia",
    "Cairo",
    sans-serif;
}

.title-en{
    color:#0F4C81;
}

.title-ar{
    color:#0F4C81;
    direction:rtl;
    text-align:right;
}

.info-card{
    background:white;
    padding:35px;
    border-radius:18px;
    border:1px solid #E5E7EB;
    box-shadow:0 6px 20px rgba(0,0,0,.05);
    margin-top:18px;
}

table{
    width:100%;
    border-collapse:collapse;
    margin-top:25px;
}

th{
    background:#F5F8FC;
    padding:18px;
}

td{
    padding:18px;
    border:1px solid #ECECEC;
}

.bilingual-grid{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:25px;
}

.language-panel{
    background:#ffffff;
    border:1px solid #E5E7EB;
    border-radius:12px;
    padding:18px;
}

.language-panel{
    font-size:19px;
}

.language-panel h4{
    margin-top:0;
    color:#0F4C81;
}

.language-panel table{
    width:100%;
    border-collapse:collapse;
}

.language-panel th{
    width:40%;
    background:#F3F6FA;
    color:#123B70;
    text-align:left;
    padding:10px;
    border:1px solid #DDD;
}

.language-panel td{
    padding:10px;
    border:1px solid #DDD;
}

.arabic-panel{
    direction:rtl;
    text-align:right;
    font-family:
    "Tajawal",
    "Cairo",
    sans-serif;
    font-size:19px;
    line-height:2;
}

</style>
"""


def build_card(title_en,title_ar,content):

    return f"""

<div class="section">

<div class="section-title">

<div class="title-en">
    {title_en}
</div>

<div class="title-ar">
    {title_ar}
</div>

</div>

<div class="info-card">

{content}

</div>

</div>

"""

def build_header():

    today = datetime.now().strftime("%d %B %Y")

    report = REPORT_STYLE + f"""

<div class="report-title">

EARTHMIND

</div>

<div class="report-subtitle">

Global Intelligence Report

</div>

"""
    return report

def build_summary(country_en, country_ar, analysis):

    problem_en = analysis.get(
        "primary_problem",
        analysis.get("problem", "Unknown")
    )

    problem_ar = analysis.get(
        "primary_problem_ar",
        analysis.get("problem_ar", "غير معروف")
    )

    confidence = analysis.get(
        "confidence",
        0
    )

    body = f"""

<div class="bilingual-grid">

<div class="language-panel">
<div class="language-label">ENGLISH</div>

<p>
EarthMind analyzed multiple trusted information sources including international news,
scientific observations and global intelligence databases.
</p>

<p>
The highest-priority national issue is
<b>{problem_en}</b>.
</p>

<p>
Confidence: <b>{confidence}%</b>
</p>

</div>

<div class="language-panel arabic-panel">

<div class="language-label">العربية</div>

<p dir="rtl">
اعتمدت منصة EarthMind على الأخبار الدولية والبيانات العلمية وقواعد المعرفة العالمية.
</p>

<p dir="rtl">
تم تحديد المشكلة ذات الأولوية:

<b>{problem_ar}</b>
</p>

<p dir="rtl">
درجة الثقة:
<b>{confidence}%</b>
</p>

</div>

</div>
"""

    return build_card(
        "EXECUTIVE SUMMARY",
        "الملخص التنفيذي",
        body
    )

def generate_report(
    country_en,
    country_ar,
    analysis,
    best_solution,
    news_count,
    nasa_count,
    total_sources
):

    primary_problem = analysis.get(
        "primary_problem",
        analysis.get("problem", "Unknown")
    )

    primary_problem_ar = analysis.get(
        "primary_problem_ar",
        analysis.get("problem_ar", "غير معروف")
    )

    confidence = analysis.get("confidence", 0)

    confidence_reason = analysis.get(
        "confidence_reason",
        "No confidence explanation available."
    )

    news_coverage = analysis.get(
        "news_coverage",
        0
    )

    scientific_support = analysis.get(
        "scientific_support",
        0
    )

    root_cause = analysis.get(
        "root_cause",
        "Not available"
    )

    root_cause_ar = analysis.get(
        "root_cause_ar",
        "غير متوفر"
    )

    risk_level = analysis.get(
        "risk_level",
        "Unknown"
    )

    risk_level_ar = analysis.get(
        "risk_level_ar",
        "غير معروف"
    )

    impact_dimensions = analysis.get(
        "impact_dimensions",
        []
    )

    impact_dimensions_ar = analysis.get(
        "impact_dimensions_ar",
        []
    )

    future_consequences = analysis.get(
        "future_consequences",
        "No prediction available."
    )

    future_consequences_ar = analysis.get(
        "future_consequences_ar",
        "لا يوجد توقع متوفر."
    )

    recommendation = analysis.get(
        "recommendation",
        "No recommendation available."
    )

    recommendation_ar = analysis.get(
        "recommendation_ar",
        "لا توجد توصية متوفرة."
    )

    findings = analysis.get(
        "key_findings",
        []
    )

    findings_ar = analysis.get(
        "key_findings_ar",
        []
    )

    data_quality = analysis.get(
        "data_quality",
        "Insufficient"
    )

    report = build_header()

    # EXECUTIVE SUMMARY

    report += build_summary(
        country_en,
        country_ar,
        analysis
    )

    # CRISIS ASSESSMENT

    report += build_card(
        "CRISIS ASSESSMENT",
        "تقييم الأزمة",
        f"""
<div class="bilingual-grid">

<div class="language-panel">

<h4>English</h4>

<table>
<tr>
<th>Country</th>
<td>{country_en}</td>
</tr>

<tr>
<th>Primary National Problem</th>
<td>{primary_problem}</td>
</tr>

<tr>
<th>Confidence</th>
<td>{confidence}%</td>
</tr>

<tr>
<th>Risk Level</th>
<td>{risk_level}</td>
</tr>
</table>

</div>

<div class="language-panel arabic-panel">

<h4>العربية</h4>

<table dir="rtl">

<tr>
<th>الدولة</th>
<td>{country_ar}</td>
</tr>

<tr>
<th>المشكلة الوطنية الرئيسية</th>
<td>{primary_problem_ar}</td>
</tr>

<tr>
<th>درجة الثقة</th>
<td>{confidence}%</td>
</tr>

<tr>
<th>مستوى الخطورة</th>
<td>{risk_level_ar}</td>
</tr>

</table>

</div>

</div>
"""
)

    # EVIDENCE ANALYSIS

    report += build_card(
        "EVIDENCE ANALYSIS",
        "تحليل الأدلة",
        f"""
<div class="bilingual-grid">

<div class="language-panel">

<h4>English</h4>

<table>

<tr>
<th>News Sources</th>
<td>{news_count}</td>
</tr>

<tr>
<th>Scientific Observations</th>
<td>{nasa_count}</td>
</tr>

<tr>
<th>Total Sources</th>
<td>{total_sources}</td>
</tr>

<tr>
<th>News Support</th>
<td>{news_coverage}%</td>
</tr>

<tr>
<th>Scientific Support</th>
<td>{scientific_support}%</td>
</tr>

<tr>
<th>Evidence Quality</th>
<td>{data_quality}</td>
</tr>

<tr>
<th>Confidence Reason</th>
<td>{confidence_reason}</td>
</tr>

</table>

</div>

<div class="language-panel arabic-panel">

<h4>العربية</h4>

<table dir="rtl">

<tr>
<th>المصادر الإخبارية</th>
<td>{news_count}</td>
</tr>

<tr>
<th>المصادر العلمية</th>
<td>{nasa_count}</td>
</tr>

<tr>
<th>إجمالي المصادر</th>
<td>{total_sources}</td>
</tr>

<tr>
<th>دعم الأخبار</th>
<td>{news_coverage}%</td>
</tr>

<tr>
<th>الدعم العلمي</th>
<td>{scientific_support}%</td>
</tr>

<tr>
<th>جودة الأدلة</th>
<td>{data_quality}</td>
</tr>

<tr>
<th>سبب الثقة</th>
<td>{analysis.get("confidence_reason_ar","")}</td>
</tr>

</table>

</div>

</div>
"""
)
    
    # ROOT CAUSE

    report += build_card(
        "UNDERLYING CAUSE",
        "السبب الجذري",
        f"""
<div class="bilingual-grid">

<div class="language-panel">

<h4>English</h4>

<table>

<tr>
<th>Current Crisis</th>
<td>{primary_problem}</td>
</tr>

<tr>
<th>Underlying Cause</th>
<td>{root_cause}</td>
</tr>

</table>

</div>

<div class="language-panel arabic-panel">

<h4>العربية</h4>

<table dir="rtl">

<tr>
<th>الأزمة الحالية</th>
<td>{primary_problem_ar}</td>
</tr>

<tr>
<th>السبب الجذري</th>
<td>{root_cause_ar}</td>
</tr>

</table>

</div>

</div>
"""
)

    # IMPACT DIMENSIONS

    impact_text_en = "<br>".join(impact_dimensions)
    impact_text_ar = "<br>".join(impact_dimensions_ar)
    
    report += build_card(
        "IMPACT DIMENSIONS",
        "مجالات التأثير",
        f"""
<div class="bilingual-grid">

<div class="language-panel">

<h4>English</h4>

<table>

<tr>
<th>Affected Dimensions</th>
<td>{impact_text_en}</td>
</tr>

</table>

</div>

<div class="language-panel arabic-panel">

<h4>العربية</h4>

<table dir="rtl">

<tr>
<th>المجالات المتأثرة</th>
<td>{impact_text_ar}</td>
</tr>

</table>

</div>

</div>
"""
)

    # KEY FINDINGS

    findings_text_en="<br>".join(findings)
    findings_text_ar="<br>".join(findings_ar)

    report += build_card(
        "KEY FINDINGS",
        "النتائج الرئيسية",
        f"""
<div class="bilingual-grid">

<div class="language-panel">

<h4>English</h4>

<table>

<tr>
<th>Main Findings</th>
<td>{findings_text_en}</td>
</tr>

</table>

</div>

<div class="language-panel arabic-panel">

<h4>العربية</h4>

<table dir="rtl">

<tr>
<th>النتائج الرئيسية</th>
<td>{findings_text_ar}</td>
</tr>

</table>

</div>

</div>
"""
)
    # FUTURE CONSEQUENCES

    report += build_card(
        "FUTURE CONSEQUENCES",
        "العواقب المستقبلية",
        f"""
<div class="bilingual-grid">

<div class="language-panel">

<h4>English</h4>

<table>

<tr>
<th>Predicted Consequences</th>
<td>{future_consequences}</td>
</tr>

</table>

</div>

<div class="language-panel arabic-panel">

<h4>العربية</h4>

<table dir="rtl">

<tr>
<th>العواقب المتوقعة</th>
<td>{future_consequences_ar}</td>
</tr>

</table>

</div>

</div>
"""
)

    # STRATEGIC RECOMMENDATION

    report += build_card(
        "STRATEGIC RECOMMENDATION",
        "التوصية الاستراتيجية",
        f"""
<div class="bilingual-grid">

<div class="language-panel">

<h4>English</h4>

<table>

<tr>
<th>Recommendation</th>
<td>{recommendation}</td>
</tr>

</table>

</div>

<div class="language-panel arabic-panel">

<h4>العربية</h4>

<table dir="rtl">

<tr>
<th>التوصية</th>
<td>{recommendation_ar}</td>
</tr>

</table>

</div>

</div>
"""
)

    # EARTHMIND ASSESSMENT

    report += build_card(
        "EARTHMIND ASSESSMENT",
        "تقييم EarthMind",
        """
<div class="bilingual-grid">

<div class="language-panel">

<h4>English</h4>

<table>

<tr>
<th>Assessment Method</th>
<td>
National news intelligence<br>
Scientific observations<br>
AI reasoning<br>
Evidence quality assessment<br>
Environmental intelligence
</td>
</tr>

<tr>
<th>Decision Logic</th>
<td>
EarthMind prioritizes national crises using evidence quality,
severity, impact, and AI reasoning rather than selecting
the most frequently mentioned issue.
</td>
</tr>

</table>

</div>

<div class="language-panel arabic-panel">

<h4>العربية</h4>

<table dir="rtl">

<tr>
<th>يعتمد التقييم على</th>
<td>
المعلومات الإخبارية الوطنية<br>
الملاحظات والبيانات العلمية<br>
تحليل الذكاء الاصطناعي<br>
تقييم جودة الأدلة<br>
الذكاء البيئي
</td>
</tr>

<tr>
<th>منهجية اتخاذ القرار</th>
<td>
تعتمد EarthMind على جودة الأدلة، ومستوى الخطورة،
وحجم التأثير، وتحليل الذكاء الاصطناعي لترتيب
الأزمات الوطنية، وليس فقط على تكرار ظهورها
في الأخبار.
</td>
</tr>

</table>

</div>

</div>
"""
)

    # REPORT STATUS

    report += build_card(
    "REPORT STATUS",
    "حالة التقرير",
    """
<div class="bilingual-grid">

<div class="language-panel">

<h4>English</h4>

<table>

<tr>
<th>Status</th>
<td>Completed Successfully</td>
</tr>

<tr>
<th>Generated By</th>
<td>EarthMind AI</td>
</tr>

</table>

</div>

<div class="language-panel arabic-panel">

<h4>العربية</h4>

<table dir="rtl">

<tr>
<th>الحالة</th>
<td>تم إنشاء التقرير بنجاح</td>
</tr>

<tr>
<th>تم الإنشاء بواسطة</th>
<td>EarthMind AI</td>
</tr>

</table>

</div>

</div>
"""
)

    return report

    