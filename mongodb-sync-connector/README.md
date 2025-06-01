---
description: Bi-directional Data Sync with MongoDB - on-premise and to the cloud
---

# MongoDB Sync Connector

ObjectBox Data Sync syncs data with MongoDB using the integrated [MongoDB Sync Connector](https://objectbox.io/mongodb/). Changes made on ObjectBox clients are synchronized in real-time to MongoDB and vice versa.

{% hint style="info" %}
[Get your MongoDB Sync Connector Alpha](https://objectbox.io/mongodb/)
{% endhint %}

## Bi-directional Synchronization with MongoDB

<figure><img src="../.gitbook/assets/ObjectBox-Mongo-Architecture-Central.webp" alt="Architecture: MongoDB <--> ObjectBox Sync Server <--> ObjectBox Sync Client"><figcaption><p>ObjectBox Sync Connector for MongoDB: Architecture</p></figcaption></figure>

ObjectBox Sync brings your data in MongoDB to the edge (e.g. mobile and IoT devices, big and small servers) and synchronizes changes back to MongoDB. By using ObjectBox Sync, you can make your MongoDB data always available: continue to work offline and sync in real-time when online.

## Roadmap

If you are coming from Atlas Device Sync, you already now that it [reaches its end-of-life](https://www.mongodb.com/docs/atlas/app-services/deprecation/) on **September 30, 2025**. Thus, it's a good idea to [contact ObjectBox asap](https://objectbox.io/mongodb/) to get started with your migration.

While ObjectBox Sync is an established product, the MongoDB Connector is in its early stages. You can still get started with POCs or integrations right away. The timeline below enables you to align your development with ours and pick up speed. Once new features are out, you profit immediately.

<table><thead><tr><th width="134.93328857421875">Planned Date</th><th width="94.73333740234375" align="center">Released</th><th width="148.5333251953125">Connector Version</th><th>Main features</th></tr></thead><tbody><tr><td>Oktober 2024</td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td>Alpha 1</td><td>Two-way sync between MongoDB and ObjectBox for changes that are happening live.</td></tr><tr><td>January 2025</td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td>Alpha 2</td><td>JWT authentication, Mapping for all MongoDB data types</td></tr><tr><td>February 2025</td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td>Alpha 3</td><td>Relation mapping (to-one and many-to-many)</td></tr><tr><td>March 2025</td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td>Alpha 4</td><td>Support for additional MongoDB ID types</td></tr><tr><td>April 2025</td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td>Alpha 5 (2025-04-01)</td><td>Use MongoDB transactions, better change tracking, improved error handling, improved MongoDB Admin page</td></tr><tr><td>May 2025</td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td>Beta 1<br>(2025-05-05)</td><td>Import initial data from MongoDB, pick-up sync at any point. New admin page for full-syncs.</td></tr><tr><td>End of May 2025</td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td>Beta 2</td><td>Sync trials via public Docker images, map nested documents to JSON string</td></tr><tr><td>June 2025</td><td align="center"></td><td>Beta 3</td><td>Server-side rules to select data for sync per user</td></tr><tr><td>July 2025</td><td align="center"></td><td>1.0</td><td>Initial release incorporating most important user feedback</td></tr></tbody></table>

We'll update the plan regularly.

## Understanding ObjectBox and MongoDB

ObjectBox and MongoDB have many similarities. Nevertheless, it's important to understand some differences in terminology and concepts between the two databases. The following table illustrates these differences. It serves as background information on how to map things between the two systems:

<table><thead><tr><th width="186">Concept</th><th>ObjectBox</th><th>MongoDB</th></tr></thead><tbody><tr><td><strong>Database</strong> containing the data</td><td>A <strong>store</strong>, grouped into types (data classes).</td><td>A <strong>database</strong>, grouped into collections.</td></tr><tr><td><strong>What your application "opens"</strong></td><td>Using a name or directory a single store (database) is opened locally on device. (In the case of Sync, this is the "client database".)<br>Multiple stores can be opened, which are strictly separate.</td><td>A client is used to connect to a MongoDB server. All databases can be accessed on the server remotely.</td></tr><tr><td><strong>Arranging data in a database (e.g. data sets)</strong></td><td>A <strong>box</strong> holds all objects of the same <strong>type</strong>. A type typically matches a data class in programming languages.<br>It's part of a <strong>strict schema</strong> (data model) that is enforced. The type definition consists of a fixed set of <strong>properties</strong>.</td><td><strong>Collections</strong> are used to group documents together. By default, no strict rules are imposed (<strong>schema-less</strong>).</td></tr><tr><td><strong>Data record</strong></td><td>An <strong>object</strong> is an instance of a type. It can have data values for the <strong>properties</strong> defined in the type.</td><td>A <strong>document</strong> is a set of data values called <strong>fields</strong>. It's very similar to a JSON file.</td></tr><tr><td><strong>Modelling related data</strong></td><td>Objects can have <strong>to-one and to-many relationships</strong> to other objects. Relationships are bidirectional. Data is typically <strong>normalized</strong>.</td><td>Typically, a document <strong>embeds</strong> all "related data" into itself resulting in larger documents. Data is typically <strong>not normalized</strong>. Alternatively, one can also choose to use references, which is more similar to relationships.</td></tr><tr><td><strong>Many-to-many relationships</strong></td><td><strong>Fully supported</strong>. Unlike to-one relationships, the data is stored <strong>outside the object</strong>. Updating relations is very <strong>efficient</strong>. There's <strong>no user-defined order</strong> and <strong>no duplicates</strong>.</td><td><strong>Alternative modelling</strong> by embedding or referencing documents. <strong>Inside the document</strong>, you can have an array of IDs in a <strong>user-defined order</strong> allowing <strong>duplicates</strong>.</td></tr><tr><td><strong>Nested data records</strong></td><td>Nested data is supported by <strong>flex properties.</strong> E.g. these allow maps, which can contain nested data structures (JSON-like).</td><td>Documents contain nested data <strong>by default</strong>.</td></tr><tr><td><strong>Identifiers (IDs)</strong></td><td>IDs are <strong>64-bit integers.</strong><br>They are unique within its box and database instance.</td><td>MongoDB uses <strong>Object ID</strong> (short: OID; 12 bytes) by default and supports other ID types. OIDs are unique within their collection and likely globally unique.</td></tr></tbody></table>

## Next Steps

* Setup a MongoDB instance, either locally or in the cloud.
* Setup an ObjectBox Server instance and configure the MongoDB Sync Connector.
* Import data from MongoDB to ObjectBox initially.
* Now, two-way data synchronization between MongoDB and ObjectBox automatically happens.
