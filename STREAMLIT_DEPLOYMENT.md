# Streamlit Deployment Fix — V13

The dashboard was failing with `ModuleNotFoundError` because Streamlit Cloud was launching `app.py` from the repository root while the application and its modules were split between the root and `iconnect_marketing_intelligence/`.

This build fixes the deployment layout by providing:
- a root `app.py` entry point;
- a root `requirements.txt` so Streamlit Cloud installs dependencies;
- the existing enterprise modules at the repository root;
- the full application copy under `iconnect_marketing_intelligence/`.

Recommended Streamlit Cloud configuration:
- Main file path: `app.py`
- Python dependencies: `requirements.txt`

Do not set the main file path to `iconnect_marketing_intelligence/app.py` unless you also change the deployment working directory accordingly.
