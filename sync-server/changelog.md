---
description: Recent Sync Server releases
---

# Changelog

Version numbers refer to the Docker images and are in the format "YYYY-MM-DD". This changelog covers releases since May 2025.

### 2025-06-02

* Admin: fixed GraphQL page
* Admin: minor UI improvements in the menu (icons, padding)

### 2025-05-27

* The Sync trial is now distributed publicly as a Docker image via Docker Hub
* New "JSON to native" property type to convert strings to nested documents in MongoDB; requires 4.3 client releases
* Increase maximum Sync message size to 32 MB
* JWT authentication: public keys URLs can now refer to directly to PEM public key or X509 certificate files
* Admin fixes

### 2025-05-05

* Import initial data from MongoDB, pick-up sync at any point.
* Admin: new admin page for full-syncs with MongoDB
* Admin: better display of large vectors in data view; display only the first element and the full vector in a dialog
* Admin: detect images stored as bytes and show them as such (PNG, GIF, JPEG, SVG, WEBP)
* Admin: new log events for important server events, which can be viewed on new Admin page
