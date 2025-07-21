---
description: Recent Sync Server releases
---

# Changelog

Version numbers refer to the Docker images and are in the format "YYYY-MM-DD". This changelog covers releases since May 2025.

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
