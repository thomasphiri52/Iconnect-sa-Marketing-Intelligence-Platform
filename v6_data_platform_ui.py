import pandas as pd
import streamlit as st
from enterprise_data_platform import (
    initialize, health, seed_demo, source_rows, recent_ingestions, ingest_csv
)

def render_v6_data_platform(st_module=st):
    initialize()
    st_module.markdown("## 🗄️ Enterprise Data Platform")
    st_module.caption("Persistent data layer, ingestion monitoring, data quality and operational health.")

    h = health()
    c1, c2, c3, c4 = st_module.columns(4)
    c1.metric("Database", h["status"].upper())
    c2.metric("Tables", len(h["tables"]))
    c3.metric("Stored Records", sum(h["tables"].values()))
    c4.metric("DB Size", f"{h['size_bytes']/1024:.1f} KB")

    st_module.divider()
    left, right = st_module.columns([1.15, 1])

    with left:
        st_module.markdown("### Data Sources")
        rows = source_rows()
        if rows:
            df = pd.DataFrame(rows)
            st_module.dataframe(
                df[["name","source_type","status","row_count","quality_score","last_run"]],
                use_container_width=True, hide_index=True
            )
        else:
            st_module.info("No data sources configured yet.")

        st_module.markdown("### Ingestion Centre")
        upload = st_module.file_uploader("Upload CSV data", type=["csv"], key="v6_csv")
        source_name = st_module.text_input("Source name", value="Business Data")
        if upload and st_module.button("Ingest into Enterprise Data Platform", type="primary"):
            tmp = __import__("tempfile").NamedTemporaryFile(delete=False, suffix=".csv")
            tmp.write(upload.getvalue())
            tmp.close()
            result = ingest_csv(tmp.name, source_name)
            st_module.success(
                f"{result.status}: {result.rows_loaded} rows loaded, "
                f"{result.rows_rejected} rejected, quality {result.quality_score}%"
            )
            st_module.rerun()

    with right:
        st_module.markdown("### Data Warehouse Tables")
        counts = h["tables"]
        for name, count in counts.items():
            st_module.write(f"**{name.replace('_',' ').title()}** — {count:,} records")

        st_module.markdown("### Pipeline Runs")
        runs = recent_ingestions()
        if runs:
            st_module.dataframe(
                pd.DataFrame(runs)[["source_name","filename","status","rows_loaded","rows_rejected","completed_at"]],
                use_container_width=True, hide_index=True
            )
        else:
            st_module.info("No ingestion runs yet.")

        st_module.markdown("### Environment")
        st_module.code(
            "ICONNECT_DB_PATH=/path/to/iconnect_enterprise.db\n"
            "Use PostgreSQL in production by mapping this persistence layer to your managed database."
        )
        if st_module.button("Seed Demo Enterprise Data"):
            if seed_demo():
                st_module.success("Demo intelligence records added.")
            else:
                st_module.info("Demo data already exists.")
            st_module.rerun()
