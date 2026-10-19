# iConnect SA Market Intelligence — V7 API & Integration Layer

V7 adds the integration foundation needed to move the command centre toward
a connected enterprise platform.

## Included
- Versioned API endpoint catalogue.
- API health service.
- Secure random API-key generation with SHA-256 storage representation.
- Connector catalogue for CRM, Google Analytics, Meta Ads, Google Ads, SQL and REST.
- Connector payload contracts.
- Event/webhook contract and event IDs.
- Developer console.
- Webhook test-event generator.

## Production deployment
- Put the API behind HTTPS and an API gateway.
- Store only hashed API keys.
- Add key rotation and revocation.
- Add OAuth2/OIDC for user-facing integrations.
- Add rate limiting, request validation and structured logs.
- Connect real provider SDKs/credentials through a secrets manager.
- Run scheduled/background ingestion jobs.
