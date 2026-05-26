# Production Readiness Plan

Status date: 2026-04-24
Scope: Backend, frontend, deployment, security, and release quality gates

## 1) Launch Gate Definition

Go live only when all items below are complete:

- No default secrets, no DEBUG mode, and no dev reload in production
- PostgreSQL in production with migration-based schema management
- Admin flows fully functional end-to-end (products, categories, quotes, posts, settings, contacts, brands)
- No known high/critical security issues (XSS, path traversal, auth/session hardening)
- Production deployment pipeline exists and is repeatable
- Smoke tests pass for public + admin critical paths
- Monitoring, logs, and backup/restore runbook verified

## 2) Priority Phases

## Phase P0 (Blockers, do first)

Objective: Remove immediate launch risks and broken functionality.

### P0.1 Runtime hardening
- Set production defaults via environment only, not insecure code defaults.
- Files to update:
  - backend/app/core/config.py
  - backend/app/main.py
  - docker-compose.yml (or separate docker-compose.prod.yml)
- Acceptance:
  - DEBUG false in production
  - docs disabled in production
  - strong SECRET_KEY required at startup
  - no --reload in production command

### P0.2 Database lifecycle
- Introduce Alembic migrations and remove startup create_all behavior.
- Files to update:
  - backend/app/core/database.py
  - backend/ (add alembic.ini, alembic/env.py, versions/*)
- Acceptance:
  - app starts without create_all auto-mutation
  - migration baseline created and applied cleanly
  - rollback strategy documented

### P0.3 API contract parity for admin
- Fix backend routes vs frontend expectations.
- Files to update:
  - backend/app/api/v1/__init__.py
  - backend/app/api/v1/endpoints/quotes.py
  - backend/app/api/v1/endpoints/products.py
  - backend/app/api/v1/endpoints/brands.py
  - backend/app/api/v1/endpoints/admin_settings.py (ensure mounted)
  - backend/app/api/v1/endpoints/sitemap.py (ensure mounted)
  - frontend/pages/admin/*
- Acceptance:
  - no 404/405 across admin UI actions
  - quotes list + update works
  - products create/edit/delete works
  - settings endpoints mounted and functional
  - sitemap endpoint reachable

### P0.4 Finish missing admin surfaces
- Implement missing pages and/or remove dead nav links.
- Files to update:
  - frontend/layouts/admin.vue
  - frontend/pages/admin/brands/* (create)
  - frontend/pages/admin/contacts/* (create)
  - frontend/pages/admin/products/new.vue (create)
  - frontend/pages/admin/products/[id].vue (create)
  - frontend/pages/admin/index.vue (replace TODO with real data)
- Acceptance:
  - every admin menu link resolves
  - dashboard shows real counts and recent items

## Phase P1 (Security and reliability)

Objective: Eliminate high-impact vulnerabilities and stabilize operations.

### P1.1 XSS protection for rich content
- Sanitize stored HTML for post content and product description.
- Files to update:
  - backend/app/schemas/post.py
  - backend/app/schemas/product.py
  - backend/app/api/v1/endpoints/admin_posts.py
  - backend/app/api/v1/endpoints/products.py (admin write paths)
  - frontend/pages/tin-tuc/[slug].vue
  - frontend/pages/san-pham/[slug].vue
- Acceptance:
  - malicious script payloads are neutralized
  - allowed formatting tags still render correctly

### P1.2 Upload path safety
- Restrict upload subfolder input to allowlist; prevent traversal and unsafe deletions.
- Files to update:
  - backend/app/api/v1/endpoints/upload.py
  - backend/app/services/image_service.py
- Acceptance:
  - subfolder validated against strict pattern/allowlist
  - delete operation cannot escape upload root
  - upload tests include traversal attempts

### P1.3 Admin auth/session hardening
- Move away from localStorage bearer token to secure cookie/session pattern.
- Files to update:
  - backend/app/api/v1/endpoints/auth.py
  - backend/app/api/deps.py
  - frontend/stores/auth.ts
  - frontend/layouts/admin.vue
  - frontend/middleware/* (create route guard middleware)
- Acceptance:
  - auth token not stored in localStorage
  - admin routes protected before page render
  - logout invalidates session effectively

### P1.4 Bootstrap/admin provisioning safety
- Remove default credentials from normal path and gate first-admin bootstrap.
- Files to update:
  - backend/app/seed.py
  - backend/app/api/v1/endpoints/auth.py
  - backend/README.md
- Acceptance:
  - no known static admin credential in prod runbook
  - first admin creation is controlled (env flag/one-time token/manual command)

## Phase P2 (Deployment and observability)

Objective: Make production deploy reproducible and supportable.

### P2.1 Production containers
- Build immutable production images and run non-dev commands.
- Files to update:
  - backend/Dockerfile
  - frontend/Dockerfile
  - docker-compose.yml (or docker-compose.prod.yml)
- Acceptance:
  - frontend runs nuxt build + start/preview in prod mode
  - backend uses production ASGI settings
  - no source bind mounts in production

### P2.2 Reverse proxy, TLS, and security headers
- Add Nginx (or equivalent) for HTTPS termination and headers.
- Files to add/update:
  - nginx/nginx.conf
  - compose/prod deployment manifests
- Acceptance:
  - HSTS, X-Content-Type-Options, X-Frame-Options/CSP policy defined
  - gzip/brotli and cache policy configured for static assets

### P2.3 Logging and health
- Structured logs and endpoint health checks wired for orchestration.
- Files to update:
  - backend/app/main.py
  - deployment config
- Acceptance:
  - health + readiness checks available
  - logs capture request id, status, latency, and error traces

### P2.4 Backups and restore
- Add DB backup schedule and restore drill docs.
- Files to add:
  - docs/runbooks/backup-restore.md
- Acceptance:
  - successful restore test from latest backup

## Phase P3 (Quality gates and release governance)

Objective: Prevent regressions and make releases predictable.

### P3.1 Automated tests
- Add API and UI smoke tests for key paths.
- Suggested coverage:
  - public: home, product list/detail, quote submit, contact submit
  - admin: login, product CRUD, quote status update, post CRUD, settings update
- Files to add:
  - backend/tests/*
  - frontend/tests/* or e2e framework setup
- Acceptance:
  - smoke suite required in CI before merge/deploy

### P3.2 CI/CD
- Add build, lint, test, image build, and deploy workflow.
- Files to add:
  - .github/workflows/ci.yml
  - .github/workflows/deploy.yml
- Acceptance:
  - pull requests run full validation
  - deploy uses protected environment/secrets

### P3.3 Documentation alignment
- Update docs to match actual implementation.
- Files to update:
  - README.md
  - PROJECT_SPEC.md
  - backend/README.md
- Acceptance:
  - no major mismatch between spec and running system

## 3) Suggested Execution Order (Fastest path)

Week 1
- P0.1, P0.2, P0.3

Week 2
- P0.4, P1.1, P1.2

Week 3
- P1.3, P1.4, P2.1, P2.2

Week 4
- P2.3, P2.4, P3.1, P3.2, P3.3

## 4) Ownership Template

For each task, assign:
- Owner
- Reviewer
- Estimated effort (S/M/L)
- Start date
- Target date
- Risk notes

## 5) Immediate Next Actions (Tomorrow)

- Create migrations baseline and disable create_all startup path
- Fix API route mounting and admin endpoint parity first
- Implement missing admin pages or remove links until implemented
- Switch production config to secure env-only settings
- Add one smoke test per critical flow before further feature work

## Appendix: SQLite Go‑Live Checklist

This checklist is tailored to deploying this application with a persisted SQLite file (`autofilm.db`). Use it as the minimal launch gate for small-scale or single-instance deployments.

- **Environment:** Set `DEBUG=False` and provide `SECRET_KEY` (>=32 chars) via environment only.
- **Database URL:** Set `DATABASE_URL=sqlite+aiosqlite:////app/data/autofilm.db` in production containers and mount a named volume to `/app/data`.
- **Migrations:** Run `alembic upgrade head` against the production DB file prior to starting the app.
- **Seed Admin:** Run `python -m app.seed` once to create the initial admin user; confirm the account exists and disable open registration.
- **Backups:** Configure an automated backup of the `autofilm.db` file (daily or more frequent), keep offsite copies, and test restore to a staging instance.
- **File permissions:** Ensure the runtime user can read/write `/app/data` and `/app/uploads`, and that volumes are not world-writable.
- **Healthchecks:** Verify `/health` and readiness endpoints respond correctly and are included in your orchestration (container restart on failure).
- **Static assets:** Build frontend (`npm run build`) and serve via a reverse proxy; in containers, do not mount source folders in production images.
- **TLS & Proxy:** Terminate TLS at the proxy (Nginx/Cloud LB) and set security headers (HSTS, X-Frame-Options, CSP, X-Content-Type-Options).
- **Monitoring & Logs:** Ship logs to an external system, enable error alerting, and monitor DB file size/growth (SQLite can become a bottleneck).
- **Scale & Limitations:** Document that SQLite is single-writer and not suitable for multi-replica writes; plan migration to Postgres for higher scale.
- **Rollback:** Keep a pre-migration DB snapshot to restore in case of migration issues; test the restore procedure as part of pre-launch checks.
- **Operational Runbook:** Add short runbook steps for: "migrate", "seed admin", "backup rotate", "restore from backup", and "rebuild frontend".

Follow this checklist before flipping DNS to the new instance. For production with moderate traffic or multiple replicas, replace SQLite with a managed Postgres instance and update the deployment manifests accordingly.
