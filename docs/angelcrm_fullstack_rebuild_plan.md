# AngelCRM Fullstack Rebuild Plan

## 1. Document Goal

This document is the master specification for rebuilding AngelCRM as a maintainable full-stack application.

It combines four input sources:

1. the live demo site capture results,
2. the downloaded frontend bundle and DOM structure,
3. the screenshot library collected with Playwright,
4. the local reference file [AngelCRM 细粒度功能拆解文档 v4.docx](/d:/1、工作文件/25.自研项目/10.海外CRM/AngelCRM%20细粒度功能拆解文档%20v4.docx).

The rebuild target is not a static visual copy. It is a production-ready application that:

- faithfully recreates the current interaction model,
- preserves the business semantics embedded in the demo and documentation,
- upgrades the system into a real backend-driven architecture,
- supports Docker deployment and PostgreSQL persistence,
- remains easy to extend after the first delivery.

## 2. Current Reconstruction Assets

### Captured frontend artifacts

- Bundle JS: [index-Bs3lg_NN_61995081a7.js](/d:/1、工作文件/25.自研项目/10.海外CRM/output/bundles/index-Bs3lg_NN_61995081a7.js)
- Bundle CSS: [index-BMlGZC1p_d718393436.css](/d:/1、工作文件/25.自研项目/10.海外CRM/output/bundles/index-BMlGZC1p_d718393436.css)
- Static assets: [output/assets](/d:/1、工作文件/25.自研项目/10.海外CRM/output/assets)
- Route mapping: [route_bundles.json](/d:/1、工作文件/25.自研项目/10.海外CRM/output/routes/route_bundles.json)
- DOM snapshots: [output/dom](/d:/1、工作文件/25.自研项目/10.海外CRM/output/dom)
- Desktop screenshots: [output/desktop](/d:/1、工作文件/25.自研项目/10.海外CRM/output/desktop)

### Structured reconstruction inputs

- [reconstruction_inputs.json](/d:/1、工作文件/25.自研项目/10.海外CRM/output/metadata/reconstruction_inputs.json)
- [domain_model_plan.json](/d:/1、工作文件/25.自研项目/10.海外CRM/output/metadata/domain_model_plan.json)
- [schema_notes.md](/d:/1、工作文件/25.自研项目/10.海外CRM/output/metadata/schema_notes.md)
- [schema.sql](/d:/1、工作文件/25.自研项目/10.海外CRM/backend/docs/schema.sql)

### Business reference document

- [docx_extracted.txt](/d:/1、工作文件/25.自研项目/10.海外CRM/output/metadata/docx_extracted.txt)

The extracted Word document confirms that the original design intent is:

- global sales CRM for AHT / Angel,
- seven markets: `SG`, `HK`, `MY`, `TH`, `ID`, `MO`, `US`,
- product lines: commercial / retail / industrial / public scenarios,
- role-based operation across executives, country managers, sales, finance, supply chain, orders, admin, and distributors,
- a process-centric CRM rather than a contact-only CRM.

## 3. Reconstruction Scope

### In scope for the rebuild

- login and role-aware shell
- desktop-first CRM UI
- all captured navigation routes
- all captured account detail tabs
- all captured settings tabs
- realistic seed data imported from the demo bundle
- PostgreSQL-backed domain data
- FastAPI backend
- Docker Compose local startup
- audit, notifications, and role-aware data shaping

### Deferred for later phase

- mobile-specific layouts
- SSO / enterprise identity
- real external ERP / finance integrations
- file storage service beyond local / S3-compatible abstraction
- BI-grade report export engine

## 4. Product Positioning

AngelCRM is not a generic SMB CRM. It behaves like a cross-border sales operating system with:

- account planning,
- pipeline management,
- campaign-to-lead-to-opportunity conversion,
- contract and order execution,
- receivables tracking,
- deployment / installation follow-up,
- executive and country reporting,
- multi-market operational governance.

