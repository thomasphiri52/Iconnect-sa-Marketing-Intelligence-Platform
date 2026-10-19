
import pandas as pd
import streamlit as st
from dataclasses import dataclass, asdict

@dataclass
class Customer:
    account: str
    segment: str
    region: str
    health: int
    revenue: float
    clv: float
    churn_risk: float
    pipeline: float

def demo_customers():
    return [
        Customer("Apex Retail Group","Enterprise","Gauteng",92,1850000,6200000,4.2,840000),
        Customer("BlueWave Financial","Enterprise","Western Cape",86,1320000,4800000,8.7,620000),
        Customer("Metro Logistics","Mid-Market","KwaZulu-Natal",78,740000,2450000,15.4,410000),
        Customer("Nova Healthcare","Enterprise","Gauteng",95,2180000,7100000,3.1,980000),
        Customer("UrbanTech Solutions","SMB","Western Cape",71,285000,920000,21.8,165000),
        Customer("Cedar Manufacturing","Mid-Market","Eastern Cape",83,560000,1980000,10.2,290000),
    ]

def render_v13_customer_360(st):
    st.markdown("## 👥 Enterprise Customer 360 & CRM Intelligence")
    st.caption("Unify customer value, health, churn risk, pipeline and engagement into one decision layer.")

    customers = demo_customers()
    df = pd.DataFrame([asdict(c) for c in customers])

    total_revenue = df["revenue"].sum()
    avg_health = df["health"].mean()
    high_risk = (df["churn_risk"] >= 15).sum()
    pipeline = df["pipeline"].sum()

    k1,k2,k3,k4,k5 = st.columns(5)
    k1.metric("Accounts", len(df))
    k2.metric("Revenue", f"R {total_revenue/1e6:.2f}M")
    k3.metric("Avg Health", f"{avg_health:.0f}%")
    k4.metric("High Churn Risk", high_risk)
    k5.metric("Open Pipeline", f"R {pipeline/1e6:.2f}M")

    tabs = st.tabs(["🎯 Customer 360", "⚠️ Churn Intelligence", "💰 Revenue & CLV", "📈 Sales Pipeline", "🧩 CRM Sync"])

    with tabs[0]:
        st.markdown("### Customer portfolio")
        display = df.copy()
        display["Revenue"] = display["revenue"].map(lambda x: f"R {x:,.0f}")
        display["CLV"] = display["clv"].map(lambda x: f"R {x:,.0f}")
        display["Health"] = display["health"].map(lambda x: f"{x}%")
        display["Churn Risk"] = display["churn_risk"].map(lambda x: f"{x:.1f}%")
        display["Pipeline"] = display["pipeline"].map(lambda x: f"R {x:,.0f}")
        display = display.rename(columns={"account":"Account","segment":"Segment","region":"Region"})
        st.dataframe(display[["Account","Segment","Region","Health","Revenue","CLV","Churn Risk","Pipeline"]],
                     hide_index=True, use_container_width=True)

        account = st.selectbox("Open customer profile", df["account"].tolist(), key="v13_account")
        row = df[df["account"] == account].iloc[0]
        st.markdown(f"### {account}")
        a,b,c,d = st.columns(4)
        a.metric("Health", f"{row.health}%")
        b.metric("Revenue", f"R {row.revenue:,.0f}")
        c.metric("Customer Lifetime Value", f"R {row.clv:,.0f}")
        d.metric("Churn Risk", f"{row.churn_risk:.1f}%")
        st.info(f"Recommended focus: {'Retention intervention' if row.churn_risk >= 15 else 'Expansion and cross-sell'}.")

    with tabs[1]:
        st.markdown("### Churn risk radar")
        risk = df[["account","segment","region","health","churn_risk","revenue"]].sort_values("churn_risk", ascending=False)
        st.dataframe(risk.rename(columns={"account":"Account","segment":"Segment","region":"Region","health":"Health %","churn_risk":"Churn Risk %","revenue":"Revenue"}),
                     hide_index=True, use_container_width=True)
        st.markdown("### Automated retention priorities")
        for _, r in risk.head(3).iterrows():
            if r["churn_risk"] >= 15:
                st.warning(f"**{r['account']}** — {r['churn_risk']:.1f}% churn risk. Create retention intervention and executive review.")
            else:
                st.info(f"**{r['account']}** — monitor; risk remains below intervention threshold.")

    with tabs[2]:
        st.markdown("### Customer value distribution")
        rev = df.groupby("segment", as_index=False).agg(Revenue=("revenue","sum"), CLV=("clv","sum"))
        st.dataframe(rev, hide_index=True, use_container_width=True)
        st.bar_chart(rev.set_index("segment")[["Revenue","CLV"]])
        st.markdown("### Expansion intelligence")
        df["Expansion Potential"] = df["clv"] * (1 - df["health"]/100) * 0.25 + df["pipeline"]
        top = df.sort_values("Expansion Potential", ascending=False)[["account","Expansion Potential"]].head(5)
        top["Expansion Potential"] = top["Expansion Potential"].map(lambda x: f"R {x:,.0f}")
        st.dataframe(top.rename(columns={"account":"Account"}), hide_index=True, use_container_width=True)

    with tabs[3]:
        st.markdown("### Sales pipeline")
        pipe = df[["account","segment","region","pipeline"]].sort_values("pipeline", ascending=False)
        pipe["pipeline"] = pipe["pipeline"].map(lambda x: f"R {x:,.0f}")
        st.dataframe(pipe.rename(columns={"account":"Account","segment":"Segment","region":"Region","pipeline":"Pipeline"}),
                     hide_index=True, use_container_width=True)
        stages = pd.DataFrame({
            "Stage":["Qualified","Proposal","Negotiation","Commit"],
            "Value":[1420000,980000,610000,420000]
        })
        st.bar_chart(stages.set_index("Stage"))

    with tabs[4]:
        st.markdown("### CRM integration")
        connectors = pd.DataFrame({
            "System":["Salesforce","HubSpot","Microsoft Dynamics","Custom REST CRM"],
            "Status":["Ready","Ready","Ready","Ready"],
            "Sync Mode":["Incremental","Incremental","Incremental","Webhook/API"],
            "Last Sync":["—","—","—","—"]
        })
        st.dataframe(connectors, hide_index=True, use_container_width=True)
        system = st.selectbox("CRM system", connectors["System"].tolist(), key="v13_crm")
        if st.button("🔄 Run CRM sync", key="v13_sync"):
            st.success(f"{system} synchronization queued. Demo mode does not contact external systems.")
        st.caption("Production deployment should use OAuth/service accounts, field mapping, incremental sync, conflict handling and encrypted credentials.")
