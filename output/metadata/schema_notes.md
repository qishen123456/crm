# AngelCRM Schema Notes

## 1. Source Basis

This draft schema is derived from:

- `output/bundles/index-Bs3lg_NN_61995081a7.js`
- `output/dom/*.txt`
- `output/metadata/reconstruction_inputs.json`
- `output/metadata/domain_model_plan.json`

The live demo appears to be a front-end mock application with bundled in-memory data rather than a real API backend. Because of that, the reconstruction target should be:

1. preserve current product behavior and information architecture,
2. normalize the bundled mock data into maintainable PostgreSQL tables,
3. keep room for later workflow hardening without forcing a second schema rewrite.

## 2. Core Domain Relationships

The strongest relationship chain confirmed from bundle data is:

`account -> opportunity -> contract -> order -> payment_plan/payment`

Supporting relationships:

- `user -> accounts/opportunities/campaigns/leads/orders` via owner/requester roles
- `account -> contacts`
- `account -> documents`
- `campaign -> leads`
- `lead -> converted account/contact/opportunity`
- `opportunity -> activities`
- `opportunity -> end_users`
- `account -> project_updates`
- `contract -> orders`
- `order -> order_items`
- `order -> after_sales_tickets` or embedded service events
- `daily_reports -> activities/opportunities/accounts`

## 3. Design Principles

- Keep IDs as text/varchar initially so we can import original mock IDs like `a1`, `o13`, `cmp-1`.
- Separate reference tables from transaction tables.
- Preserve original bundle fields even if the first UI only uses part of them.
- Avoid over-normalizing view-specific aggregates that may later become materialized values.
- Use JSONB only where the mock source clearly stores semi-structured payloads.

## 4. Reference / Auth Model

### `markets`

Confirmed built-in markets:

- `SG`
- `HK`
- `MY`
- `TH`
- `ID`
- `MO`
- `US`

Need fields:

- code
- English / Chinese names
- region
- active flag
- builtin flag

### `users`

Bundle confirms these role/permission values:

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

User records also carry:

- department
- language preference
- manager
- market scope
- specialisation
- status (`active`, `invited`, etc.)

### `user_market_scopes`

Because user records carry arrays like `markets: ['SG', 'MY']`, use a join table instead of an array column.

## 5. Customer / Sales Model

### `accounts`

Confirmed account fields include:

- code
- name
- market
- ownerId
- annualTargetUsd
- yearToDateUsd
- contractStatus
- contractExpiresAt
- businessType
- opportunityNotes
- customerResources
- nextDigDirections
- landmarkCaseStatus
- marketingOwnerId
- pooledAt
- pooledReason
- embedded payment account info

Recommendation:

- keep core account row in `accounts`
- move bank / tax / settlement details into `account_payment_profiles`

### `account_contacts`

Confirmed fields:

- nameEn / nameZh
- title
- email
- phone
- wechat
- whatsapp
- isPrimary
- notes

### `leads`

Confirmed fields:

- source, status, rating
- estimated value
- owner
- campaign link
- conversion targets
- lost reason

Conversion should update but not delete the lead row.

### `campaigns`

Confirmed fields:

- code, type, status, market
- start / end dates
- budget / actual spend
- owner
- objective
- channels
- rollup metrics
- notes

Use a companion `campaign_channels` table instead of storing channels as plain text arrays.

### `opportunities`

Confirmed fields:

- stage `L1`-`L6`, and lost state `L7`
- productLine
- dealType
- expectedValueUsd
- owner
- lastActivityAt
- wonAt / lostAt
- contractNo
- commercialGrade / reason
- expectedCloseDate
- lostReason / lostNotes

Keep `contract_no_snapshot` on the opportunity because the bundle stores it there once won.

### `opportunity_activities`

Confirmed fields:

- type
- summary
- nextAction
- loggedById
- loggedAt
- scheduledFor
- sourceDailyReportId appears later in the bundle store logic

Add nullable `source_daily_report_id`.

## 6. Fulfillment / Finance Model

### `contracts`

Confirmed fields:

- contractNo
- opportunityId
- valueUsd
- feishuPaymentStatus
- expiryDate
- createdAt
- contractType
- signStatus
- valueOriginalCurrency
- valueOriginal
- effectiveDate
- durationYears
- owningEntity
- rollupOrderedUsd
- rollupCollectedUsd
- rollupShippedUsd

Contract belongs logically to an account through opportunity, but store `account_id` redundantly for simpler querying.

### `products`

Confirmed fields:

- sku
- nameEn / nameZh
- productLine
- category (`product`, `consumable`, `accessory`)
- description
- spec
- unitPriceUsd
- leadTimeDays
- availability
- status
- updatedAt
- isStrategic
- strategicReason

### `orders`

Confirmed fields:

- orderNumber
- accountId
- requestedById
- status (`submitted`, `piIssued`, `confirmed`, `shipped`, `completed`)
- piNumber / piIssuedAt
- contractId
- orderType
- paymentTerms
- notes
- PO file metadata
- shippedAt / customsDeclaredAt
- shippedDeclaredValueUsd

The bundle also shows later runtime logic for:

- `piOverrides`
- `shipmentBatches`

These should be represented as JSONB for now unless we decide to fully normalize the PI and logistics subsystem.

### `order_items`

Confirmed fields:

