---
description: Recent Sync Server releases
---

# Changelog

Docker images use versions in the format "YYYY-MM-DD".
If not specified otherwise, you can pull the latest image using `docker pull objectboxio/sync-server-trial`
(via the `latest` Docker tag).

2025-11-11: New MongoDB Connector option flags
----------------------------------------------
ObjectBox version: 5.0.0-2025-11-11

* When syncing from MongoDB, there is a new global flag that creates empty lists for absent list values.
* For data conversion from/to MongoDB, there is a new strict option for each direction,
  which will stop sync on conversion errors.
  This may be useful e.g. during development to ensure no data glitch is forgotten.

2025-11-08: MongoDB Connector improvements
------------------------------------------
ObjectBox version: 5.0.0-2025-11-08

* The import phase of "MongoDB full sync" is now faster.
  By using larger batches, processing got more efficient and also results in fewer Sync history entries.
* Many-to-many relations synced from MongoDB are now considered by sync filters more reliably.
  With MongoDB, we saw some scenarios where many-to-many relations where synced before the actual target objects.        
  Since sync filters did not have sufficient information, these relations were filtered out before.

2025-10-10: JWT and MongoDB improvements
----------------------------------------
Update advise: update asap if you are using MongoDB Sync Connector.

ObjectBox version: 5.0.0-rc-2025-10-10

* JWT and Sync filters: values from nested claims in the JWT JSON are now available in sync filters
* JWT: allow `aud` to be a array (single string only)
* MongoDB connector: making Sync to MongoDB more robust, e.g. always using majority read concern

2025-10-02: Minor fixes and improvements
----------------------------------------
**Note: Sync filters require version 5.0 of ObjectBox sync clients.**

ObjectBox version: 5.0.0-rc-2025-10-02

* Incoming objects from Sync (clients) are now checked more strictly.
* Fix MongoDB CLI arguments when a configuration file is used.
* Internal improvements and dependency updates

2025-09-16: Sync filter updates, client filter variables
--------------------------------------------------------
**Note: Sync filters require version 5.0 of ObjectBox sync clients.**

* Detect when sync filters are changed for a client and enforce a complete sync from scratch.
* Client filter variables: clients can now send variables to the Sync Server, which are available in sync filter
  expressions.

2025-08-28: JSON model fix for external types and names
-------------------------------------------------------
* Parsing the JSON model file with externalType or externalName field fixed
* Sync filters: added `${...}` variable syntax for special characters

2025-08-21: Sync filter fix for vector types
--------------------------------------------
* Fixes "Float vector indexes are not supported" when using vectors in sync filter expressions
* MongoDB Sync Connector: add mapping for MongoDB's decimal128 type to string (via external property type)
* Minor dependency updates

2025-08-02: Filter expression string value improvements
-------------------------------------------------------
* Sync filter expression improvements for string values:
  allow single quotes in addition to double quotes, allow escapes using the `\` character.

2025-08-01: Sync filters and user-specific sync (beta)
------------------------------------------------------
* Sync filters: configure expressions for the Sync Server to filter objects that are to by synced.
* User-specific sync: sync filter expression can use user-specific variables and thus enable user-specific sync.
  This is a major feature that allows clients to sync only partial (individual) data.
* JWT claims available as user-specific sync filter variables.
  Data send by the clients via JWT is available to the sync filter expressions.
  Check your JWT provider how you can add the claims that you need to your JWT.

This beta version has a few known limitations that will be addressed in one of the next versions:

* When sync filter expressions changed, it's not yet handled.
  Clients may still keep old data previously synced by old filters.
  In a new version, we will likely enforce a complete sync from scratch when filters change
  so that clients have consistent data.
* It's possible to change the value of a property, which is used in a sync filter expression.
  For example, consider a property `team` that is used in a sync filter expression.
  One client changes the team from "blue" to "green".
  The server now correctly syncs the change to "team green" clients.
  However, it is not yet deleted from "team blue" clients.
* JWT claims are only the first variables available to sync filter expressions.
  We are currently collecting customer requirements to add more variables and user information.
  Check with the ObjectBox to ensure that your needs are covered.

2025-07-21: MongoDB grant check fix
-----------------------------------
* MongoDB Connector: when using a MongoDB without authentication, do not display warnings in the status page.

2025-07-17: MongoDB user grant checks and maintenance
-----------------------------------------------------
* MongoDB Connector: improved error handling; some errors only showed up in debug logs.
* MongoDB Connector: fix to only sync entity types that are actually enabled for sync.
* Admin: fixed GraphQL page (this time pinning GraphiQL to version 4.1)
* Admin: MongoDB status page now shows the MongoDB user and warnings if it does not have enough privileges for Sync.
* Admin: Special connection state if full sync was not yet performed
* Docker image: adding various Linux utility packages that are useful to debug/troubleshoot:
  iputils, iproute, procps-ng, strace, lsof, nmap-ncat
* Internal improvements, e.g. updated dependencies and compiler to new major versions

2025-06-02: Admin Fixes
-----------------------
* Admin: fixed GraphQL page
* Admin: minor UI improvements in the menu (icons, padding)

2025-05-27: Public docker image and major improvements
------------------------------------------------------
* The Sync trial is now distributed publicly as a Docker image via Docker Hub
* New "JSON to native" property type to convert strings to nested documents in MongoDB; requires 4.3 client releases
* Increase maximum Sync message size to 32 MB
* JWT authentication: public keys URLs can now refer to directly to PEM public key or X509 certificate files
* Admin fixes

2025-05-05: MongoDB initial Sync, etc.
--------------------------------------
* Import initial data from MongoDB, pick-up sync at any point.
* Admin: new admin page for full-syncs with MongoDB
* Admin: better display of large vectors in data view; display only the first element and the full vector in a dialog
* Admin: detect images stored as bytes and show them as such (PNG, GIF, JPEG, SVG, WEBP)
* Admin: new log events for important server events, which can be viewed on new Admin page

Earlier versions
----------------
We started this changelog only in May 2025, when the Sync Server was first released as a public Docker image.
Earlier versions, which were provided individually, are not listed here.