That means the rebuild must preserve:

- dense information displays,
- operational tables and detail drawers,
- role-sensitive workflows,
- business snapshots on account and opportunity records,
- auditability for key updates.

## 5. Confirmed Information Architecture

### Navigation groups

1. Home
   - `/app/today`
   - `/app/dashboard`
   - `/app/workqueue`
   - `/app/attendance`
2. Marketing
   - `/app/campaigns`
   - `/app/leads`
3. Retail
   - `/app/retail`
4. Accounts & Contacts
   - `/app/accounts`
   - `/app/pool`
   - `/app/contacts`
   - `/app/end-users`
5. Sales Pipeline
   - `/app/pipeline`
   - `/app/log-activity`
   - `/app/project-updates`
6. Contracts & Orders
   - `/app/contracts`
   - `/app/orders`
   - `/app/invoices`
   - `/app/payments`
7. Catalog
   - `/app/products`
8. Reports
   - `/app/country-reports`
   - `/app/report`
9. Admin
   - `/app/import`
   - `/app/invite`
   - `/app/team`
   - `/app/settings`

### Account detail tabs

1. Overview
2. Contacts
3. Opportunities
4. Contracts
5. Orders
6. Payments
7. Activities
8. Campaigns
9. Documents

### Settings tabs

1. Brand
2. Markets
3. Departments
4. Roles & Permissions
5. Annual Targets
6. Document Templates
7. Notifications
8. Audit Logs
9. Account

## 6. Core Domain Model

The extracted data confirms the core relationship chain:

`market -> user -> account -> contact -> opportunity -> contract -> order -> payment_plan/payment`

Supporting aggregates:

- `campaign -> lead -> conversion`
- `opportunity -> activity`
- `opportunity -> end_user`
- `account -> project_update`
- `user -> daily_report`
- `system -> notification / audit_log`

### Core entities confirmed from bundle data

1. Users
2. Markets
3. Accounts
4. Contacts
5. Campaigns
6. Leads
7. Opportunities
8. Opportunity Activities
9. Contracts
10. Orders
11. Order Items
12. Payment Plans
13. Payment Plan Lines
14. Payments
15. Products
16. End Users
17. Project Updates
18. Daily Reports
19. Document Templates
20. Notifications
21. Audit Logs

## 7. Roles and Permission Direction

Confirmed role codes from bundle:

- `executive`
- `countryManager`
- `salesManager`
- `salesRep`
- `marketing`
- `distributor`
- `admin`
- `productManager`
- `readComment`
- `readOnly`

### Rebuild guidance

- keep a coarse-grained role model in v1,
- add capability flags at backend level,
- keep menu visibility and action visibility driven by backend claims,
- preserve preview/switch-user style admin capability later if needed.

## 8. Page-by-Page Frontend Rebuild Plan

### 8.1 Login

Purpose:

- email/password login into a role-aware shell.

Must include:

- branded welcome surface,
- email/password fields,
- demo account hinting in non-production mode,
- session bootstrap,
- post-login redirect to Today.

### 8.2 Today

Purpose:

- daily operating cockpit for the current user.

Likely contents from demo and documentation:

- daily summary,
- tasks / nudges,
- account follow-ups,
- report submission cues,
- recent activity snapshots.

### 8.3 Dashboard

Must preserve the four business regions the user explicitly called out:

1. overall sales results,
2. funnel and opportunities,
3. team efficiency,
4. orders and products.

### 8.4 Work Queue

Needs:

- role switch or role-based views,
- grouped operational queues,
- action-oriented table blocks.

### 8.5 Attendance

Needs:

- check-in / check-out record view,
- daily attendance state,
- simple form or entry panel.

### 8.6 Campaigns

Needs:

- campaign list page,
- detail modal,
- metrics cards,
- channel and lead rollup display.

### 8.7 Leads

Needs:

- list table,
- status chips,
- owner / source / score,
- conversion modal,
- converted state traceability.

