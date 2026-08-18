MAIN_CSS = """

.stApp {
    background: linear-gradient(
        to bottom right,
        #f8fbff,
        #e9f3ff,
        #d9ebff,
        #eef7ff
    );
}

.stButton > button{
    width:100%;
    height:65px;
    border-radius:18px;
    background:linear-gradient(135deg,#0F4C81,#1E88E5);
    color:white;
    font-size:20px;
    font-weight:700;
    border:none;
    transition:0.3s;
}

.stButton > button:hover{
    transform:translateY(-3px);
    box-shadow:0 10px 20px rgba(0,0,0,.25);
}

.brand-logo {
    display: flex;
    align-items: center;
    justify-content: center;
}

.glob_title {
    font-size: 60px;
    font-weight: bold;
    color: #0f4c5c;
    font-family: "Georgia";
    text-align: center;
    margin-bottom: 10px;
}

.feature-card{
    background: rgba(255,255,255,0.9);
    padding:25px;
    border-radius:20px;
    box-shadow:0 4px 20px rgba(0,0,0,0.08);
    text-align:center;
    margin-bottom:20px;
}

.feature-title{
    font-size:24px;
    font-weight:bold;
    color:#0f4c5c;
}

.feature-text{
    font-size:18px;
    color:#37586a;
    font-family:'Tajawal',sans-serif;
}

.metric-card{
    background:white;
    border-radius:20px;
    padding:28px;
    margin:18px 0;
    box-shadow:
    0 8px 24px rgba(0,0,0,.06);
    border:1px solid #ECECEC;
}

.metric-title {
    font-size: 22px;
    font-weight: 700;
    color: #0f4c5c;
    font-family: 'Georgia', serif;
    margin-bottom: 10px;
    text-align: center;
}

.metric-value {
    font-size: 18px;
    color: #1c3c4c;
    margin-top: 5px;
    line-height: 1.6;
    text-align: center;
}

.solution-card{
    background:linear-gradient(
    135deg,
    #eef6ff,
    #f8fbff
    );
    border-radius:24px;
    padding:35px;
    margin-top:35px;
    box-shadow:
    0 10px 28px rgba(0,0,0,.08);
    text-align:center;
    border:1px solid #dbeafe;
}

.solution-card:hover{
    transform:translateY(-3px);
    box-shadow:
    0 15px 35px rgba(0,0,0,.12);
}

.solution-title{
    font-size:34px;
    font-weight:700;
    text-align:center;
    color:#0f172a;
    margin-bottom:30px;
    font-family:
    'Playfair Display',serif;
}


.solution-text{
    font-size:20px;
    line-height:2;
    text-align:center;
    color:#243746;
    font-family:"Segoe UI", Arial, sans-serif;
}

.solution-card li{
    margin-bottom:18px;
    line-height:1.8;
}

.solution-card li strong{
    display:block;
    margin-bottom:6px;
    font-size:16px;
    color:#1a4f9c;
}

.solution-card li span{
    color:#555;
    font-size:15px;
}

.bilingual-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 40px;
    margin-top: 15px;
}

.language-panel li{
    ackground:white;
    border-radius:14px;
    padding:18px;
    margin-bottom:18px;
    box-shadow:0 4px 10px rgba(0,0,0,.05);
    line-height:1.8;
    font-size:16px;
}

.language-panel ul{
    list-style:none;
    padding-left:0;
    margin:0;
}

.arabic-panel ul{
    list-style:none;
    padding-right:0;
    margin:0;
}

.arabic-panel {
    direction: rtl;
    text-align: right;
}

.language-label{
    font-size:20px;
    font-weight:700;
    text-align:center;
    margin-bottom:20px;
    color:#0F4C81;
}

@media (max-width: 800px) {
    .bilingual-grid {
        grid-template-columns: 1fr;
    }
}

details{
    border-radius:18px;
    border:1px solid #dbeafe;
    background:white;
    box-shadow:0 8px 22px rgba(0,0,0,.08);
    margin-top:15px;
}

details summary{
    font-size:22px;
    font-weight:700;
    color:#0f4c5c;
    padding:18px;
    cursor:pointer;
    font-family:Georgia, serif;
}

details[open] summary{
    border-bottom:1px solid #E5E7EB;
}

"""