# iConnect SA Market Intelligence — V6 Enterprise Data Platform

V6 introduces a persistent data platform behind the command centre.

## Added
- SQLite persistence with a production migration path to PostgreSQL.
- Enterprise schema for tenants, users, audit events, data sources, ingestion runs,
  market metrics, competitor metrics, opportunities, alerts, actions and reports.
- CSV ingestion with row counts, checksum, quality score and run history.
- Database health and table-volume monitoring.
- Demo seed data.
- Streamlit Data Platform / Ingestion Centre.

## Production hardening
1. Replace local SQLite with managed PostgreSQL.
2. Store DATABASE_URL in a secret manager.
3. Add scheduled ETL/API connectors.
4. Add encryption at rest and in transit.
5. Add data-retention and backup policies.
6. Add tenant isolation at the database/query layer.
7. Connect the V5 RBAC/audit layer to persistent tables.
