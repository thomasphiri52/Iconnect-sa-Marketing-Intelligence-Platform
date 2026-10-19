import os
import sys

# Ensure the project root is importable when Streamlit launches this file directly.
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from v13_customer_360 import render_v13_customer_360
from v12_collaboration import render_v12_collaboration
from v11_enterprise_operations import render_v11_operations
from v10_strategy_console import render_v10_strategy_console
from v9_realtime_command_centre import render_v9_realtime_command_centre
from v8_ai_decision_ui import render_v8_ai_decision_engine
from v7_api_integration_ui import render_v7_api_integration
from v6_data_platform_ui import render_v6_data_platform
from v5_security_ui import render_security_console
from enterprise_ai_automation import generate_signals, default_workflows, executive_brief, forecast, create_action

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import date

st.set_page_config(
    page_title="iConnect SA | Marketing Intelligence",
    page_icon="🔷",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Theme ----------
st.markdown("""
<style>
:root { --bg:#061225; --panel:#0b1b35; --panel2:#0d2342; --blue:#16a8ff; --purple:#7b3cff; --cyan:#18e0d0; }
.stApp { background: radial-gradient(circle at 70% 0%, #102c54 0%, #061225 45%, #030a16 100%); color:#f5f7fb; }
section[data-testid="stSidebar"] { background: linear-gradient(180deg,#041022,#07182f); border-right:1px solid #15375f; }
section[data-testid="stSidebar"] .stButton > button {
    width:100%; text-align:left; background:transparent; color:#d8e7fb; border:0;
    border-radius:10px; padding:10px 12px; margin:2px 0;
}
section[data-testid="stSidebar"] .stButton > button:hover { background:#123b75; color:white; }
div.stButton > button {
    border-radius:10px; border:1px solid #174c82; background:#0b2040; color:#eaf5ff;
}
div.stButton > button:hover { border-color:#19b8ff; background:#10345e; color:white; }
.card {
    background:linear-gradient(145deg,rgba(12,36,69,.95),rgba(6,20,39,.95));
    border:1px solid #16416d; border-radius:15px; padding:18px; min-height:125px;
    box-shadow:0 8px 30px rgba(0,0,0,.22);
}
.card h4 { margin:0; color:#b9cbe4; font-size:14px; }
.metric { font-size:30px; font-weight:800; margin:7px 0; }
.up { color:#20e0b1; font-weight:700; }
.small { color:#8ea8c8; font-size:12px; }
.section-title { font-size:22px; font-weight:800; margin:8px 0 15px; }
.badge { display:inline-block; padding:5px 9px; border-radius:99px; background:#12395f; color:#8fe7ff; font-size:12px; }
</style>
""", unsafe_allow_html=True)

# ---------- Demo data ----------
rng = np.random.default_rng(7)
days = pd.date_range("2025-04-01", periods=28)
channels = ["Social Media", "Search Ads", "Email", "Display"]

campaign_daily = pd.DataFrame({
    "Date": np.tile(days, len(channels)),
    "Channel": np.repeat(channels, len(days)),
})
campaign_daily["Revenue"] = np.concatenate([
    np.linspace(22000, 60000, 28) + rng.normal(0,2500,28),
    np.linspace(18000, 47000, 28) + rng.normal(0,2200,28),
    np.linspace(10000, 30000, 28) + rng.normal(0,1600,28),
    np.linspace(7000, 19000, 28) + rng.normal(0,1200,28),
])
campaign_daily["Leads"] = (campaign_daily["Revenue"] / rng.uniform(22,34,len(campaign_daily))).astype(int)
campaign_daily["Cost"] = campaign_daily["Revenue"] * rng.uniform(.12,.32,len(campaign_daily))
campaign_daily["Conversions"] = (campaign_daily["Leads"] * rng.uniform(.06,.16,len(campaign_daily))).astype(int)
campaign_daily["ROI"] = campaign_daily["Revenue"] / campaign_daily["Cost"]

campaigns = pd.DataFrame({
    "Campaign":["Spring Sale 2025","Brand Awareness","Email Nurture Series","Product Launch","Retargeting Campaign"],
    "Channel":["Social Media","Search Ads","Email","Display Ads","Social Media"],
    "Leads":[3482,2941,2156,1320,987],
    "Cost":[12450,18230,8620,11340,6540],
    "ROI":[8.4,6.7,5.9,4.2,3.8]
})
audience = pd.DataFrame({
    "Segment":["18–24","25–34","35–44","45–54","55+"],
    "Share":[22,34,24,14,6],
    "Conversion Rate":[6.2,9.8,8.1,5.4,3.2]
})
social = pd.DataFrame({
    "Network":["Instagram","LinkedIn","X","Facebook","TikTok"],
    "Engagements":[12400,8700,6200,4100,3800],
    "Growth":[32,21,17,12,9]
})

# ---------- Navigation ----------
pages = {
    "Dashboard":"Dashboard",
    "Command Centre":"Command Centre",
    "Campaigns":"Campaigns",
    "Audience Intelligence":"Audience Intelligence",
    "Market Insights":"Market Insights",
    "Competitor Analysis":"Competitor Analysis",
    "Content Performance":"Content Performance",
    "Social Media":"Social Media",
    "SEO & Search":"SEO & Search",
    "Paid Media":"Paid Media",
    "Email Marketing":"Email Marketing",
    "Attribution & ROI":"Attribution & ROI",
    "Reports":"Reports",
    "Automation":"Automation",
    "Data & AI":"Data & AI",
    "Data Integration Centre":"Data Integration Centre",
    "Intelligence Monitor":"Intelligence Monitor",
    "Opportunity Intelligence":"Opportunity Intelligence",
    "Alerts & Risk":"Alerts & Risk",
    "Executive Reports":"Executive Reports",
    "Enterprise Operations":"Enterprise Operations",
    "Collaboration Centre":"Collaboration Centre",
    "Customer 360":"Customer 360",
    "Settings":"Settings",
}

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

def go(page):
    st.session_state.page = page

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("## 🔷 iConnect SA")
    st.caption("MARKETING INTELLIGENCE PLATFORM")
    st.divider()
    for label in pages:
        if st.button(("🏠 " if label=="Dashboard" else "▸ ") + label, key="nav_"+label):
            go(label)

    st.divider()
    st.caption("QUICK ACTIONS")
    if st.button("＋ Create Campaign", key="quick_campaign"): go("Campaigns")
    if st.button("⇧ Upload Data", key="quick_upload"): go("Data & AI")
    if st.button("▤ Generate Report", key="quick_report"): go("Reports")
    if st.button("✦ AI Insights", key="quick_ai"): go("Data & AI")
    st.divider()
    st.markdown("### 👤 Thomas")
    st.caption("Marketing Director")
    st.caption("System Online • v1.0.0")

# ---------- Header ----------
c1,c2,c3 = st.columns([5,1,1])
with c1:
    st.markdown(f"# {st.session_state.page}")
    st.caption("iConnect SA • Marketing Intelligence • Data-driven growth")
with c2:
    st.button("🔔 3", key="notifications")
with c3:
    st.button("⚙ Settings", key="settings_top", on_click=lambda: go("Settings"))

# ---------- Screens ----------
def _render_dashboard_safely():
    try:
        dashboard()
    except Exception as exc:
        st.error("Dashboard display error")
        st.warning("The dashboard failed to render, but the application is still running.")
        with st.expander("Show technical details"):
            st.code(f"{type(exc).__name__}: {exc}")

def dashboard():
    st.markdown('<div class="section-title">Welcome back, Thomas 👋</div>', unsafe_allow_html=True)
    d1,d2 = st.columns([4,1])
    with d1:
        st.caption("Marketing intelligence overview — every interactive element opens a detailed screen.")
    with d2:
        st.date_input("Report date", value=date(2025,4,30), label_visibility="collapsed")

    metrics = [
        ("💰","Total Revenue","R 2.48M","+18.2%","Market revenue"),
        ("🎯","Marketing ROI","4.8x","+22.7%","ROI analysis"),
        ("👥","Total Leads","12,843","+34.5%","Lead intelligence"),
        ("🔻","Conversion Rate","6.7%","+2.3%","Conversion analysis"),
        ("💎","Customer Lifetime Value","R 4,320","+15.8%","Customer value"),
    ]
    cols = st.columns(5)
    for i,(icon,name,val,delta,target) in enumerate(metrics):
        with cols[i]:
            st.markdown(f'<div class="card"><h4>{icon} {name}</h4><div class="metric">{val}</div><div class="up">▲ {delta} <span class="small">vs previous month</span></div></div>', unsafe_allow_html=True)
            if st.button("Open details →", key=f"metric_{i}"):
                go({"Market revenue":"Campaigns","ROI analysis":"Attribution & ROI","Lead intelligence":"Audience Intelligence","Conversion analysis":"Campaigns","Customer value":"Audience Intelligence"}[target])
                st.rerun()

    st.markdown("###")
    left, mid, right = st.columns([1.7,1,1])
    with left:
        st.markdown("#### 📣 Campaign Performance")
        tab = st.radio("View", ["Revenue","Leads","Conversions"], horizontal=True, label_visibility="collapsed")
        y = tab
        fig = px.line(campaign_daily, x="Date", y=y, color="Channel", template="plotly_dark")
        fig.update_layout(height=320, margin=dict(l=10,r=10,t=10,b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
        if st.button("Open Campaign Intelligence →", key="open_campaign_chart"): go("Campaigns"); st.rerun()

    with mid:
        st.markdown("#### 🏆 Top Campaigns")
        st.dataframe(campaigns, hide_index=True, use_container_width=True, height=260)
        if st.button("View all campaigns →", key="open_campaigns"): go("Campaigns"); st.rerun()

    with right:
        st.markdown("#### 👥 Audience Intelligence")
        fig = px.pie(audience, names="Segment", values="Share", hole=.55, template="plotly_dark")
        fig.update_layout(height=260, margin=dict(l=5,r=5,t=5,b=5), paper_bgcolor="rgba(0,0,0,0)", showlegend=True)
        st.plotly_chart(fig, use_container_width=True)
        if st.button("Explore audiences →", key="open_audience"): go("Audience Intelligence"); st.rerun()

    a,b,c = st.columns(3)
    with a:
        st.markdown("#### 🔻 Marketing Funnel")
        funnel = pd.DataFrame({"Stage":["Awareness","Interest","Consideration","Conversion"],"Value":[100000,56320,28450,12843]})
        fig = px.funnel(funnel, x="Value", y="Stage", template="plotly_dark")
        fig.update_layout(height=300, margin=dict(l=5,r=5,t=5,b=5), paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
        if st.button("Open funnel analysis →", key="funnel"): go("Campaigns"); st.rerun()
    with b:
        st.markdown("#### 🧠 AI Marketing Insights")
        insights = [
            ("⚠️","Conversion rate declined 18% for mobile traffic."),
            ("🟢","25–34 segment shows the strongest conversion rate."),
            ("🔵","Competitor social activity increased this month."),
            ("🟣","Lead volume forecast indicates continued growth."),
        ]
        for i,(icon,msg) in enumerate(insights):
            if st.button(f"{icon} {msg}", key=f"insight_{i}"): go("Data & AI"); st.rerun()
    with c:
        st.markdown("#### 📰 Latest Activities")
        acts = ["Campaign performance updated","New lead captured","Report generated","Audience segment updated","Data sync completed"]
        for i,x in enumerate(acts):
            if st.button(f"• {x}", key=f"activity_{i}"): go("Reports" if "Report" in x else "Data & AI"); st.rerun()

def command_centre():
    """Executive Market Intelligence Command Centre."""
    st.markdown("## 🧭 Market Intelligence Command Centre")
    st.caption("Executive command view — market movement, opportunities, customer health, competitor signals and management attention.")

    # Executive controls
    c1, c2, c3, c4 = st.columns([1.3, 1.3, 1.3, 2.1])
    with c1:
        period = st.selectbox("Period", ["Current month", "Last 90 days", "Year to date"], key="cc_period")
    with c2:
        region = st.selectbox("Market", ["South Africa", "Gauteng", "Western Cape", "KwaZulu-Natal"], key="cc_region")
    with c3:
        lens = st.selectbox("Intelligence lens", ["Executive", "Growth", "Risk", "Competition"], key="cc_lens")
    with c4:
        st.markdown('<div class="badge">● Intelligence system online</div>', unsafe_allow_html=True)

    # Executive KPI strip
    kpis = [
        ("🌍 Market Growth", "+8.6%", "trend improving"),
        ("🎯 Opportunities", "27", "12 newly detected"),
        ("⚠️ Signals to Review", "8", "3 high priority"),
        ("👥 Customer Health", "91%", "stable"),
        ("🏢 Competitor Activity", "14", "5 new movements"),
        ("📊 Intelligence Confidence", "94%", "data quality"),
    ]
    cols = st.columns(6)
    for i, (name, val, sub) in enumerate(kpis):
        with cols[i]:
            st.markdown(f'<div class="card"><h4>{name}</h4><div class="metric">{val}</div><div class="small">{sub}</div></div>', unsafe_allow_html=True)

    st.markdown("###")
    # Market pulse + risk heatmap
    left, right = st.columns([1.65, 1])
    with left:
        st.markdown("### 📈 Market Pulse")
        trend = pd.DataFrame({
            "Month": pd.date_range("2025-01-01", periods=8, freq="MS"),
            "Market Demand": [72, 76, 79, 83, 88, 94, 97, 101],
            "Customer Interest": [68, 71, 75, 78, 84, 90, 93, 98],
            "Competitor Activity": [52, 58, 61, 67, 70, 76, 82, 86],
        })
        long = trend.melt("Month", var_name="Signal", value_name="Index")
        fig = px.line(long, x="Month", y="Index", color="Signal", markers=True, template="plotly_dark")
        fig.update_layout(height=355, margin=dict(l=10,r=10,t=10,b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", legend_title_text="")
        st.plotly_chart(fig, use_container_width=True)
    with right:
        st.markdown("### ⚠️ Intelligence Risk Matrix")
        risk = pd.DataFrame({
            "Area": ["Customer", "Competition", "Acquisition", "Conversion", "Data", "Market"],
            "Impact": [3, 4, 3, 4, 2, 2],
            "Velocity": [2, 4, 3, 3, 2, 1],
            "Status": ["Monitor", "Review", "Monitor", "Review", "Monitor", "Normal"],
        })
        fig = px.scatter(risk, x="Velocity", y="Impact", text="Area", size=[18,24,20,23,14,12],
                         hover_data=["Status"], template="plotly_dark")
        fig.update_traces(textposition="top center")
        fig.update_layout(height=355, margin=dict(l=10,r=10,t=10,b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          xaxis_title="Signal velocity", yaxis_title="Business impact")
        st.plotly_chart(fig, use_container_width=True)

    # South Africa geographic intelligence
    st.markdown("### 🇿🇦 South Africa Geographic Intelligence")
    geo = pd.DataFrame({
        "Province":["Gauteng","Western Cape","KwaZulu-Natal","Eastern Cape","Limpopo","Mpumalanga","North West","Free State","Northern Cape"],
        "Latitude":[-26.27,-33.92,-29.86,-32.30,-23.40,-25.57,-26.66,-29.12,-29.05],
        "Longitude":[28.11,18.42,30.99,25.62,29.42,30.53,25.31,26.22,21.86],
        "Demand Index":[100,91,84,66,61,63,58,52,44],
        "Opportunity":[92,78,73,69,66,62,58,49,41],
        "Customers":[42000,31000,26000,14500,12000,10800,9200,7100,4200]
    })
    gm1, gm2 = st.columns([1.7, 1])
    with gm1:
        fig = px.scatter_geo(geo, lat="Latitude", lon="Longitude", size="Customers", color="Opportunity", text="Province",
                             scope="africa", projection="natural earth", template="plotly_dark",
                             hover_data=["Demand Index","Opportunity","Customers"])
        fig.update_traces(textposition="top center")
        fig.update_geos(showland=True, landcolor="#0b1b35", showcountries=True, countrycolor="#31577f", showocean=True, oceancolor="#061225")
        fig.update_layout(height=410, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
    with gm2:
        st.markdown("#### Regional opportunity")
        st.dataframe(geo[["Province","Demand Index","Opportunity"]].sort_values("Opportunity", ascending=False), hide_index=True, use_container_width=True, height=360)
        if st.button("Open geographic market insights →", key="cc_geo"): go("Market Insights"); st.rerun()

    # Opportunity radar and competitor timeline
    a, b = st.columns([1, 1.4])
    with a:
        st.markdown("### 🎯 Opportunity Radar")
        opp = pd.DataFrame({
            "Opportunity":["25–34 segment expansion","Regional growth","Search demand","Cross-sell potential","Retention programme"],
            "Potential":[92,84,79,73,68],
            "Evidence":["High conversion","Demand growth","Search trend","Customer value","Churn signal"]
        })
        fig = px.bar(opp.sort_values("Potential"), x="Potential", y="Opportunity", orientation="h", text="Potential", template="plotly_dark")
        fig.update_layout(height=300, margin=dict(l=10,r=10,t=10,b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
        if st.button("Explore opportunities →", key="cc_opportunities"): go("Market Insights"); st.rerun()
    with b:
        st.markdown("### 🏢 Competitor Movement Timeline")
        events = pd.DataFrame({
            "Date": pd.to_datetime(["2025-03-05","2025-03-14","2025-03-23","2025-04-02","2025-04-11","2025-04-22"]),
            "Competitor":["Competitor A","Competitor B","Competitor A","Competitor C","Competitor B","Competitor A"],
            "Movement":["New campaign","Pricing update","Social push","Product message","Content increase","Retargeting activity"],
            "Signal":["High","Medium","High","Medium","High","High"]
        })
        fig = px.scatter(events, x="Date", y="Competitor", color="Signal", size=[18,12,20,13,17,22], hover_data=["Movement"], template="plotly_dark")
        fig.update_layout(height=300, margin=dict(l=10,r=10,t=10,b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
        if st.button("Open competitor intelligence →", key="cc_competitors"): go("Competitor Analysis"); st.rerun()

    # Customer health + executive attention
    c, d = st.columns([1, 1])
    with c:
        st.markdown("### 👥 Customer 360 Health")
        customer_health = pd.DataFrame({
            "Metric":["Retention","Churn","CLV","Engagement","Repeat purchase"],
            "Current":[91,9,4320,78,64],
            "Target":[90,8,4000,75,60]
        })
        fig = go.Figure()
        fig.add_trace(go.Bar(name="Current", x=customer_health["Metric"], y=customer_health["Current"]))
        fig.add_trace(go.Bar(name="Target", x=customer_health["Metric"], y=customer_health["Target"]))
        fig.update_layout(barmode="group", height=300, template="plotly_dark", margin=dict(l=10,r=10,t=10,b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
        if st.button("Open customer intelligence →", key="cc_customers"): go("Audience Intelligence"); st.rerun()
    with d:
        st.markdown("### 🚨 Management Attention")
        attention = [
            ("🔴", "Competitor advertising activity increased in a key segment."),
            ("🟠", "Customer acquisition cost is trending upward."),
            ("🟠", "Conversion performance requires review in one channel."),
            ("🟢", "Demand is increasing in an identified market segment."),
            ("🔵", "Data quality remains above the operating threshold."),
        ]
        for i, (icon, msg) in enumerate(attention):
            if st.button(f"{icon} {msg}", key=f"cc_attention_{i}"):
                go("Competitor Analysis" if i == 0 else ("Campaigns" if i in [1,2] else "Market Insights")); st.rerun()

    # Executive brief
    st.markdown("### 🧠 Executive Intelligence Brief")
    st.markdown('<div class="card"><h4>Current intelligence position</h4><div style="font-size:16px;line-height:1.7;margin-top:8px">Market demand is trending upward while competitor activity is also increasing. The command centre has identified several growth opportunities and a small set of signals requiring management review. These observations are based on the demonstration dataset and should be validated against authorized iConnect SA data before operational decisions.</div></div>', unsafe_allow_html=True)
    st.markdown("###")
    x, y, z = st.columns(3)
    with x:
        if st.button("📄 Generate Executive Brief", key="cc_report"): go("Reports"); st.rerun()
    with y:
        if st.button("✦ Open AI Intelligence", key="cc_ai"): go("Data & AI"); st.rerun()
    with z:
        if st.button("📊 Open Strategic Dashboard", key="cc_strategy"): go("Dashboard"); st.rerun()

def detail_page(title, description, kpis, chart_df=None, x=None, y=None, color=None):
    st.markdown(f"## {title}")
    st.caption(description)
    cols = st.columns(len(kpis))
    for i,(name,val,delta) in enumerate(kpis):
        with cols[i]:
            st.markdown(f'<div class="card"><h4>{name}</h4><div class="metric">{val}</div><div class="up">▲ {delta}</div></div>', unsafe_allow_html=True)
    st.markdown("###")
    if chart_df is not None:
        fig = px.line(chart_df, x=x, y=y, color=color, markers=True, template="plotly_dark")
        fig.update_layout(height=380, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("### Detailed intelligence")
    st.info("This screen is connected to the same navigation system. In production, this section can connect to approved iConnect SA data sources, APIs or a data warehouse.")
    st.dataframe((chart_df if chart_df is not None else campaigns), hide_index=True, use_container_width=True)
    if st.button("← Back to Dashboard", key="back_"+title):
        go("Dashboard"); st.rerun()

def campaigns_page():
    detail_page("Campaign Intelligence","Track campaign spend, leads, conversions, revenue and ROI.",[
        ("Active Campaigns","24","+12%"),("Leads","12,843","+34.5%"),("Conversions","1,284","+21.2%"),("Spend","R 68.4K","+9.1%")
    ], campaign_daily.groupby(["Date","Channel"],as_index=False)["Revenue"].sum(), "Date","Revenue","Channel")

def audience_page():
    st.markdown("## Audience Intelligence")
    st.caption("Understand who converts, where they come from and how segments change.")
    st.dataframe(audience, hide_index=True, use_container_width=True)
    fig=px.bar(audience,x="Segment",y="Conversion Rate",template="plotly_dark")
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig,use_container_width=True)

def generic(title, description):
    detail_page(title,description,[("Reach","248K","+12.5%"),("Engagement","34.2K","+18.4%"),("Opportunities","1,842","+11.7%"),("Efficiency","4.8x","+22.7%")])


# ---------- V2 Intelligence Engine ----------
def uploaded_or_demo_data():
    if "uploaded_data" not in st.session_state:
        st.session_state.uploaded_data = None
    return st.session_state.uploaded_data if st.session_state.uploaded_data is not None else campaign_daily.copy()

def score_opportunities(df):
    base = pd.DataFrame({
        "Opportunity": [
            "Gauteng growth expansion", "25–34 high-conversion segment", "Search demand capture",
            "Customer retention programme", "Cross-sell existing customers", "Western Cape market expansion"
        ],
        "Demand": [94, 91, 88, 76, 82, 79],
        "Growth": [92, 89, 86, 71, 78, 81],
        "Customer Fit": [90, 96, 84, 88, 93, 77],
        "Competition": [64, 58, 61, 72, 69, 66],
        "Revenue Potential": [95, 92, 89, 80, 91, 82],
    })
    base["Opportunity Score"] = (base["Demand"]*.22 + base["Growth"]*.20 + base["Customer Fit"]*.18 + (100-base["Competition"])*.15 + base["Revenue Potential"]*.25).round(0).astype(int)
    base["Priority"] = pd.cut(base["Opportunity Score"], bins=[0,59,74,89,100], labels=["Low","Medium","High","Critical"], include_lowest=True)
    return base.sort_values("Opportunity Score", ascending=False)

def opportunity_page():
    st.markdown("## 🎯 Opportunity Intelligence")
    st.caption("Rank growth opportunities using demand, growth, customer fit, competitive pressure and revenue potential.")
    opp=score_opportunities(uploaded_or_demo_data())
    c1,c2,c3,c4=st.columns(4)
    for col,(name,val,sub) in zip([c1,c2,c3,c4],[
        ("Top Opportunity",opp.iloc[0]["Opportunity"],f"Score {opp.iloc[0]['Opportunity Score']}"),
        ("Critical",int((opp["Priority"]=="Critical").sum()),"immediate review"),
        ("High Priority",int((opp["Priority"]=="High").sum()),"growth actions"),
        ("Avg Score",f"{opp['Opportunity Score'].mean():.0f}/100","portfolio strength")]):
        with col: st.markdown(f'<div class="card"><h4>{name}</h4><div class="metric">{val}</div><div class="small">{sub}</div></div>',unsafe_allow_html=True)
    st.markdown("### Opportunity ranking")
    fig=px.bar(opp.sort_values("Opportunity Score"),x="Opportunity Score",y="Opportunity",color="Priority",orientation="h",text="Opportunity Score",template="plotly_dark")
    fig.update_layout(height=390,paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",margin=dict(l=10,r=10,t=10,b=10))
    st.plotly_chart(fig,use_container_width=True)
    st.dataframe(opp,hide_index=True,use_container_width=True)

def alerts_page():
    st.markdown("## 🚨 Alerts & Risk Centre")
    st.caption("Prioritise signals that require management attention.")
    alerts=pd.DataFrame({
        "Severity":["Critical","High","High","Medium","Medium","Low"],
        "Signal":["Competitor activity spike","Acquisition cost rising","Mobile conversion decline","Search demand increasing","Customer churn signal","Data freshness warning"],
        "Impact":["High","High","High","Medium","Medium","Low"],
        "Owner":["Strategy","Marketing","Growth","Marketing","Customer","Data"],
        "Status":["Open","Open","Open","Monitoring","Monitoring","Resolved"]
    })
    c1,c2,c3=st.columns(3)
    with c1: st.metric("Open alerts",int((alerts.Status=="Open").sum()))
    with c2: st.metric("High/Critical",int(alerts.Severity.isin(["High","Critical"]).sum()))
    with c3: st.metric("Monitoring",int((alerts.Status=="Monitoring").sum()))
    st.dataframe(alerts,hide_index=True,use_container_width=True)
    st.markdown("### Recommended response")
    st.info("Review the three open high-impact signals first. Connect approved live data sources before using these demo alerts for operational decisions.")

def executive_reports_page():
    st.markdown("## 📄 Executive Intelligence Reports")
    st.caption("Prepare a management-ready intelligence brief from the current platform signals.")
    opp=score_opportunities(uploaded_or_demo_data())
    st.markdown('<div class="card"><h4>Executive brief</h4><div style="font-size:16px;line-height:1.7;margin-top:8px">Market demand is positive, with the strongest current opportunity centred on high-conversion customer segments and regional expansion. Competitive activity remains an area to monitor. The opportunity engine recommends prioritising the highest-scoring initiatives and validating them against approved live business data.</div></div>',unsafe_allow_html=True)
    st.markdown("### Top recommendations")
    for i,row in opp.head(3).iterrows():
        st.success(f"{row['Priority']}: {row['Opportunity']} — score {row['Opportunity Score']}/100")
    st.download_button("⬇ Download opportunity table (CSV)",opp.to_csv(index=False),"iconnect_opportunity_intelligence.csv","text/csv")

def data_ai_page():
    st.markdown("## 🧠 Data & AI Intelligence")
    st.caption("Upload approved business data, validate it, and turn it into scored intelligence.")
    uploaded=st.file_uploader("Upload CSV data",type=["csv"],help="Recommended columns include Date, Channel, Revenue, Leads, Cost and Conversions.")
    if uploaded is not None:
        try:
            df=pd.read_csv(uploaded)
            st.session_state.uploaded_data=df
            st.success(f"Loaded {len(df):,} rows successfully.")
        except Exception as e:
            st.error(f"Could not read the CSV: {e}")
    df=uploaded_or_demo_data()
    a,b,c,d=st.columns(4)
    a.metric("Rows",f"{len(df):,}")
    b.metric("Columns",f"{len(df.columns):,}")
    b2=df.select_dtypes(include=np.number)
    c.metric("Numeric fields",f"{len(b2.columns):,}")
    d.metric("Data status","Uploaded" if st.session_state.get("uploaded_data") is not None else "Demo")
    st.markdown("### Data preview")
    st.dataframe(df.head(20),hide_index=True,use_container_width=True)
    st.markdown("### AI Analyst")
    question=st.selectbox("Ask an intelligence question",[
        "What should management prioritise?","Which opportunity looks strongest?","Where is risk concentrated?","What should we investigate next?"
    ])
    if st.button("✦ Analyse",key="ai_analyse"):
        opp=score_opportunities(df)
        if question=="Which opportunity looks strongest?":
            st.success(f"The strongest identified opportunity is {opp.iloc[0]['Opportunity']} with a score of {opp.iloc[0]['Opportunity Score']}/100.")
        elif question=="Where is risk concentrated?":
            st.warning("Risk is currently concentrated around competitive activity, acquisition efficiency and mobile conversion performance in the demonstration intelligence layer.")
        elif question=="What should we investigate next?":
            st.info("Validate the highest-scoring opportunity with customer, regional and competitor data before committing budget.")
        else:
            st.success("Prioritise the top opportunity, review open high-impact alerts, and validate the underlying data quality before taking action.")


def integration_page():
    st.markdown("## 🔌 Data Integration Centre")
    st.caption("Enterprise-ready data source management. Demo connectors are simulated until credentials/API endpoints are configured.")
    connectors = pd.DataFrame({
        "Source":["CSV / Excel","CRM","Google Analytics","Meta Ads","Google Ads","SQL Database","REST API"],
        "Category":["Files","Customer","Web Analytics","Advertising","Advertising","Database","Custom"],
        "Status":["Connected","Not connected","Connected","Not connected","Not connected","Not connected","Ready"],
        "Last Sync":["Today 06:20","—","Today 05:55","—","—","—","—"],
        "Records":["12,843","—","248,120","—","—","—","—"]
    })
    a,b,c,d=st.columns(4)
    a.metric("Connected sources", int((connectors.Status=="Connected").sum()))
    b.metric("Ready to configure", int((connectors.Status=="Ready").sum()))
    c.metric("Records available", "260,963")
    d.metric("Pipeline health", "98%")
    st.dataframe(connectors, hide_index=True, use_container_width=True)
    st.markdown("### Add a data source")
    source=st.selectbox("Connector", ["CSV / Excel","CRM","Google Analytics","Meta Ads","Google Ads","SQL Database","REST API"])
    if st.button("＋ Configure connector", key="configure_connector"):
        st.info(f"{source} connector configuration is ready for credentials, endpoint and refresh schedule. No external connection is made in demo mode.")
    st.markdown("### Refresh policy")
    r1,r2,r3=st.columns(3)
    r1.selectbox("Refresh frequency", ["Manual","Hourly","Every 6 hours","Daily"], key="refresh_frequency")
    r2.selectbox("Validation", ["Strict","Standard","Advisory"], key="validation_mode")
    r3.toggle("Auto-refresh enabled", value=False, key="auto_refresh")

def monitor_page():
    st.markdown("## 📡 Intelligence Monitor")
    st.caption("Continuous monitoring layer for anomalies, market movements and data quality signals.")
    monitor = pd.DataFrame({
        "Signal":["Market demand","Conversion rate","Competitor activity","Lead volume","Data freshness","Campaign ROI"],
        "Current":[101,6.7,86,12843,98,4.8],
        "Baseline":[94,7.1,74,11020,95,4.2],
        "Change %":[7.4,-5.6,16.2,16.6,3.2,14.3],
        "Status":["Positive","Watch","Alert","Positive","Healthy","Positive"]
    })
    st.dataframe(monitor, hide_index=True, use_container_width=True)
    st.markdown("### Automated detection")
    anomalies=[]
    for _,r in monitor.iterrows():
        if abs(r["Change %"]) >= 15:
            anomalies.append(f"{r['Signal']}: {r['Change %']:+.1f}% movement detected")
    if anomalies:
        for x in anomalies: st.warning(x)
    else: st.success("No material anomalies detected.")
    st.markdown("### Pipeline timeline")
    timeline=pd.DataFrame({"Stage":["Source check","Validation","Transformation","Scoring","Alert evaluation","Dashboard refresh"],"Status":["Complete","Complete","Complete","Complete","Complete","Complete"],"Duration (s)":[2,3,4,2,1,2]})
    st.dataframe(timeline, hide_index=True, use_container_width=True)

# ---------- Routing ----------
p=st.session_state.page
if p=="Dashboard": _render_dashboard_safely()
elif p=="Command Centre": command_centre()
elif p=="Campaigns": campaigns_page()
elif p=="Audience Intelligence": audience_page()
elif p=="Market Insights": generic(p,"Monitor market demand, trends, customer signals and growth opportunities.")
elif p=="Competitor Analysis": generic(p,"Compare competitor activity, messaging, channel presence and market movements.")
elif p=="Content Performance": generic(p,"Measure content reach, engagement, conversion contribution and lifecycle performance.")
elif p=="Social Media": 
    detail_page(p,"Track social engagement and channel growth.",[("Engagements","35.2K","+21%"),("Followers","248K","+12%"),("Reach","1.2M","+18%"),("Engagement Rate","6.7%","+4%")])
elif p=="SEO & Search": generic(p,"Monitor organic visibility, search demand, keywords, traffic and conversions.")
elif p=="Paid Media": generic(p,"Track paid media spend, CPC, CPA, ROAS and campaign efficiency.")
elif p=="Email Marketing": generic(p,"Track opens, clicks, conversions, unsubscribe rates and email revenue.")
elif p=="Attribution & ROI": generic(p,"Connect marketing activity to revenue and evaluate channel contribution.")
elif p=="Reports": generic(p,"Create management reports, export data and schedule recurring intelligence reports.")
elif p=="Automation": generic(p,"Build automated alerts, data refreshes, campaign workflows and reporting tasks.")
elif p=="Data & AI": data_ai_page()
elif p=="Data Integration Centre": integration_page()
elif p=="Intelligence Monitor": monitor_page()
elif p=="Opportunity Intelligence": opportunity_page()
elif p=="Alerts & Risk": alerts_page()
elif p=="Executive Reports": executive_reports_page()
elif p=="Enterprise Operations": render_v11_operations(st)
elif p=="Collaboration Centre": render_v12_collaboration(st)
elif p=="Customer 360": render_v13_customer_360(st)
elif p=="Settings": generic(p,"Manage platform preferences, profile, integrations, access and system configuration.")

st.markdown("---")
st.caption("iConnect SA • Enterprise Market Intelligence Platform • V13 • Demo data shown until approved live connectors are configured")


# --- AI + AUTOMATION V4 extension ---
def render_v4_ai_automation(st):
    st.markdown("## 🧠 AI + Automation V4")
    st.caption("Predictive signals, transparent forecasting, workflow automation and action tracking.")

    metrics = {
        "conversion_rate": st.number_input("Conversion rate (%)", 0.0, 100.0, 2.8, 0.1),
        "market_growth": st.number_input("Market growth (%)", -100.0, 200.0, 12.5, 0.5),
        "competitor_activity": st.slider("Competitor activity index", 0, 100, 74),
        "churn_risk": st.number_input("Churn risk (%)", 0.0, 100.0, 13.0, 0.5),
    }

    signals = generate_signals(metrics)
    st.markdown("### Intelligence Signals")
    for s in signals:
        st.info(f"**{s['severity']} — {s['title']}** · Score {s['score']}/100\n\n{s['evidence']}\n\n**Action:** {s['recommendation']}")

    st.markdown("### Workflow Automation")
    for w in default_workflows():
        st.write(f"**{w['name']}** — IF {w['trigger']} {w['condition']} → THEN {w['action']}")

    st.markdown("### Executive Brief")
    if st.button("Generate Executive Brief"):
        st.json(executive_brief(metrics))


# V5 entry point: call render_security_console(st) from the Admin/Security page.


# V6 Enterprise Data Platform
# The full UI is exposed here so it can be wired into the app's navigation.
def render_v6_page():
    render_v6_data_platform(st)


# V7 Enterprise API & Integration Hub
def render_v7_page():
    render_v7_api_integration(st)


# V8 AI Decision & Intelligence Engine
def render_v8_page():
    render_v8_ai_decision_engine(st)


# V9 Real-Time Intelligence Command Centre
def render_v9_page():
    render_v9_realtime_command_centre(st)


# V10 Executive Strategy & Scenario Simulator
def render_v10_page():
    render_v10_strategy_console(st)