### 8.8 Retail

Needs:

- retail metrics list,
- monthly entry modal,
- market / account-level business entry fields.

### 8.9 Accounts

Needs:

- account list with filters,
- owner / market / contract health,
- annual target vs YTD,
- entry to account detail.

### 8.10 Account Detail

This is one of the highest-priority rebuild pages.

Must preserve:

- top-level account snapshot,
- business insight text blocks,
- tabs for all nine subdomains,
- embedded tables and activity history,
- payment and document visibility.

### 8.11 Pool

Needs:

- unassigned / released accounts,
- reason and age in pool,
- claim action.

### 8.12 Contacts

Needs:

- list view,
- account association,
- primary contact indication,
- edit / create drawer later.

### 8.13 End Users

Needs:

- installation-site list,
- reminder state,
- install status,
- opportunity linkage.

### 8.14 Pipeline

Needs:

- kanban by stage `L1` to `L7`,
- counts and total values per stage,
- drag/drop is optional in phase 1,
- detail entry to opportunity detail.

### 8.15 Log Activity

Needs:

- fast entry form,
- opportunity association,
- follow-up type,
- next action,
- scheduled follow-up time.

### 8.16 Project Updates

Needs:

- list page,
- submit progress form,
- stage-specific updates like survey / install / commissioning.

### 8.17 Contracts

Needs:

- contract list,
- status and payment status,
- value and expiry,
- edit form.

### 8.18 Orders

Needs:

- operational split views:
  - sales,
  - finance,
  - supply chain
- order detail modal or drawer,
- PI / PO / shipping traces,
- order status timeline.

### 8.19 Invoices

Needs:

- request list,
- new request form,
- status progression.

### 8.20 Payments

Needs:

- payment records,
- status,
- proof / receipt metadata,
- relation to order / contract / account.

### 8.21 Products

Needs:

- catalog table,
- product line and category,
- strategic product highlighting,
- stock / availability state.

### 8.22 Country Reports

Needs:

- three reporting form variants,
- date / market scope,
- executive summary sections.

### 8.23 Executive Report

Needs:

- cross-market leadership summary,
- high-signal KPIs,
- escalation and forecast emphasis.

### 8.24 Team

Needs:

- user list,
- role / market / manager mapping,
- invitation and activation states.

### 8.25 Settings

Needs:

- nine tab layout,
- data management and configuration forms,
- roles and permissions display,
- annual targets,
- document templates,
- audit visibility.

## 9. Frontend Technical Design

### Recommended stack

- React
- TypeScript
- Vite
- Ant Design
- React Router
- Zustand
- ECharts

### UI principles

- desktop-first at 1920x1080 target
- information-dense CRM layout
- restrained styling, operational feel
- no marketing hero patterns
- stable table layouts and tab systems
- reuse captured screenshots as visual verification targets

### Frontend module split

- `src/app`
- `src/layouts`
- `src/pages`
- `src/modules/accounts`
- `src/modules/campaigns`
- `src/modules/leads`
- `src/modules/opportunities`
- `src/modules/orders`
- `src/modules/contracts`
- `src/modules/settings`
- `src/modules/reports`
- `src/components`
- `src/store`
- `src/mocks`
- `src/styles`

### Frontend data strategy

Phase 1:

- local structured mock data generated from extracted bundle content
- reusable route config and tab config
- screenshot-guided visual parity

Phase 2:

- replace mock store reads with real FastAPI queries

## 10. Backend Technical Design

### Recommended stack

- Python 3.12+
- FastAPI
- SQLAlchemy 2.x
- Pydantic
- PostgreSQL
- Alembic
- Redis optional later

### Backend module split

- `app/modules/auth`
- `app/modules/users`
- `app/modules/markets`
- `app/modules/accounts`
- `app/modules/contacts`
- `app/modules/campaigns`
- `app/modules/leads`
- `app/modules/opportunities`
- `app/modules/contracts`
- `app/modules/orders`
- `app/modules/payments`
- `app/modules/invoices`
- `app/modules/projects`
- `app/modules/reports`
- `app/modules/settings`
- `app/modules/notifications`
- `app/modules/audit`

