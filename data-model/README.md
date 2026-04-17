---
description: How to manage a growing data model (schema).
---

# Data model

The structure of the data stored by ObjectBox is described by a data model, sometimes also called a schema. The separation of the model and the data allows ObjectBox to work more efficiently and robustly with data. It's similar to objects of strongly typed languages, so you know exactly with what data (types) you are dealing with.

{% hint style="info" %}
This section refers mostly to the standard object model provided by ObjectBox. There are alternative ways to model data in ObjectBox, e.g. generic trees and "flex buffers", that can be used to represent flexible data models ("schema-less").
{% endhint %}

## Managing data model versions

In the [Sync Server docs](../sync-server/), you already saw data models in action. The server initially needs the JSON file containing the data model to start with. Over time this data model will evolve. New types and properties will be added, and sometimes old ones will be retired. The ObjectBox Sync Server tracks these versions and helps you manage clients using different model versions.

Let's say you have a new client version of your application that also introduced new properties to a type. To prepare that for synchronization, you need to upload the updated data model to the server. This is done via the Admin web UI — in the "Schema Versions" section, click the "New Version" button on the right, and you'll get an upload dialog.&#x20;

![](<../.gitbook/assets/image (8).png>)

You can add the new ObjectBox model JSON file by clicking the "Schema model JSON" text in the dialog. After a file is selected, the dialog window shows some preliminary information about the model; click Save to add the model version to Sync Server.&#x20;

![](<../.gitbook/assets/image (6).png>)

The newly added model isn't active yet. You can switch the server to use it by clicking the "Change current version ID" button, which shows the dialog with version selection (if there are multiple options):

![](<../.gitbook/assets/image (4).png>)

This causes the server to restart with the newly selected model version. Additionally, this disables logins of clients with an incompatible model version.

## Client data models

When clients log in, they send their data model version to the server.
By default, validation is non-strict: clients with unknown schemas can still connect.
You can enable strict validation via the [`clientSchemaValidation`](../sync-server/configuration.md) JSON config object, which rejects clients whose schema is unknown or not enabled on the server.
Use this to ensure that only "compatible" clients can connect to the server; you define what compatible means.
For example, older clients may lack new entity types that are now mandatory for your application to function.

Clients with older schema versions automatically receive only objects of types known to them.
New types added in later schema versions are filtered out during synchronization,
so older clients never encounter unknown data.

A client's data model is identified by the "base hash".
This only captures "essential" information about the model that excludes metadata like indexes.
E.g., when you index a property, the base hash does not change.

### Client Schema tab

The Admin UI includes a "Client Schema" tab on the Schema Versions page.
This gives you an overview of all schema versions used by connected clients, along with usage counts.
Use this to monitor whether all clients connect with known schemas (i.e., schemas that have an ID on the server).
Once all clients use known schemas, you can safely enable strict client schema validation.

