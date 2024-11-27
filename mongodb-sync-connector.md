---
description: Bi-directional Synchronization with MongoDB.
---

# MongoDB Sync Connector

ObjectBox Sync can synchronize data with MongoDB using the integrated [MongoDB Sync Connector](https://objectbox.io/mongodb/). This way, changes made in on ObjectBox Sync clients are synchronized to MongoDB and vice versa.

{% hint style="info" %}
At this point, the Mongo Sync Connector is available to selected customers only. Join the waitlist [here](https://objectbox.io/mongodb/).
{% endhint %}

## Bi-directional Synchronization with MongoDB

![](.gitbook/assets/MongoDB_ObjectBox_Central.png)

ObjectBox Sync brings your data in MongoDB to the edge (e.g. mobile and IoT devices, big and small servers) and synchronize changes back to MongoDB. By using ObjectBox Sync, you can make your MongoDB data always available: continue to work offline and sync in real-time when online.

## Setup

{% hint style="warning" %}
We likely don't have to mention this, but just to be on the safe side... Do not connect to your MongoDB production instance. Use an instance for testing purposes only.
{% endhint %}

Configuring the MongoDB Sync Connector involves the following steps:

1. Set up the ObjectBox Sync Server without MongoDB Sync Connector and validate it runs and actually syncs data. See the [Sync Server configuration](sync-server-configuration.md) for details.
2. Ensure that your MongoDB instance is a replica set. This is required for the MongoDB Sync Connector to work.
3. Provide the MongoDB configuration, e.g. the connection URL, to the Sync Server and restart it. This can be done via CLI arguments or the JSON configuration file (see below).
4. Use the Admin UI to verify the MongoDB connection.

### The Data Model

In general, the ObjectBox Sync server requires a data model to be provided (see the general sync server documentation). This data model is also used by the MongoDB Sync Connector to map data between ObjectBox and MongoDB. The types of the data model are mapped to MongoDB collections. Similarily, the properties of a type are mapped keys inside a MongoDB document. Thus, ensure that the data model matches the MongoDB schema.

Note: nested documents are supported via the ObjectBox "Flex" property type, which can hold a map-like (JSON-like) structure. We are also considering alternatives to this, so let us know if you have specific requirements.

### MongoDB Replica Set

Only MongoDB replica set instance provide the necessary features for the MongoDB Sync Connector to work (e.g. MongoDB's change streams). Note that all **MongoDB Atlas clusters are already replica sets**, so you are good to go with them.

Local **standalone MongoDB instances** (MongoDB Community Edition is fine) can be converted to replica sets. You can do this either by following the [official MongoDB documentation](https://www.mongodb.com/docs/manual/tutorial/convert-standalone-to-replica-set/), or by following these simplified steps (tested on Ubuntu Linux) for a single node setup:

1. Stop the MongoDB service: `sudo systemctl stop mongod`
2. Edit the MongoDB configuration file: `sudo vi /etc/mongod.conf`
3.  Add the following lines to the configuration file:

    ```yaml
    replication:
      replSetName: "rs0"
    ```
4. Start the MongoDB service: `sudo systemctl start mongod`
5. Connect to the MongoDB shell: `mongosh`
6. Initialize the replica set via the MongoDB shell: `rs.initiate()`

### MongoDB Configuration

To configure the MongoDB Sync Connector via CLI arguments, you can use the following options:

* `--mongo-url`: The [MongoDB connection string](https://www.mongodb.com/docs/manual/reference/connection-string/) (URL/URI). This can be an empty string for the default `127.0.0.1:27017` host.
* `--mongo-db`: The primary MongoDB database name; the "database" containing the collections used for sync. By default this is "objectbox\_sync".

{% hint style="warning" %}
For the JSON configuration, ensure that the server version's date is 2024-10-07 or higher. Before that, you can use {"mongoUrl": "1.2.3.4"} without the `mongoDb` config node.
{% endhint %}

If you prefer doing this via `sync-server-config.json`, you need to add a new `mongoDb` config node, which contains key/value pairs for MongoDB specific configuration attributes:

```
{
    ...
    "mongoDb": {
        "url": "1.2.3.4",
        "database": "db123"
    }
}
```
