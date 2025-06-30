---
description: Frequently asked question about ObjectBox Sync.
---

# FAQ

## MongoDB Connector

**When does the MongoDB Connector start syncing?**

The MongoDB connector starts along with Sync Server. In the initial state, the connector won't "start" right away. It will only start syncing once the first full sync is completed. The idea not to do this automatically is to make this a conscious decision, so that this does not happen by accident. While the first sync did not happen yet, there is a prominent message in the admin UI for the MongoDB pages. Also the logs periodically print a "reminder".

<hr>

**Do I need to run a full import from MongoDB to receive the latest changes? Or should this happen automatically?**

You need only **one initial** full import (triggered via Admin UI) in the beginning. Once this completes, ObjectBox will pick up changes from there on. ObjectBox and MongoDB are then synced bidirectionally and automatically.

<hr>

**What is the purpose of the __ObjectBox_Metadata collection and what does it store?**

When syncing ObjectBox to MongoDB, ObjectBox creates a collection called __ObjectBox_Metadata. This collection stores the exact state from where sync (from ObjectBox to MongoDB) can continue. Changing __ObjectBox_Metadata is part of the transaction, where data gets changed. So this is the transactional-safe way. The same info is also written to ObjectBox' internal database after the MongoDB transaction. Thus, even deleting the __ObjectBox_Metadata (e.g. by accident) typically does not affect anything. It's "just" to make things fully transactional.

<hr>

**Do I have to create a objectbox_sync database in MongoDB? Or can I use custom database and collection names for syncing?**

The database name can be configured via CLI and JSON; see [the MongoDB connector setup](mongodb-sync-connector/objectbox-sync-connector-setup#configure-the-mongodb-connection) for details.

Collection (and field) names will be configurable by "external name" annotations in the data model in the future. Please reach out to us if you require this feature.
