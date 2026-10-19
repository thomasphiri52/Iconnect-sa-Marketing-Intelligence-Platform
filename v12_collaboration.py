
import pandas as pd
import streamlit as st
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class Notification:
    title: str
    channel: str
    priority: str
    recipient: str
    status: str

@dataclass
class Approval:
    item: str
    owner: str
    priority: str
    submitted: str
    status: str

def default_notifications():
    return [
        Notification("Critical competitor movement detected", "In-App", "Critical", "Strategy Team", "Unread"),
        Notification("Gauteng opportunity requires approval", "Email", "High", "Growth Director", "Unread"),
        Notification("Weekly executive intelligence brief ready", "Teams", "Medium", "Executive Office", "Read"),
        Notification("CRM data quality warning", "In-App", "Medium", "Data Team", "Unread"),
        Notification("Campaign performance report published", "Email", "Low", "Marketing Team", "Read"),
    ]

def default_approvals():
    return [
        Approval("Approve Gauteng expansion opportunity", "Growth Team", "High", "Today 04:55", "Pending"),
        Approval("Approve competitor response strategy", "Strategy Team", "Critical", "Today 04:42", "Pending"),
        Approval("Publish executive market report", "Executive Office", "Medium", "Yesterday 16:20", "Approved"),
        Approval("Activate data-quality remediation workflow", "Data Team", "Medium", "Yesterday 15:05", "Pending"),
    ]

def render_v12_collaboration(st):
    st.markdown("## 🤝 Enterprise Collaboration & Notification Centre")
    st.caption("Centralise alerts, approvals, team communication and executive decisions.")

    notifications = default_notifications()
    approvals = default_approvals()

    unread = sum(n.status == "Unread" for n in notifications)
    pending = sum(a.status == "Pending" for a in approvals)
    critical = sum(n.priority == "Critical" for n in notifications) + sum(a.priority == "Critical" for a in approvals)

    k1,k2,k3,k4,k5 = st.columns(5)
    k1.metric("Unread Notifications", unread)
    k2.metric("Pending Approvals", pending)
    k3.metric("Critical Items", critical)
    k4.metric("Team Members", "24")
    k5.metric("Delivery Success", "98.7%")

    tabs = st.tabs(["🔔 Notifications", "✅ Approvals", "👥 Team Workspace", "📣 Distribution", "📝 Activity Feed"])

    with tabs[0]:
        ndf = pd.DataFrame([asdict(n) for n in notifications])
        st.dataframe(ndf, hide_index=True, use_container_width=True)
        selected = st.selectbox("Select notification", ndf["title"].tolist(), key="v12_notification")
        c1,c2,c3 = st.columns(3)
        with c1:
            if st.button("✓ Mark Read", key="v12_read"):
                st.success(f"Marked as read: {selected}")
        with c2:
            if st.button("🚨 Escalate", key="v12_escalate"):
                st.warning(f"Escalated: {selected}")
        with c3:
            if st.button("↗ Create Action", key="v12_action"):
                st.success(f"Action created from: {selected}")

    with tabs[1]:
        adf = pd.DataFrame([asdict(a) for a in approvals])
        st.dataframe(adf, hide_index=True, use_container_width=True)
        selected_a = st.selectbox("Select approval", adf["item"].tolist(), key="v12_approval")
        c1,c2,c3 = st.columns(3)
        with c1:
            if st.button("✓ Approve", key="v12_approve"):
                st.success(f"Approved: {selected_a}")
        with c2:
            if st.button("↩ Request Changes", key="v12_changes"):
                st.info(f"Changes requested for: {selected_a}")
        with c3:
            if st.button("✕ Reject", key="v12_reject"):
                st.error(f"Rejected: {selected_a}")

    with tabs[2]:
        teams = pd.DataFrame({
            "Team":["Executive Office","Strategy Team","Growth Team","Marketing Team","Data Team"],
            "Members":[4,5,6,5,4],
            "Open Actions":[2,4,3,5,2],
            "SLA Compliance %":[99,95,92,94,98],
            "Status":["Online","Online","Online","Online","Online"]
        })
        st.dataframe(teams, hide_index=True, use_container_width=True)
        st.markdown("### Team message")
        recipient = st.selectbox("Send to", ["Executive Office","Strategy Team","Growth Team","Marketing Team","Data Team"], key="v12_team")
        message = st.text_area("Message", placeholder="Write an operational update...")
        if st.button("📨 Send Message", key="v12_send"):
            if message.strip():
                st.success(f"Message queued for {recipient}.")
            else:
                st.warning("Enter a message first.")

    with tabs[3]:
        st.markdown("### Report & Alert Distribution")
        report = st.selectbox("Content", ["Weekly Executive Intelligence Brief","Market Risk Alert","Opportunity Pipeline Report","Campaign Performance Report"], key="v12_report")
        destinations = st.multiselect("Destinations", ["In-App","Email","Microsoft Teams","Slack","Webhook"], default=["In-App","Email"], key="v12_destinations")
        schedule = st.selectbox("Schedule", ["Immediately","Daily 07:00","Weekly Monday 07:00","Monthly 1st 08:00"], key="v12_schedule")
        if st.button("📣 Schedule Distribution", key="v12_distribution"):
            st.success(f"{report} scheduled via {', '.join(destinations)} — {schedule}.")

    with tabs[4]:
        feed = pd.DataFrame({
            "Time":["05:31","05:24","05:12","04:55","04:42","04:20"],
            "User":["System","Intelligence Engine","Growth Team","Data Team","Strategy Team","Executive Office"],
            "Activity":["Critical alert generated","Action created","Comment added","Data issue assigned","Approval submitted","Report approved"],
            "Reference":["Competitor signal","Opportunity #27","Gauteng opportunity","CRM quality","Response strategy","Executive brief"],
        })
        st.dataframe(feed, hide_index=True, use_container_width=True)

    st.markdown("### 🔗 Notification Integrations")
    integrations = pd.DataFrame({
        "Channel":["In-App","Email","Microsoft Teams","Slack","Webhook"],
        "Status":["Active","Ready","Ready","Ready","Ready"],
        "Delivery":"Real-time",
        "Security":["RBAC","Encrypted SMTP","OAuth/Secret","OAuth/Secret","Signed payload"]
    })
    st.dataframe(integrations, hide_index=True, use_container_width=True)

    st.info("Production integrations should use encrypted credentials, verified webhook signatures, retry queues, delivery receipts and immutable audit records.")
