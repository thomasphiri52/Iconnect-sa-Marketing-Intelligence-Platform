import pandas as pd
import streamlit as st
from realtime_intelligence import generate_live_signals, kpis, action_queue

def render_v9_realtime_command_centre(st_module=st):
    st_module.markdown("## 📡 Real-Time Intelligence Command Centre")
    st_module.caption("Live market, competitor, customer, revenue and risk monitoring.")

    refresh = st_module.checkbox("Auto-refresh simulation", value=False)
    seed = None if refresh else 42
    signals = generate_live_signals(18, seed=seed)
    metrics = kpis(signals)

    c1, c2, c3, c4, c5 = st_module.columns(5)
    c1.metric("Live Signals", metrics["live_signals"])
    c2.metric("High Priority", metrics["high_priority"])
    c3.metric("Medium", metrics["medium_priority"])
    c4.metric("Avg Score", metrics["avg_signal_score"])
    c5.metric("Opportunities", metrics["opportunities"])

    st_module.divider()

    tab1, tab2, tab3 = st_module.tabs(["Live Feed", "Regional Intelligence", "Action Queue"])

    with tab1:
        df = pd.DataFrame([vars(s) for s in signals])
        st_module.dataframe(
            df[["timestamp","region","category","title","value","severity","status"]],
            use_container_width=True, hide_index=True
        )
        st_module.markdown("### Signal Distribution")
        dist = df.groupby("category").size().sort_values(ascending=False)
        st_module.bar_chart(dist)

    with tab2:
        regional = df.groupby("region").agg(
            signals=("value","count"),
            avg_score=("value","mean")
        ).reset_index()
        regional["avg_score"] = regional["avg_score"].round(1)
        st_module.dataframe(regional, use_container_width=True, hide_index=True)
        st_module.markdown("### Regional Signal Score")
        st_module.bar_chart(regional.set_index("region")["avg_score"])

    with tab3:
        actions = action_queue(signals)
        if actions:
            st_module.dataframe(
                pd.DataFrame(actions),
                use_container_width=True, hide_index=True
            )
        else:
            st_module.success("No urgent actions currently queued.")

    if refresh:
        st_module.info("Auto-refresh simulation is enabled. In production, connect this to scheduled ingestion, WebSockets or streaming infrastructure.")
        st_module.button("Refresh Live Feed")
