---
description: Recent Sync Server releases
---

# Changelog

Version numbers refer to the Docker images and are in the format "YYYY-MM-DD".
This changelog covers releases since May 2025.

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
* Sync filters: configure expressions for the Sync Server to filter objects that are to be synced.
* User-specific sync: sync filter expression can use user-specific variables and thus enable user-specific sync.
  This is a major feature that allows clients to sync only partial (individual) data.
* JWT claims available as user-specific sync filter variables.
  Data sent by clients via JWT is available to the sync filter expressions.
  Check your JWT provider how you can add the claims that you need to your JWT.

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
* JWT authentication: public key URLs can now refer directly to PEM public key or X509 certificate files
* Admin fixes

2025-05-05: MongoDB initial Sync, etc.
--------------------------------------
* Import initial data from MongoDB, pick up sync at any point.
* Admin: new admin page for full-syncs with MongoDB
* Admin: better display of large vectors in data view; display only the first element and the full vector in a dialog
* Admin: detect images stored as bytes and show them as such (PNG, GIF, JPEG, SVG, WEBP)
* Admin: new log events for important server events, which can be viewed on new Admin page
