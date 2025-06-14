---
description: Ensure your MongoDB is ready to sync with ObjectBox.
---

# MongoDB Configuration

In short, the ObjectBox Sync Connector only needs two things:

1. An existing MongoDB Atlas instance or a local MongoDB instance configured as a replica set.
2. A MongoDB connection URL (and thus a MongoDB user account).

## Supported MongoDB

You need at least MongoDB 5.0 or higher. If possible, use the latest 8.0 release as it provides the best performance and most of our testing happens here. Otherwise, versions 5.0 to 7.0 are also tested automatically and supported. However, we may drop support for 5.0 in the future. Contact us if you need to use an older version.

ObjectBox Sync Connector supports all MongoDB variants:

* MongoDB Community Edition (self-hosted)
* MongoDB Enterprise Advanced (self-hosted)
* MongoDB Atlas or similar cloud services (hosted)

Note: you can use the [MongoDB Atlas](https://www.mongodb.com/products/platform/atlas-database) Cloud service, which offers a free tier (M0), which is known to work well with the MongoDB Sync Connector.

## Separate MongoDB Instance for Testing

It is highly recommended to use a separate MongoDB instance for testing the ObjectBox Sync Connector. Switch to a production MongoDB instance only after everything has been thoroughly tested and confirmed to be working correctly.

It is common to start with a local MongoDB instance during the development process for quick roundtrips and tests.

## Ensure that your MongoDB instance is a Replica Set

{% hint style="info" %}
**MongoDB Atlas clusters** are already replica sets, no additional configuration is required.
{% endhint %}

If you use a local MongoDB instance (e.g. a local instance or via Docker), it likely is not a replica set yet.
Only a MongoDB replica set instance provides the necessary features for the MongoDB Sync Connector to work (e.g. MongoDB's change streams).

A local **standalone MongoDB instance** (MongoDB Community Edition is fine) can be converted to a replica set. You can do this either by following the [official MongoDB documentation](https://www.mongodb.com/docs/manual/tutorial/convert-standalone-to-replica-set/), or by following these simplified steps (tested on Ubuntu Linux) for a single node setup:

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

Note: If you are running MongoDB within a Docker container, the general principle of enabling replica set mode still applies. You would typically modify the MongoDB configuration file used by the Docker container or pass appropriate command-line arguments to `mongod` when starting the container to initiate it as a replica set. Consult the documentation for the specific MongoDB Docker image you are using for precise instructions.

## Prepare a user account for the MongoDB Sync Connector

It is recommended to use a separate MongoDB user account for the MongoDB Sync Connector. To create a MongoDB user account, see [MongoDB User Accounts](https://www.mongodb.com/docs/manual/tutorial/create-users/). Ensure that the user account has read and write access to the database and collections that you want to synchronize.

Note: the ObjectBox Sync Connector will store a few small metadata documents in a collection named `__ObjectBox_Metadata` within the database being synced. Therefore, the user account must have read and write permissions for this collection as well. Typically, granting the `readWrite` role on the database being synchronized will cover this requirement.

Once the user account is set up, you can get the MongoDB connection URL for the [ObjectBox Sync Connector setup](objectbox-sync-connector-setup.md), which is the next step.