### Database baseline

See:

- [schema_notes.md](/d:/1、工作文件/25.自研项目/10.海外CRM/output/metadata/schema_notes.md)
- [schema.sql](/d:/1、工作文件/25.自研项目/10.海外CRM/backend/docs/schema.sql)

## 11. API Design Direction

### Authentication

- `POST /api/auth/login`
- `POST /api/auth/logout`
- `GET /api/auth/me`

### CRM core

- `GET /api/accounts`
- `GET /api/accounts/{id}`
- `GET /api/accounts/{id}/timeline`
- `GET /api/accounts/{id}/documents`
- `GET /api/opportunities`
- `GET /api/opportunities/{id}`
- `POST /api/opportunities/{id}/activities`
- `GET /api/leads`
- `POST /api/leads/{id}/convert`
- `GET /api/campaigns`
- `GET /api/contracts`
- `GET /api/orders`
- `GET /api/orders/{id}`
- `GET /api/payments`
- `GET /api/invoices`

### Settings / admin

- `GET /api/settings/markets`
- `GET /api/settings/roles`
- `GET /api/settings/targets`
- `GET /api/settings/templates`
- `GET /api/audit-logs`
- `GET /api/team/users`

## 12. Docker and Deployment Plan

### Local compose target

Services:

1. `frontend`
2. `backend`
3. `postgres`

Optional later:

4. `redis`
5. `minio`

### Local persistence

- PostgreSQL data volume
- uploads volume
- optional seed import volume

### Suggested structure

- `docker-compose.yml`
- `backend/Dockerfile`
- `frontend/Dockerfile`
- `.env`

## 13. Seed / Migration Strategy

### Initial source

Use the current demo bundle as seed input.

Bundle arrays already identified:

- `Ni` users
- `Li` accounts
- `Gi` contacts
- `ea` campaigns
- `ta` leads
- `zi` opportunities
- `Vi` activities
- `Wi` contracts
- `Ki` products
- `qi` orders
- `na` payment plans
- `ra` payments
- `Ui` end users
- `Ji` project updates
- `Yi` document templates
- `$i` daily reports

### Import pipeline

1. parse bundle arrays into structured JSON
2. map to normalized DB tables
3. load reference data first
4. load business entities in relationship order
5. validate counts and foreign keys

## 14. Verification Strategy

### Visual verification

Use the collected screenshots in [output/desktop](/d:/1、工作文件/25.自研项目/10.海外CRM/output/desktop) as parity targets for:

- layout structure
- tab presence
- table density
- cards and metrics
- modal and detail state composition

### Functional verification

- route coverage matches captured routes
- account detail has all 9 tabs
- settings has all 9 tabs
- orders has 3 operational views
- campaign / lead / retail / invoice modals exist

### Data verification

- seed counts match bundle entity counts
- known example accounts and orders are queryable
- stage and status enums match captured behavior

## 15. Delivery Phases

### Phase 1

- development spec
- schema
- frontend shell
- core mock-driven pages

### Phase 2

- backend skeleton
- postgres integration
- seed importer
- core API endpoints

### Phase 3

- frontend/backend integration
- detail actions
- permissions
- audit and notifications

### Phase 4

- refinement
- visual parity pass
- screenshot regression
- packaging and deployment docs

## 16. Immediate Execution Order

1. Finish frontend shell and navigation
2. Build Today, Dashboard, Accounts, Account Detail, Pipeline, Orders, Settings
3. Add shared mock store based on extracted entities
4. Add Docker and backend skeleton
5. Build seed importer from captured bundle

## 17. Current Decision

We are now in:

- desktop-first rebuild,
- frontend-first execution,
- backend schema already drafted,
- documentation and implementation proceeding in parallel.
