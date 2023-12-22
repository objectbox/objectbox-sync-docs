---
description: How to manage a growing data model (schema).
---

# Data model evolution

The structure of the data stored by ObjectBox is described by a data model, sometimes also called a schema. The separation of the model and the data allows ObjectBox to work more efficiently and robustly with data. It's similar to objects of strongly typed languages, so you know exactly with what data (types) you are dealing with.

{% hint style="info" %}
This section refers mostly to the standard object model provided by ObjectBox. There are alternative ways to model data in ObjectBox, e.g. generic trees and "flex buffers", that can be used to represent flexible data models ("schema-less").
{% endhint %}

## Managing data model versions

In the [Sync Server docs](objectbox-sync-server.md), you already saw data models in action. The server initially needs the JSON file containing the data model to start. Over time this data model will evolve. New types and properties will be added, and sometimes old ones will be retired. The ObjectBox Sync Server tracks these versions and helps you manage clients using different model versions.

Let's say you have a new client version of your application that also introduced new properties to a type. To prepare that for synchronization, you need to upload the updated data model to the server. This is done by the admin web UI - in "Schema Versions" section, click "New Version" button in the right and you'll get an upload dialog.&#x20;

![](<.gitbook/assets/image (8).png>)

You can add the new ObjectBox model JSON file by clicking on the "Schema model JSON" text in the dialog. After a file is selected, the dialog window shows some preliminary information about the model, click Save to add the model version SyncServer.&#x20;

![](<.gitbook/assets/image (6).png>)

The newly added model isn't active yet, you can switch the server to use it by clicking the "Change current version ID" button, which shows the dialog with version selection (if there re multiple possible options):

![](<.gitbook/assets/image (4).png>)

This causes the server to restart with the newly selected model version. Additionally, this disables logins of clients with an incompatible model version
