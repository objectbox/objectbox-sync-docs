---
description: Frequently asked question about ObjectBox Sync.
---

# FAQ

## Data Model

_ObjectBox (mostly) has a fixed schema, aka the data model._ 

**How do I get the data model (objectbox-model.json) for the Sync Server?**

The data model file is created by Sync Clients. Use the same file for the Sync server (e.g. copy it to your server directory). When your data model changes, the file will change and thus it has to be updated for the Sync Server, too. Details are available on the [Sync Server page](sync-server/README.md#data-model-json-file).

<hr>

**What are these IDs in the data model file? Why do I have to check in the model file?**

When you look inside the JSON file of the model file, you will notice that entity types and properties also have IDs. These IDs are essential information to ObjectBox Sync and there are strict rules to them. First and most importantly, consider the data model file a crucial part of your sources and store it in your version control system like git. The IDs are maintained by the ObjectBox build tools and should not be changed manually nor should the model file be deleted. Different IDs, e.g. when regenerating the data model after it was, lead to inconsistencies that will prevent to sync to work(!).

Why use IDs at all? Unlike string-based names, IDs are meant to be stable. Consider renaming a property: from the data model perspective it is not clear if it was a rename or if one property was deleted and a new property was added. This is solved by using IDs. Furthermore, it allows automatic data model updates without writing any migration scripts.

For details, please refer to the general [Data Model Updates](https://docs.objectbox.io/advanced/data-model-updates) and Sync-specific [Data Model](data-model/README.md) pages.

<hr>

## Sync Server

_General questions about the ObjectBox Sync Server that do not fit into any other category._

**Can I sync data directly between devices?**

The typical ObjectBox Sync setup is to have a centralized. However, alternative setup are possible within given bounds. For example, for a limited amount of devices it is possible to configure peers that sync directly with each other. There's also "hybrid" nodes that are both a client and a server. And finally, there's also a "edge" setup, e.g. via a central MongoDB that allows to have multiple Sync Servers. Talk to us if you are interested in such a setup.  

## Admin UI

_The Admin UI is a web interface for ObjectBox Sync Server._

**Can I edit/remove data directly in the Admin interface or via API? Or only via Sync clients?

The Admin allows to browse data in a read-only way. You can modify data directly on the Sync Server via the [GraphQL API](sync-server/graphql-database/README.md). 

## MongoDB Connector

_The MongoDB Connector allows to synchronize data between ObjectBox Sync Server and MongoDB._

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

<hr>

**What happens if fields are only present on the MongoDB side?**

If a field/property is present on both sides, it will be synced. If a field is only present in a MongoDB document, it will be ignored on ObjectBox. Updates from ObjectBox do not touch "unknown" fields stored in the MongoDB document. New documents created from ObjectBox objects will only include fields that are present on ObjectBox.
If a field is present on ObjectBox only, it will be ignored on MongoDB.

<hr>

**What happens if properties are only present on the ObjectBox side?**

If a field/property is present on both sides, it will be synced. If a property is only present in an ObjectBox object, it will be read as a "null" value (no value). Updates and inserts from ObjectBox will store the property value as a field in the MongoDB document.

<hr>

**Is it possible to connect multiple Sync Servers to one MongoDB instance?**

Yes, that's what we call "tiered sync" or "edge sync". The MongoDB database becomes the central instance, where all ObjectBox Sync Servers are connected to synchronize data. Each Sync Server can be deployed at its own location and can have its own set of clients. You can setup this with the Server trial on your own, or talk to us if you are interested in further details.
