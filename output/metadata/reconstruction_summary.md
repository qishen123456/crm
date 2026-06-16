# AngelCRM Reconstruction Summary

## Captured Inputs

- Bundled frontend assets:
  - `output/bundles/index-Bs3lg_NN_61995081a7.js`
  - `output/bundles/index-BMlGZC1p_d718393436.css`
- Static assets:
  - `output/assets/`
- Route and bundle mapping:
  - `output/routes/route_bundles.json`
- Page screenshots and interaction captures:
  - `output/desktop/`
- DOM snapshots:
  - `output/dom/`
- Structured extraction:
  - `output/metadata/reconstruction_inputs.json`
  - `output/metadata/domain_model_plan.json`

## Navigation Groups

- Home:
  - `/app/today`
  - `/app/dashboard`
  - `/app/workqueue`
  - `/app/attendance`
- Marketing:
  - `/app/campaigns`
  - `/app/leads`
- Retail:
  - `/app/retail`
- Accounts & Contacts:
  - `/app/accounts`
  - `/app/pool`
  - `/app/contacts`
  - `/app/end-users`
- Sales Pipeline:
  - `/app/pipeline`
  - `/app/log-activity`
  - `/app/project-updates`
- Contracts & Orders:
  - `/app/contracts`
  - `/app/orders`
  - `/app/invoices`
  - `/app/payments`
- Catalog:
  - `/app/products`
- Reports:
  - `/app/country-reports`
  - `/app/report`
- Admin:
  - `/app/import`
  - `/app/invite`
  - `/app/team`
  - `/app/settings`

## Account Detail Tabs

- Overview
- Contacts
- Opportunities
- Contracts
- Orders
- Payments
- Activities
- Campaigns
- Documents

## Settings Tabs

- Brand
- Markets
- Departments
- Roles & Permissions
- Annual Targets
- Document Templates
- Notifications
- Audit Logs
- Account

## Confirmed Mock Domains From Bundle

- Users:
  - executive
  - countryManager
  - salesManager
  - salesRep
  - marketing
  - distributor
  - admin
  - productManager
  - finance-like read roles
- Markets:
  - `SG`, `HK`, `MY`, `TH`, `ID`, `MO`, `US`
- Core business objects:
  - accounts
  - opportunities
  - campaigns
  - leads
  - contracts
  - orders
  - payment plans
  - payments
  - project updates
  - daily reports
  - document templates

## Suggested Backend Core Tables

- `users`
- `markets`
- `user_market_scopes`
- `accounts`
- `account_contacts`
- `opportunities`
- `opportunity_activities`
- `campaigns`
- `leads`
- `contracts`
- `orders`
- `order_items`
- `payment_plans`
- `payment_plan_lines`
- `payments`
- `project_updates`
- `end_users`
- `products`
- `document_templates`
- `account_documents`
- `daily_reports`
- `notifications`
- `audit_logs`

## Immediate Next Build Step

Use `output/metadata/domain_model_plan.json` as the source for:

- PostgreSQL schema draft
- FastAPI module split
- seed/mock data scaffolding
- frontend route-to-page mapping
