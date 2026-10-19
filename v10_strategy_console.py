import pandas as pd
import streamlit as st
from strategy_simulator import scenario_pack, expansion_model

def render_v10_strategy_console(st_module=st):
    st_module.markdown("## 🎯 Executive Strategy & Scenario Simulator")
    st_module.caption("Model growth, investment, competitive pressure and South African market expansion before committing capital.")

    a,b,c = st_module.columns(3)
    base_revenue = a.number_input("Current annual revenue (R)", min_value=0.0, value=10000000.0, step=500000.0)
    margin = b.slider("Current operating margin %", 1.0, 60.0, 22.0)
    investment = c.number_input("Scenario investment (R)", min_value=0.0, value=1500000.0, step=100000.0)

    scenarios = scenario_pack(base_revenue, margin, investment)

    st_module.markdown("### Executive Scenario Board")
    df = pd.DataFrame([vars(x) for x in scenarios])
    st_module.dataframe(
        df[["name","market_growth","revenue_growth","customer_growth",
            "competitor_pressure","investment","projected_revenue",
            "projected_profit","roi","recommendation"]],
        use_container_width=True, hide_index=True
    )

    best = max(scenarios, key=lambda x: x.roi)
    c1,c2,c3 = st_module.columns(3)
    c1.metric("Best Projected Revenue", f"R{best.projected_revenue:,.0f}")
    c2.metric("Best Projected Profit", f"R{best.projected_profit:,.0f}")
    c3.metric("Best ROI", f"{best.roi:.1f}%")

    st_module.markdown("### Revenue Scenario")
    chart = df.set_index("name")[["projected_revenue","projected_profit"]]
    st_module.bar_chart(chart)

    st_module.info(best.recommendation)

    st_module.divider()
    st_module.markdown("### 🇿🇦 Provincial Expansion Simulator")
    p1,p2,p3,p4 = st_module.columns(4)
    province = p1.selectbox("Province", ["Gauteng","Western Cape","KwaZulu-Natal","Eastern Cape","Limpopo","Mpumalanga"])
    market = p2.slider("Market potential %", 0, 40, 18)
    risk = p3.slider("Execution risk %", 0, 100, 30)
    expand_investment = p4.number_input("Expansion investment (R)", min_value=0.0, value=800000.0, step=50000.0)

    result = expansion_model(province, base_revenue, expand_investment, market, risk)
    r1,r2,r3 = st_module.columns(3)
    r1.metric("Projected Revenue", f"R{result['projected_revenue']:,.0f}")
    r2.metric("Projected Profit", f"R{result['projected_profit']:,.0f}")
    r3.metric("Expansion ROI", f"{result['roi']:.1f}%")

    st_module.json(result)

    st_module.markdown("### Board Decision")
    decision = st_module.selectbox(
        "Strategic decision",
        ["Proceed", "Proceed with pilot", "Hold", "Reject / redesign"]
    )
    if st_module.button("Generate Board Recommendation", type="primary"):
        st_module.success(
            f"Recommended decision: **{decision}**. "
            f"Use the scenario assumptions and ROI above as the documented decision baseline."
        )
