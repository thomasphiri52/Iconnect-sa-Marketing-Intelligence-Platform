import pandas as pd
import streamlit as st
from ai_decision_engine import generate_signals, executive_brief, forecast

def render_v8_ai_decision_engine(st_module=st):
    st_module.markdown("## 🧠 AI Decision & Intelligence Engine")
    st_module.caption("Predictive scoring, threat detection, churn risk, forecasting and executive recommendations.")

    with st_module.expander("Intelligence Inputs", expanded=True):
        a,b,c = st_module.columns(3)
        demand = a.slider("Market demand", 0, 100, 82)
        growth = b.slider("Market growth %", 0.0, 15.0, 8.5)
        customer_fit = c.slider("Customer fit", 0, 100, 88)
        d,e,f = st_module.columns(3)
        competition = d.slider("Competition", 0, 100, 38)
        revenue = e.slider("Revenue potential", 0, 100, 84)
        competitor_activity = f.slider("Competitor activity", 0, 100, 64)
        g,h,i = st_module.columns(3)
        competitor_momentum = g.slider("Competitor momentum", 0, 100, 58)
        pricing_pressure = h.slider("Pricing pressure", 0, 100, 42)
        usage_drop = i.slider("Usage drop", 0, 100, 22)
        support_pressure = st_module.slider("Support pressure", 0, 100, 28)
        payment_risk = st_module.slider("Payment risk", 0, 100, 18)

    metrics = {
        "demand": demand, "growth": growth, "customer_fit": customer_fit,
        "competition": competition, "revenue_potential": revenue,
        "competitor_activity": competitor_activity,
        "competitor_momentum": competitor_momentum,
        "pricing_pressure": pricing_pressure,
        "usage_drop": usage_drop, "support_pressure": support_pressure,
        "payment_risk": payment_risk
    }
    signals = generate_signals(metrics)

    st_module.divider()
    st_module.markdown("### Intelligence Signals")
    df = pd.DataFrame([vars(s) for s in signals])
    st_module.dataframe(
        df[["title","category","severity","score","recommendation","rationale"]],
        use_container_width=True, hide_index=True
    )

    st_module.markdown("### Predictive Forecast")
    history = st_module.text_input(
        "Historical values (comma separated)",
        "52, 56, 61, 67, 72"
    )
    try:
        values = [float(x.strip()) for x in history.split(",") if x.strip()]
        predicted = forecast(values, 4)
        st_module.write({"forecast_periods": predicted})
        if predicted:
            st_module.line_chart(pd.DataFrame({"Historical": values + [None]*4, "Forecast": [None]*len(values) + predicted}))
    except ValueError:
        st_module.warning("Enter numeric values separated by commas.")

    if st_module.button("Generate Executive AI Brief", type="primary"):
        st_module.text_area("Executive Brief", executive_brief(signals), height=280)
