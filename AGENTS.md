# Repository Guidelines

## Project Structure & Module Organization

- This repository is documentation-first and organized by topic.
- Root pages include `README.md`, `sync-client.md`, `faq.md`, and `troubleshooting-sync.md`.
- Feature areas live in folders such as `sync-server/`, `mongodb-sync-connector/`, `data-model/`, and `blog-posts/`.
- Navigation is defined in `SUMMARY.md`; update it when adding or moving pages that should appear in the GitBook sidebar.
- Static images are stored in `.gitbook/assets/`.

## Writing Style & Conventions

- Use Markdown with clear ATX headings (`#`, `##`, `###`) and short sections.
- Keep language direct and technical.
- Avoid internal developer terms like "transaction logs" or even "TX logs"; use "sync history" or "sync logs" instead.
- Prefer fenced code blocks with an explicit language (for example `bash`, `json`, `graphql`).
- Keep file names lowercase and hyphenated (for example `sync-filters.md`).
- Use relative links for internal docs and keep image references under `.gitbook/assets/`.
- New prose edits shall follow the rule "one sentence per line", including when editing existing sentences.
- Do not reflow code blocks, tables, or GitBook tags only to enforce this rule.

## Testing Guidelines

No automated test suite is configured for this repository. Validate docs changes manually:
- check internal links and anchors you touched,
- verify code blocks are copy-paste ready,
- confirm screenshots and asset paths render correctly,
- scan changed pages for broken GitBook tags (`{% hint %}`, `{% tabs %}`, etc.).
For broad edits, review navigation integrity in `SUMMARY.md`.

## Commit & Pull Request Guidelines

Follow existing commit style: concise, scoped subjects such as `sync-client.md: fix Swift syntax` or `changelog.md: add 2026-01-20 entry`. Keep one topic per commit. PRs should include: purpose, files/sections changed, any link/path moves, and screenshots when UI docs are affected. Link related issues or tickets when available.

## File Index

Quick reference of every page in this repo and what it covers.

### Root

- **`README.md`** — Landing page. Overview of ObjectBox Sync: three-step getting-started guide, architecture diagram, core concepts (offline-first, delta sync, WebSocket networking, robust transactions, reconnection back-off).
- **`SUMMARY.md`** — GitBook table of contents. Defines left-nav structure; must be updated when pages are added, removed or moved.
- **`sync-client.md`** — Sync Client docs (~1600 lines). Covers: obtaining sync-enabled libraries per language (Java/Kotlin, Swift, Dart, C/C++, Go), enabling sync on entity types (`@Sync` annotation), starting a client, sync filter client variables (including IN values), drop-off / send-only clients, sync flags (`RemoveWithObjectData`, debug flags, etc.), authentication options (JWT, shared secret, Google Sign-In, none), manual start, event listeners, and controlling sync update behavior. Multi-language code samples throughout.
- **`faq.md`** — Frequently asked questions grouped by Data Model, Sync Server, Admin UI, and MongoDB Connector topics.
- **`troubleshooting-sync.md`** — Troubleshooting guide: reaching the server, checking network, enabling debug logging (CLI, config file, Admin UI), log events, client logs, Docker container utilities, diagnosing "clients don't connect/sync", ID mismatch explanation, MongoDB-specific issues, sync performance degradation with filters, and contacting support.

### `blog-posts/`

Ignore `blog-posts/` for now.

### `data-model/`

- **`data-model/README.md`** — Data model (schema) overview: what a data model is, managing versions via the Admin UI (uploading new JSON, switching active version).
- **`data-model/object-ids.md`** — Object IDs and Sync: default local ID spaces with automatic ID mapping, how relations map IDs, and opt-in shared global IDs (`@Sync(sharedGlobalIds = true)`) with per-language examples.

### `sync-server/`

