
"""Optional Streamlit page renderer for V5 security controls."""
from enterprise_security import default_users, issue_api_key, allowed, audit

def render_security_console(st):
    st.markdown("## 🔐 Enterprise Security & Administration")
    st.caption("Role-based access, tenant controls, API keys and audit visibility.")

    st.markdown("### Role-Based Access Control")
    for u in default_users():
        perms = "All permissions" if u["role"] == "Super Admin" else ", ".join(sorted({
            "dashboard","market","competitor","customer","reports","ai"
        }) if u["role"] in {"Executive","Analyst"} else {
            "dashboard","market","customer","reports","ai"
        } if u["role"] == "Marketing Manager" else {"dashboard","reports"})
        st.write(f"**{u['username']}** · {u['role']} · {perms}")

    st.markdown("### API Key Management")
    label = st.text_input("API key label", "Production Data Connector")
    if st.button("Issue API Key"):
        st.code(issue_api_key(label)["key_preview"])

    st.markdown("### Audit Controls")
    events = [
        audit("admin", "Login", "Admin Console"),
        audit("analyst", "Export", "Market Intelligence"),
        audit("executive", "Generate", "Executive Brief"),
    ]
    st.dataframe(events, use_container_width=True)
