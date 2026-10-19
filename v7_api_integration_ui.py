import pandas as pd
import streamlit as st
from enterprise_api import (
    platform_health, api_catalog, connector_catalog, connector_payloads,
    create_api_key, webhook_event, WEBHOOK_EVENTS
)

def render_v7_api_integration(st_module=st):
    st_module.markdown("## ⚡ Enterprise API & Integration Hub")
    st_module.caption("API gateway, integration contracts, connector health and event-driven intelligence.")

    health = platform_health()
    c1, c2, c3, c4 = st_module.columns(4)
    c1.metric("API Status", health["status"].upper())
    c2.metric("API Version", health["api_version"])
    c3.metric("Connectors", len(connector_catalog()))
    c4.metric("Events", len(WEBHOOK_EVENTS))

    st_module.divider()

    tab1, tab2, tab3, tab4 = st_module.tabs(
        ["API Gateway", "Connectors", "Webhooks", "Developer Console"]
    )

    with tab1:
        st_module.markdown("### API Endpoint Catalogue")
        st_module.dataframe(
            pd.DataFrame(api_catalog()),
            use_container_width=True, hide_index=True
        )
        st_module.info(
            "Production deployment should place these endpoints behind TLS, "
            "authentication, rate limiting and an API gateway."
        )

    with tab2:
        st_module.markdown("### Integration Health")
        df = pd.DataFrame([vars(x) for x in connector_catalog()])
        st_module.dataframe(df, use_container_width=True, hide_index=True)

        st_module.markdown("### Connector Contracts")
        st_module.json(connector_payloads())

    with tab3:
        st_module.markdown("### Event-Driven Intelligence")
        event = st_module.selectbox("Event", sorted(WEBHOOK_EVENTS))
        payload = st_module.text_area(
            "Payload JSON",
            value='{"source":"iConnect","status":"ready","message":"Enterprise intelligence signal"}'
        )
        if st_module.button("Generate Webhook Event", type="primary"):
            try:
                import json
                result = webhook_event(event, json.loads(payload))
                st_module.success("Webhook event queued.")
                st_module.json(result)
            except Exception as exc:
                st_module.error(str(exc))

    with tab4:
        st_module.markdown("### API Key Generator")
        label = st_module.text_input("Integration label", "Client Integration")
        if st_module.button("Generate API Key"):
            raw, record = create_api_key(label)
            st_module.success("API key generated. Store it securely; it will not be shown again.")
            st_module.code(raw)
            st_module.json(vars(record))

        st_module.markdown("### Example Request")
        st_module.code(
            'curl -H "Authorization: Bearer YOUR_API_KEY" '
            'https://your-domain/api/v1/health'
        )
