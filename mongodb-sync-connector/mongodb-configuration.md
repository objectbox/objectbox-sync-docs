---
description: Ensure your MongoDB is ready to sync with ObjectBox.
---

# MongoDB Configuration

In short, the ObjectBox Sync Connector only needs two things:

1. An existing MongoDB Atlas instance or a local MongoDB instance configured as a replica set 
2. A MongoDB connection URL (and thus a MongoDB user account)

## Supported MongoDB

You need at least MongoDB 5.0 or higher. If possible, use the latest 8.0 release as it provides the best performance and most of our testing happens here. Otherwise, versions 5.0 to 7.0 are also tested automatically and supported. However, we may drop support for 5.0 in the future. Contact us if you need to use an older version.

Hint: you can use the [MongoDB Atlas](https://www.mongodb.com/products/platform/atlas-database) Cloud service, which offers a free tier (M0), which is known to work well with the MongoDB Sync Connector.

## Separate MongoDB Instance for Testing

It's highly recommended to use a separate MongoDB instance for testing the ObjectBox Sync Connector. Only once everything is working and tested, switch to a MongoDB instance for production.

It's common to start with a local MongoDB instance during the development process for quick roundtrips and tests.   

## Ensure that your MongoDB instance is a Replica Set

{% hint style="info" %}
**MongoDB Atlas clusters** are already replica sets, no additional configuration is required.
{% endhint %}

If you use a local MongoDB instance (e.g. a local instance or via Docker), it likely isn't a replica set yet.
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

## Prepare a user account for the MongoDB Sync Connector

It is recommended to use a separate MongoDB user account for the MongoDB Sync Connector. To create a MongoDB user account, see [MongoDB User Accounts](https://www.mongodb.com/docs/manual/tutorial/create-users/). Ensure that the user account has read and write access to the database and collections that you want to synchronize.

Note: the ObjectBox Sync Connector will store a few small metadata documents in a collection `__ObjectBox_Metadata`. So please allow read/write access to this collection, too.

Once the user account is set up, you can get the MongoDB connection URL for the [ObjectBox Sync Connector setup](objectbox-sync-connector-setup.md), which is the next step.