- **`sync-server/README.md`** — Sync Server main page: getting the Docker trial image, data model JSON file (location per language, importance of version control), running the container (Bash & PowerShell), activating the trial, Admin Web UI overview (data browsing, schema, sync statistics, status page), logging (levels, format, debug logs example), updating the data model, Docker volumes appendix, Docker on Windows notes.
- **`sync-server/configuration.md`** — Server configuration: CLI options (`--help` output), JSON config file format, primary options (`dbDirectory`, `dbMaxSize`, `modelFile`, `bind`, `adminBind`), developer/debug options (detailed `log` sub-flags like `idMapping`, `syncFilterVariables`), authentication options, sync filter config reference, advanced options, clusters reference, combining CLI and file config.
- **`sync-server/jwt-authentication.md`** — JWT Authentication: obtaining/passing JWT on client side, server-side verification (audience, issuer, signature), JSON and CLI configuration, supported public key URL formats (key-value JSON / Firebase, JWKS / Auth0, PEM public key, PEM certificate).
- **`sync-server/sync-filters.md`** — Sync Filters (~450 lines): JSON config for per-type filter expressions, expression syntax (property names, comparison/string operators, IN/IN~ operators), literal and variable operands, variables (`$auth.*` from JWT claims including nested claims, `$client.*` from client-provided key/value pairs), default values (`??` syntax), logical operators (AND/OR) with precedence, performance tips (use indexes for `==`), caveats (avoid changing filtered property values).
- **`sync-server/sync-cluster.md`** — Sync Cluster: scalability (vertical & horizontal), read vs. write (leader/follower architecture), Raft-based consensus, JSON config (`clusterId`, `serversToConnect`), Admin UI cluster visualization.
- **`sync-server/embedded-sync-server.md`** — Embedded Sync Server (not standalone): using sync-server library in Java/Kotlin/C++ apps, Gradle setup for AAR/JAR, starting server programmatically, client authentication (shared secret, none), listening to incoming data changes, peer servers.
- **`sync-server/changelog.md`** — Changelog of Sync Server releases (Docker image versions from 2025-05-27 onward): filterable removes, MongoDB fixes, name mappings, sync filter improvements (IN, default values, performance), JWT improvements, Admin UI fixes, public Docker image launch, and more.

### `sync-server/admin-web-ui/`

- **`sync-server/admin-web-ui/README.md`** — Admin Web UI stub page (minimal; most Admin UI docs are inline in `sync-server/README.md`).
- **`sync-server/admin-web-ui/log-events.md`** — Log Events page in Admin UI: event types (Debug through Crash), event fields (timestamp, type, message, component, peer ID, thread, stacktrace, etc.), navigation/pagination, jump-to-date, downloading events as JSON.

### `sync-server/graphql-database/`

- **`sync-server/graphql-database/README.md`** — GraphQL overview: ObjectBox as a GraphQL database, GraphQL Playground in Admin UI (tabs, formatting, schema explorer).
- **`sync-server/graphql-database/graphql-queries.md`** — GraphQL Queries: query naming conventions, query-all, query-by-ID, filters (eq, neq, lt, gt, contains, startsWith, endsWith per type), pagination (offset, first).
- **`sync-server/graphql-database/graphql-mutations.md`** — GraphQL Mutations: put (single & multiple objects), delete by IDs, delete all, returning IDs.
- **`sync-server/graphql-database/graphql-python-client.md`** — GraphQL Python Client example: installing `python-graphql-client`, obtaining a session ID, making queries.

### `mongodb-sync-connector/`

- **`mongodb-sync-connector/README.md`** — MongoDB Sync Connector overview: bi-directional sync architecture diagram, Realm/Atlas Device Sync migration note, GA status (Oct 2025), ObjectBox vs. MongoDB terminology comparison table (store/database, box/collection, object/document, relations/embedding), next steps.
- **`mongodb-sync-connector/mongodb-configuration.md`** — MongoDB Configuration: supported versions (5.0+, prefer 8.0), supported variants (Community, Enterprise, Atlas), replica set requirement (conversion steps for standalone), user account setup (database-level vs. collection-level privileges), troubleshooting user privileges (change stream errors).
- **`mongodb-sync-connector/objectbox-sync-connector-setup.md`** — Connector Setup: creating/providing a data model, running Sync Server first, configuring MongoDB connection (CLI `--mongo-url`/`--mongo-db` or JSON config), primary database notes, all JSON config options (`automaticInitialImport`, `strictConversions*`, `emptyListForAbsentValues`), initial import from MongoDB (Admin UI workflow, progress phases, viewing import history), troubleshooting (snapshot isolation timeouts `minSnapshotHistoryWindowInSeconds`, verifying Atlas cluster reachability from Docker).
- **`mongodb-sync-connector/mongodb-data-mapping.md`** — Data Mapping (~456 lines): type/property name mapping (`@ExternalName`), ID mapping (automatic, special ID types: ObjectID, UUID variants, String, Binary, Int), property/field type mapping tables (standard types, special types like Decimal128, JavaScript, JsonToNative, MongoId, UUID, MongoBinary, MongoRegex, MongoTimestamp), to-one relations, many-to-many relations, nested documents (flex properties vs. JSON string with `@ExternalType(JsonToNative)`), heterogeneous arrays. Multi-language code samples (Java, Kotlin, Swift, Dart, C/C++, Go).
- **`mongodb-sync-connector/performance-and-best-practices.md`** — Performance tips: use transactions, avoid switching object types in a transaction, keep puts separate from removes, background on embedded vs. network DB latency.
