# iConnect SA V5 — Enterprise Security

## Added
- Role-based access control (RBAC)
- Tenant-aware user model
- API key issuance with hashed storage representation
- Audit event model
- Enterprise security/admin console renderer
- Production migration notes

## Roles
Super Admin, Executive, Analyst, Marketing Manager, Viewer.

## Production hardening
Use a real identity provider, persistent database, encrypted secrets, MFA/SSO, CSRF protection, secure cookies, rate limiting, key rotation/revocation, and immutable audit storage before production deployment.
