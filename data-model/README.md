---
description: How to manage a growing data model (schema).
---

# Data model

The structure of the data stored by ObjectBox is described by a data model, also called a schema. The separation of the model and the data allows ObjectBox to work more efficiently and robustly with data. It's similar to objects of strongly typed languages, so you know exactly with what data (types) you are dealing with.

{% hint style="info" %}
This section refers mostly to the standard object model provided by ObjectBox. There are alternative ways to model data in ObjectBox, e.g. generic trees and "flex buffers", that can be used to represent flexible data models ("schema-less").
{% endhint %}

## Schema Versions

![](<../.gitbook/assets/schema-versions.png>)

The Admin lets you view and manage schema versions.
All schema versions ever used are listed in the "Schema Versions" tab.
The current version is displayed in bold (typically the latest data model that you use). 

Notable columns:

* Clients allowed: if disabled, clients will be rejected at login if they use this schema version.
  This is independent of the "strict" client schema validation setting, which controls whether clients with unknown schemas are allowed to connect.
* Actions icons: view or download the model JSON file.

## Add a new schema version

In the [Sync Server docs](../sync-server/), you already saw data models in action. The server initially needs the JSON file containing the data model to start with. Over time this data model will evolve. New types and properties will be added, and sometimes old ones will be retired. The ObjectBox Sync Server tracks these versions and helps you manage clients using different model versions.

Let's say you have a new client version of your application that also introduced new properties to a type. To prepare that for synchronization, you need to upload the updated data model to the server. This is done via the Admin web UI — in the "Schema Versions" section, click the "New Version" button on the right, and you'll get an upload dialog.&#x20;

![](<../.gitbook/assets/image (8).png>)

You can add the new ObjectBox model JSON file by clicking the "Schema model JSON" text in the dialog. After a file is selected, the dialog window shows some preliminary information about the model; click Save to add the model version to Sync Server.&#x20;

![](<../.gitbook/assets/image (6).png>)

The newly added model isn't active yet. You can switch the server to use it by clicking the "Change current version ID" button, which shows the dialog with version selection (if there are multiple options):

![](<../.gitbook/assets/image (4).png>)

This causes the server to restart with the newly selected model version.

## Client data models

When clients log in, they send their data model version to the server.
More specifically, clients send two data model hashes to identify their schema version:
the "base hash" and the "full hash".
The "base hash" is a hash of the model's essential information, such as the entities and their properties.
The "full hash" is a hash of the entire model, including metadata like indexes and constraints.

{% hint style="info" %}
If two schema versions have the same base hash, they are considered "data equal" even if their full hashes are different.
E.g., when you index a property, the base hash does not change, but the full hash does.
{% endhint %}

### Client Schema validation

By default, validation is non-strict: clients with unknown schemas can still connect.
You can enable strict validation via the [`clientSchemaValidation`](../sync-server/configuration.md) JSON config object, which rejects clients whose schema is unknown or not enabled on the server.
Use this to ensure that only "compatible" clients can connect to the server; you define what compatible means.
For example, older clients may lack new entity types that are now mandatory for your application to function.

Clients with older (still enabled) schema versions automatically receive only objects of types known to them.
New types added in later schema versions are filtered out during synchronization,
so older clients never encounter unknown data.

You can also set a default schema version for "unknown" clients via the [`clientSchemaValidation`](../sync-server/configuration.md) JSON config object.
This is intended to still support older clients that have gone "off the radar".
For future versions, you should ensure uploading all schema versions used by clients to the server.

### Client Schema tab

![](<../.gitbook/assets/schema-versions-client.png>)

The Admin UI includes a "Client Schema" tab on the Schema Versions page.
This gives you an overview of all schema versions used by connected clients, along with usage counts.
Use this to monitor whether all clients connect with known schemas (i.e., schemas that have an ID on the server).
Once all clients use known schemas, you can safely enable strict client schema validation.
This is recommended to ensure all schema versions are known to the server, i.e., to filter out unknown types.

### Client Schema validation example

Suppose your server has two schema versions uploaded:

| ID          | Version | Base hash   | Full hash   | Clients allowed |
|-------------|---------|-------------|-------------|-----------------|
| 2 (current) | 2       | `ccc...ccc` | `ddd...ddd` | ✅ yes           |
| 1           | 1       | `aaa...aaa` | `bbb...bbb` | ✅ yes           |

Now three clients connect and try to login with their schema hashes:

| Client | Base hash   | Full hash   | Description                                                  |
|--------|-------------|-------------|--------------------------------------------------------------|
| A      | `ccc...ccc` | `ddd...ddd` | Full hash matches ID 2 exactly                               |
| B      | `aaa...aaa` | `eee...eee` | Base hash matches ID 1, full hash differs (e.g. index added) |
| C      | `111...111` | `222...222` | No hash matches any known version                            |

#### Non-strict (default behavior)

No special configuration needed (or `"strict": false`).

```json
{
  "clientSchemaValidation": {
    "strict": false
  }
}
```

| Client | Outcome                                                                                                                                   |
|--------|-------------------------------------------------------------------------------------------------------------------------------------------|
| A      | ✅ Connects. Matched to ID 2 by full hash. Receives all V2 types.                                                                          |
| B      | ✅ Connects. Matched to ID 1 by base hash (the schemas are data-equal). Receives only V1 types.                                            |
| C      | ✅ Connects. No matching version found, but strict is off — client is assigned to the current schema ID 2 and thus receives **all** types. |

This is the most permissive mode defaulting to the latest schema version.
It is useful during development when the data models are still evolving.

#### Strict

```json
{
  "clientSchemaValidation": {
    "strict": true
  }
}
```

| Client | Outcome                                                                       |
|--------|-------------------------------------------------------------------------------|
| A      | ✅ Connects. Matched to ID 2 by full hash. Receives all V2 types.              |
| B      | ✅ Connects. Matched to ID 1 by base hash. Receives only V1 types.             |
| C      | ❌ **Rejected.** No known version matches — the server refuses the connection. |

Use strict mode once you have uploaded all schema versions used by your clients.
The "Client Schema" tab in the Admin UI helps you verify this.

#### Default hash

```json
{
  "clientSchemaValidation": {
    "defaultHash": "bbb...bbb"
  }
}
```

Here `defaultHash` is set to the full hash of V1.

| Client | Outcome                                                                                   |
|--------|-------------------------------------------------------------------------------------------|
| A      | ✅ Connects. Matched to ID 2 by full hash. Receives all V2 types.                          |
| B      | ✅ Connects. Matched to ID 1 by base hash. Receives only V1 types.                         |
| C      | ✅ Connects. Unknown hash, but falls back to V1 via `defaultHash`. Receives only V1 types. |

This is helpful when older clients are already deployed and you cannot upload their exact schema version.
By setting `defaultHash` to a compatible version, those clients can still connect and sync;
without the types that were added after that version.

{% hint style="info" %}
Strict mode and default hash are mutually exclusive. Enabling both will result in an error.
{% endhint %}