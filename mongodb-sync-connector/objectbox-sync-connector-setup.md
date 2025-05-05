---
description: >-
  Configure the ObjectBox Sync Server to connect to MongoDB and do an initial
  synchronization.
---

# ObjectBox Sync Connector Setup

Once you have a [MongoDB instance running](mongodb-configuration.md), you can connect the ObjectBox Sync Server to it.

## Setup

{% hint style="warning" %}
**Do not connect to your MongoDB production instance!** Use a separate instance for testing purposes.
{% endhint %}

Setting up Sync server and its MongoDB Sync Connector involves the following steps:

1. [**Create and provide a Data Model to Sync Server**](./#create-and-provide-a-data-model-to-sync-server) using a model JSON file.
2. [**Run and test Sync Server**](./#run-and-test-sync-server) _without_ connecting to MongoDB and validate it actually syncs data.
3. [**Ensure that your MongoDB instance is a replica set**](./#ensure-that-your-mongodb-instance-is-a-replica-set)**.** This is required for the MongoDB Sync Connector to work.
4. [**Configure the MongoDB connection and run Sync Server**](./#configure-the-mongodb-connection-and-run-sync-server)**.** E.g. provide the connection URL to the Sync Server and restart it. This can be done via CLI arguments or the JSON configuration file.
5. [**Verify the MongoDB connection**](./#verify-the-mongodb-connection) using the Admin UI.

Read on for details.

### **Create and** Provide a Data Model to Sync Server

In general, the ObjectBox Sync server requires a data model to be provided (a JSON file, see [objectbox-sync-server.md](../objectbox-sync-server.md "mention")). This data model is also used by the MongoDB Sync Connector to map data between ObjectBox and MongoDB. On how this works, see the chapter on [data mapping](./#syncing-and-mapping-data-with-mongodb) below.

### **Run and test Sync Server**

To avoid any later issues, run and test Sync Server without connecting to MongoDB and your client application and validate data is synced.

See the [objectbox-sync-server.md](../objectbox-sync-server.md "mention") page on how to run Sync Server.

### Configure the MongoDB connection and run Sync Server

To configure the ObjectBox MongoDB Sync Connector **via CLI arguments** when starting Sync Server (see [objectbox-sync-server.md](../objectbox-sync-server.md "mention")), you can use the following options:

* `--mongo-url`: The [MongoDB connection string](https://www.mongodb.com/docs/manual/reference/connection-string/) (URL or URI). This can be an empty string for the default `127.0.0.1:27017` host.
* `--mongo-db`: The primary MongoDB database name; the "database" containing the collections used for sync. By default this is "objectbox\_sync".

{% hint style="info" %}
If you are using Docker on Windows/macOS to run an instance of the ObjectBox Sync server, use `host.docker.internal` as the host in the MongoDB connection string for the `--mongo-url` parameter, for example,

```bash
docker run --rm -it \
    --volume "$(pwd):/data" \
    --user $UID \
    --publish 127.0.0.1:9999:9999 \
    --publish 127.0.0.1:9980:9980 \
    objectboxio/sync:sync-server-${sync_server_version} \
    --model /data/objectbox-model.json \
    --unsecured-no-authentication \
    --admin-bind 0.0.0.0:9980 \
    --mongo-url mongodb://host.docker.internal:27017 \
    --mongo-db test-db
```

It enables the Sync server running within the container to access the MongoDB instance running on the host system. Note, **it only works on Windows and macOS**.
{% endhint %}

Alternatively, configure the MongoDB connection in the Sync Server configuration file (see [sync-server-configuration](../sync-server-configuration/ "mention")). In your `sync-server-config.json`, add a new `mongoDb` node which contains key/value pairs for MongoDB specific configuration attributes:

```json
{
    ...
    "mongoDb": {
        "url": "1.2.3.4",
        "database": "db123"
    }
}
```

{% hint style="warning" %}
If your Sync server version's date is lower than 2024-10-07, use `{"mongoUrl": "1.2.3.4"}` without the `mongoDb` config node.
{% endhint %}

### **Verify the MongoDB connection**

Use the ObjectBox Sync Server [Admin web app](../objectbox-sync-server.md#admin-web-ui) to verify the MongoDB connection works.