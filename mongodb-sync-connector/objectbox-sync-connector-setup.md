---
description: >-
  Configure the ObjectBox Sync Server to connect to MongoDB and do an initial
  synchronization.
---

# ObjectBox Sync Connector Setup

Once you have a [MongoDB instance running](mongodb-configuration.md), you can connect the ObjectBox Sync Server to it.

## ObjectBox Preparations

Before using the MongoDB Sync Connector, let's ensure that the ObjectBox Sync Server is up and running. This involves basically two steps: having a data model and running the ObjectBox Sync Server. Read on for details.

### Create and Provide a Data Model

{% hint style="info" %}
The ObjectBox data model defines which collections are synced with MongoDB (and much more...).
{% endhint %}

In general, the ObjectBox relies on a data model, which is typically defined as part of your (client) application. This is a different approach to MongoDB and other databases. The data model is defined by developers using special annotations in the programming language of your application. If you are not familiar with that process yet, then this is a good time to get familiar with ObjectBox "annotations" and how to define your data model. This is dependent on the programming language:

* [Java, Kotlin, Dart, Python](https://docs.objectbox.io/entity-annotations)
* [Swift](https://swift.objectbox.io/entity-annotations)
* [Go](https://golang.objectbox.io/entity-annotations)
* [C, C++](https://cpp.objectbox.io/entity-annotations) (uses a FlatBuffers schema file)

All ObjectBox build tools also generate a data model JSON file. This 

Sync server requires a  to be provided (a JSON file, see [objectbox-sync-server.md](../objectbox-sync-server.md "mention")). This data model is also used by the MongoDB Sync Connector to map data between ObjectBox and MongoDB (see the [data mapping page](mongodb-data-mapping.md)).

### **Run and test Sync Server**

To avoid any later issues, run and test Sync Server without connecting to MongoDB and your client application and validate data is synced.

See the [objectbox-sync-server.md](../objectbox-sync-server.md "mention") page on how to run Sync Server.

## Configure the MongoDB connection

{% hint style="warning" %}
Use a separate MongoDB instance for testing purposes.
{% endhint %}

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

### **Verify the MongoDB connection**

Use the ObjectBox Sync Server [Admin web app](../objectbox-sync-server.md#admin-web-ui) to verify the MongoDB connection works.