- productId
- productSku
- productNameEn
- quantity
- unitPriceUsd
- lineTotalUsd

Keep sku and product name snapshots to preserve historical truth.

### `payment_plans`

Confirmed root fields:

- orderId
- accountId
- totalDueUsd
- currency
- createdAt

The bundle stores line arrays underneath each plan, so normalize into:

- `payment_plans`
- `payment_plan_lines`

### `payments`

The planning JSON had only partial certainty, but bundle/store naming confirms `paymentRecords` and matching add/update actions.

Expected stable columns:

- order_id
- account_id
- amount
- currency
- status
- received_at
- confirmed_at
- proof file metadata
- receipt file metadata
- note / reference

Because field certainty is lower than contracts/orders, keep room for nullable fields and add `raw_payload JSONB`.

### `invoice_requests`

The store logic references invoice request CRUD even though we have less bundle detail than for orders/contracts. Add an explicit table now, because the UI has a standalone invoice module and creation form.

## 7. Delivery / Post-Sale Model

### `end_users`

Confirmed fields from bundle:

- opportunityId
- siteName
- productType
- unitCount
- installStatus
- reminderCount
- installedAt
- lastReminderAt

This is really installation/site-level deployment tracking.

### `project_updates`

Confirmed fields:

- accountId
- postedById
- stage (`install`, `survey`, `commissioning`)
- summary
- unitsInstalled
- createdAt

## 8. Admin / Collaboration Model

### `daily_reports`

Confirmed fields:

- userId
- date
- todaySummary
- tomorrowPlan
- customersContacted
- revenueUpdateNote
- blockers
- escalationNotes
- escalationPriority
- escalationAccountIds
- moodRating
- submittedAt

Because arrays are present, split into:

- `daily_reports`
- `daily_report_accounts`
- optional future `daily_report_touchpoints`

### `document_templates`

Confirmed fields:

- type
- name
- description
- fileName
- uploadedById
- uploadedAt
- isActive

### `account_documents`

Needed for the account detail "Documents" tab. Exact bundle structure is less explicit, so start with generic metadata:

- account_id
- name
- file_name
- file_url
- document_type
- uploaded_by
- uploaded_at

### `notifications`

The store exposes notification actions and role-targeted triggers from order status changes. Keep a simple notifications table with:

- audience / target role
- event type
- bilingual title/body if needed
- link
- read state

### `audit_logs`

The store writes audit events for many actions (`update_user`, `update_account`, `update_opportunity`). This should be first-class in the rebuild.

Recommended fields:

- actor_user_id
- action
- entity_type
- entity_id
- summary
- detail_json
- created_at

## 9. Tables To Create First

Phase 1 tables required for an MVP that matches the current demo:

1. `markets`
2. `users`
3. `user_market_scopes`
4. `accounts`
5. `account_payment_profiles`
6. `account_contacts`
7. `campaigns`
8. `campaign_channels`
9. `leads`
10. `opportunities`
11. `opportunity_activities`
12. `contracts`
13. `products`
14. `orders`
15. `order_items`
16. `payment_plans`
17. `payment_plan_lines`
18. `payments`
19. `invoice_requests`
20. `project_updates`
21. `end_users`
22. `document_templates`
23. `account_documents`
24. `daily_reports`
25. `daily_report_accounts`
26. `notifications`
27. `audit_logs`

## 10. Seed Strategy

Use the original bundle data as the initial seed source.

Recommended seed layers:

1. `seed_reference`
   - markets
   - users
   - roles/permissions enum values
   - picklists
2. `seed_master`
   - products
   - document templates
3. `seed_business`
   - accounts
   - contacts
   - campaigns
   - leads
   - opportunities
   - contracts
   - orders
   - payment plans
   - payments
   - project updates
   - end users
4. `seed_collaboration`
   - daily reports
   - notifications
   - audit logs

For the rebuild, keep a dedicated import script that maps bundle arrays by anchor:

- `Ni` -> users
- `Li` -> accounts
- `zi` -> opportunities
- `Vi` -> activities
- `Ui` -> end_users
- `Wi` -> contracts
- `Gi` -> contacts
- `Ki` -> products
- `qi` -> orders
- `na` -> payment_plans
- `ra` -> payments
- `Ji` -> project_updates
- `Yi` -> document_templates
- `$i` -> daily_reports
- `ea` -> campaigns
- `ta` -> leads

## 11. FastAPI Module Split Recommendation

Suggested backend package split:

- `app/modules/auth`
- `app/modules/users`
- `app/modules/markets`
- `app/modules/accounts`
- `app/modules/contacts`
- `app/modules/campaigns`
- `app/modules/leads`
- `app/modules/opportunities`
- `app/modules/contracts`
- `app/modules/products`
- `app/modules/orders`
- `app/modules/payments`
- `app/modules/invoices`
- `app/modules/projects`
- `app/modules/reports`
- `app/modules/settings`
- `app/modules/notifications`
- `app/modules/audit`

## 12. Open Gaps

Items still worth a second extraction pass before we freeze v1 API contracts:

- exact invoice request fields
- exact payment record fields from bundle/store
- settings sub-tab data structures:
  - brand
  - targets
  - notifications
  - roles & permissions
- work queue aggregation logic
- dashboard KPI formulas
- country report form schemas

These gaps do not block starting the backend skeleton, schema, and seed importer.
