
import pandas as pd
import streamlit as st
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta

@dataclass
class Workflow:
    name: str
    owner: str
    trigger: str
    priority: str
    sla_hours: int
    status: str = "Active"

@dataclass
class Action:
    title: str
    owner: str
    priority: str
    due: str
    status: str
    source: str

def default_workflows():
    return [
        Workflow("High-Priority Market Alert", "Intelligence Team", "Signal score >= 85", "Critical", 4),
        Workflow("Opportunity Qualification", "Growth Team", "Opportunity score >= 80", "High", 24),
        Workflow("Competitor Escalation", "Strategy Team", "Competitor threat >= 75", "High", 12),
        Workflow("Data Quality Review", "Data Team", "Quality score < 90", "Medium", 24),
        Workflow("Executive Weekly Brief", "Executive Office", "Every Monday 07:00", "Medium", 48),
    ]

def default_actions():
    return [
        Action("Review high-priority competitor movement", "Strategy Team", "Critical", "Today 10:00", "Open", "Competitor Intelligence"),
        Action("Validate Gauteng growth opportunity", "Growth Team", "High", "Today 16:00", "In Progress", "Opportunity Engine"),
        Action("Resolve CRM data freshness warning", "Data Team", "Medium", "Tomorrow 09:00", "Open", "Data Integration"),
        Action("Approve executive market report", "Executive Office", "Medium", "Tomorrow 12:00", "Pending", "Reporting"),
        Action("Review mobile conversion anomaly", "Marketing Team", "High", "Today 14:00", "Open", "Intelligence Monitor"),
    ]

def render_v11_operations(st):
    st.markdown("## ⚙️ Enterprise Operations & Automation")
    st.caption("Convert intelligence into governed actions, workflows, SLAs and measurable execution.")

    workflows = default_workflows()
    actions = default_actions()

    k1,k2,k3,k4,k5 = st.columns(5)
    k1.metric("Active Workflows", len([w for w in workflows if w.status == "Active"]))
    k2.metric("Open Actions", len([a for a in actions if a.status in ("Open","In Progress","Pending")]))
    k3.metric("Critical Actions", len([a for a in actions if a.priority == "Critical"]))
    k4.metric("SLA Compliance", "94%")
    k5.metric("Automation Rate", "78%")

    st.markdown("### 🧭 Operations Control Tower")
    tab1, tab2, tab3, tab4 = st.tabs(["Action Queue", "Workflows", "SLA Monitor", "Execution Analytics"])

    with tab1:
        df = pd.DataFrame([asdict(a) for a in actions])
        st.dataframe(df, hide_index=True, use_container_width=True)
        selected = st.selectbox("Select action", df["title"].tolist(), key="v11_action")
        c1,c2,c3 = st.columns(3)
        with c1:
            if st.button("▶ Start Action", key="v11_start"):
                st.success(f"Started: {selected}")
        with c2:
            if st.button("✓ Complete Action", key="v11_complete"):
                st.success(f"Completed: {selected}")
        with c3:
            if st.button("↗ Escalate", key="v11_escalate"):
                st.warning(f"Escalated: {selected}")

    with tab2:
        wdf = pd.DataFrame([asdict(w) for w in workflows])
        st.dataframe(wdf, hide_index=True, use_container_width=True)
        st.markdown("#### Create automation")
        c1,c2,c3 = st.columns(3)
        with c1:
            trigger = st.selectbox("Trigger", [
                "Market signal detected", "Opportunity score threshold",
                "Competitor threat threshold", "Data quality threshold",
                "Scheduled time"
            ], key="v11_trigger")
        with c2:
            threshold = st.slider("Threshold", 0, 100, 80, key="v11_threshold")
        with c3:
            owner = st.selectbox("Owner", ["Intelligence Team","Growth Team","Strategy Team","Data Team","Executive Office"], key="v11_owner")
        if st.button("＋ Create Workflow", key="v11_create"):
            st.success(f"Workflow created: {trigger} → {owner} at threshold {threshold}.")

    with tab3:
        sla = pd.DataFrame({
            "Workflow":["High-Priority Market Alert","Opportunity Qualification","Competitor Escalation","Data Quality Review","Executive Weekly Brief"],
            "Target (hrs)":[4,24,12,24,48],
            "Avg Response (hrs)":[2.6,18.2,9.4,21.1,31.5],
            "Compliance %":[96,92,95,88,99],
            "Status":["Healthy","Healthy","Healthy","Watch","Healthy"]
        })
        st.dataframe(sla, hide_index=True, use_container_width=True)
        st.progress(0.94, text="Overall SLA compliance: 94%")
        st.warning("Data Quality Review is below the 90% internal SLA target.")

    with tab4:
        exec_df = pd.DataFrame({
            "Week":["W1","W2","W3","W4"],
            "Actions Created":[31,38,44,52],
            "Actions Completed":[27,34,41,47],
            "Automation %":[62,68,73,78],
            "SLA Compliance %":[89,91,93,94]
        })
        st.dataframe(exec_df, hide_index=True, use_container_width=True)
        st.markdown("### Execution trend")
        st.line_chart(exec_df.set_index("Week")[["Actions Created","Actions Completed","Automation %"]])

    st.markdown("### 🔔 Escalation Rules")
    rules = pd.DataFrame({
        "Rule":["Critical signal","SLA breach","High churn risk","Data quality failure"],
        "Escalate to":["Executive Office","Operations Manager","Customer Success Lead","Data Manager"],
        "Response":["Immediate","Within 2 hours","Within 4 hours","Within 4 hours"],
        "Enabled":[True,True,True,True]
    })
    st.dataframe(rules, hide_index=True, use_container_width=True)

    st.markdown("### 📝 Governance Log")
    st.caption("Demo execution events are shown below. Production deployment should persist these events in the enterprise audit database.")
    log = pd.DataFrame({
        "Time":["05:31","05:24","05:10","04:52"],
        "Event":["Workflow evaluated","Action created","SLA checked","Report approval requested"],
        "Actor":["System","Intelligence Engine","System","Executive Office"],
        "Result":["Completed","Created","Completed","Pending"]
    })
    st.dataframe(log, hide_index=True, use_container_width=True)
