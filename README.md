# iConnect SA — Enterprise Market Intelligence Command Centre V3

V3 upgrades the V2 prototype with an enterprise-ready **Data Integration Centre** and **Intelligence Monitor**.

## V3 additions
- Data Integration Centre for CSV/Excel, CRM, Google Analytics, Meta Ads, Google Ads, SQL and REST API connectors
- Connector status, record counts and sync visibility
- Refresh policy controls and validation modes
- Intelligence Monitor for continuous signal tracking
- Automated anomaly detection for material movements
- Pipeline timeline: source check → validation → transformation → scoring → alert evaluation → dashboard refresh
- Existing V2 Command Centre, Opportunity Intelligence, Alerts & Risk, Executive Reports and AI Analyst retained

## Run
```bash
pip install -r requirements.txt
streamlit run app.py
```

The connector layer is intentionally safe demo mode: no external credentials are stored or contacted until production endpoints are configured.
