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

All ObjectBox build tools also generate a data model JSON file, which must be provided to the ObjectBox Sync Server. This data model is also used by the MongoDB Sync Connector to map data between ObjectBox and MongoDB (see the [data mapping page](mongodb-data-mapping.md)).

### Run and test Sync Server

To avoid any later issues, run and test Sync Server without connecting to MongoDB and your client application and validate data is synced.

See the [objectbox-sync-server.md](../objectbox-sync-server.md "mention") page on how to run Sync Server.

By then you should be able to reach the ObjectBox Sync Server [Admin web app](../objectbox-sync-server.md#admin-web-ui). Navigate to the "Schema" page to see your data model, which should look like this:

<figure><img src="../.gitbook/assets/sync-server-schema.webp" alt="Admin web app schema page showing a Tape with its properties"><figcaption><p>Data model (schema), which will be synced with MongoDB</p></figcaption></figure>

For a visual overview, you can also try the "Type dependencies" and "Class" diagrams on the page. 

## Configure the MongoDB connection

{% hint style="warning" %}
Use a separate MongoDB instance for testing purposes.
{% endhint %}

Now that the Sync Server is up and running, let's connect it to MongoDB. This can be done via CLI arguments or via the configuration file.

To configure the ObjectBox MongoDB Sync Connector **via CLI arguments** when starting Sync Server (see [objectbox-sync-server.md](../objectbox-sync-server.md "mention")), you can use the following options:

* `--mongo-url`: The [MongoDB connection string](https://www.mongodb.com/docs/manual/reference/connection-string/) (URL or URI). This can be an empty string for the default `127.0.0.1:27017` host.
* `--mongo-db`: The primary MongoDB database name; the "database" containing the collections used for sync. By default, this is "objectbox\_sync".

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

<!-- not working at the moment
### **Verify the MongoDB connection**

Use the ObjectBox Sync Server [Admin web app](../objectbox-sync-server.md#admin-web-ui) to verify the MongoDB connection works.
-->

## Initial Import from MongoDB

To fully enable data synchronization, we need to do an initial import from MongoDB. This syncs all collections from MongoDB, which are part of the ObjectBox data model, into ObjectBox. It does this with snapshot isolation level to offer a maximum level of consistency, e.g. concurrent updates from other systems do not interfere with this process (when done in accordance with MongoDB transaction semantics). From this snapshot on, all changes are synchronized continuously between MongoDB and ObjectBox. If one system goes offline, the synchronization will pick up where it left off. So no change will be lost.

When you navigate to a MongoDB page in the Admin, you will see a prominent message if the initial import did not run yet:

<figure><img src="../.gitbook/assets/mongodb-initial-import-required.webp" alt="Admin web app initial import message"><figcaption><p>The initial MongoDB import still needs to be triggered</p></figcaption></figure>

## Triggering a full MongoDB import

On the "Full Sync" page beneath the "MongoDB Connector" menu, tap the "Full Import from MongoDB" button and a dialog like this will appear:

<figure><img src="../.gitbook/assets/mongodb-full-import-dialog.webp" alt="Full MongoDB import dialog showing info and input fields for name and notes"><figcaption><p>MongoDB import confirmation dialog</p></figcaption></figure>

It shows you some information and input fields. You must enter your name (required) and optional notes to help you identify this import in the future. Then tap "Import" to start the import process.

During the import you can see the progress on the page. There are two main phases:

* Exporting from MongoDB: one column shows the counts of MongoDB databases, collections and documents already exported
* Importing into ObjectBox: the next column to the right shows the counts of objects actually changed in ObjectBox and the total count of all checked objects, which should roughly match the number of documents in MongoDB

<figure><img src="../.gitbook/assets/mongodb-full-sync-importing.webp" alt=""><figcaption><p>MongoDB Example of an ongoing import</p></figcaption></figure>

As you can see in the image above, you have the possibility to abort an ongoing import process. This is to be used very cautiously, as it can yield in inconsistent states of data if importing has already started (e.g. dangling relations). Then the best thing you can do is to start a new full sync again and let it complete. You already guessed it: aborting an ongoing import should be reserved for emergencies only.

A finished import will show up in as "Completed" in the "State" column on green background. At that point, it's a good time to check the logs to ensure the sync went smoothly. Also having a look at the "Data" page will give you a good overview of the data imported.
