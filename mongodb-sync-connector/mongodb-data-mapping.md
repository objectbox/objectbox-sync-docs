---
description: >-
  Ensure smooth data synchronization between MongoDB and ObjectBox by correctly
  mapping data and types.
---

# MongoDB Data Mapping

The data model used by ObjectBox defines types, which are mapped to MongoDB collections. Similarly, the properties of a type are mapped to keys inside a MongoDB document. Thus, you should **ensure that the ObjectBox data model matches the MongoDB schema**. For example, if you have an existing MongoDB database, ensure to match the names when you create the ObjectBox model.

## Objects and Documents

When you compare the data structure of simple data elements, the difference is not significant. Without nested data, the main difference you will note is the ID type.

<figure><img src="../.gitbook/assets/ObjectVsDocument (1).png" alt="Comparison of ObjectBox Object and MongoDB Document structure" width="563"><figcaption><p>Figure 1: ObjectBox Object vs. MongoDB Document (Simplified)</p></figcaption></figure>

Note: nested documents are supported via the ObjectBox "Flex" property type, which can hold a map-like (JSON-like) structure. We are also considering alternatives to this, so please let us know if you have specific requirements.

## ID mapping

ObjectBox Sync automatically maps IDs when syncing with an external system like MongoDB. This way, you can use the native IDs in each system: 64-bit integer IDs in ObjectBox and, for example, 12-byte object IDs in MongoDB. This also means that the MongoDB ID is not present in ObjectBox objects and vice versa.

{% hint style="warning" %}
ObjectBox IDs are only valid on their local device. Do not store them manually (apart from relations) e.g. as a custom list or vector, when you want to sync to other devices.\
For details, you can refer to the [internal ID mapping docs](../data-model/object-ids.md) that occurs on each ObjectBox device.
{% endhint %}

Besides the Object ID, ObjectBox supports most common ID types offered by MongoDB. IDs of **incoming documents from MongoDB** are automatically detected and mapped to ObjectBox local IDs. This mapping is persisted, and thus any change made on the ObjectBox side can be mapped back to the initial ID type and value.

For **newly created (inserted) objects on the ObjectBox side,** a new MongoDB object ID (OID) is created by default. You can customize the MongoDB ID types in the ObjectBox data model: for the ID property, define an "external property type" on the ID property. Then, ObjectBox will create a new UUID-based ID for the MongoDB document. 

{% tabs %}
{% tab title="Java" %}
```java
@ExternalType(ExternalPropertyType.UUID)
private byte[] externalId;
```
Recommended types for IDs: `UUID` (UUIDv7), `UUIDString` (UUIDv7 as string), `UUIDV4`, `UUIDV4String`.
{% endtab %}

{% tab title="Swift" %}
```swift
// objectbox: externalType="uuid"
var externalId: Int
```

Recommended types for IDs: `uuid` (UUIDv7), `uuidString` (UUIDv7 as string), `uuidV4`, `uuidV4String`.
{% endtab %}

{% tab title="Dart/Flutter" %}
```dart
  @Id()
  @ExternalType(type: ExternalPropertyType.uuid)
  int id = 0;
```

Recommended types for IDs: `uuid` (UUIDv7), `uuidString` (UUIDv7 as string), `uuidV4`, `uuidV4String`.
{% endtab %}
{% endtabs %}

The following table shows the supported ID types:

<table><thead><tr><th width="198.5333251953125">MongoDB type</th><th width="216.6998291015625" align="center">Incoming from MongoDB</th><th align="center">IDs for new documents created in ObjectBox</th></tr></thead><tbody><tr><td>Object ID</td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span><br>This is the default type</td></tr><tr><td>UUID (Binary with UUID subtype)</td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span><br>External types: Uuid (V7) or UuidV4</td></tr><tr><td>String</td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span><br>External types: UuidString (V7) or UuidV4String</td></tr><tr><td>Binary</td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td align="center">Uses default MongoDB Object ID</td></tr><tr><td>Int64</td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td align="center">Uses default MongoDB Object ID</td></tr><tr><td>Int32</td><td align="center"><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td><td align="center">Uses default MongoDB Object ID</td></tr></tbody></table>

## To-One Relations

{% hint style="info" %}
If you want to learn more about ObjectBox relations, check the [relation documentation](https://docs.objectbox.io/relations).
{% endhint %}

ObjectBox Sync also automatically maps IDs used in relations (starting with version Alpha 3 of MongoDB Sync Connector).

Consider ObjectBox to-one relations, which have a single relation property pointing to another object using a 64-bit integer ID. This becomes a reference field in MongoDB's document containing the MongoDB object ID (OID). See the following illustration for an example:

<figure><img src="../.gitbook/assets/ObjectVsDocument-Parent (1).png" alt="To-One Relationship Example: motherId mapping" width="563"><figcaption><p>Figure 2: To-One Relationship Example (motherId)</p></figcaption></figure>

The supported ID types also apply for relations. For example, if a "Person" document uses a UUID as its `_id` field value, relations to it would also use the UUID as the relation ID on the MongoDB side.

## Many-to-Many Relations

Many-to-many relations work a bit differently. As illustrated in the table above, many-to-many relations work differently in ObjectBox and MongoDB. For mapping between them, the following rules apply:

* On the MongoDB side, many-to-many relations are stored as an array of ID references:
  * The IDs are stored inside the document "owning" the relationship.
  * The owning side of a relationship is always the same type (collection).
  * If you want to, you can make this relation bidirectional by adding IDs to the "target side" of the relationship. Do not make this visible in the ObjectBox data model.
* On the ObjectBox side, its native many-to-many relationships are used:
  * They are bidirectional, e.g. you can define it on the owning and target side.
  * They can be updated efficiently without touching the object.
  * They can be used in queries to link types (aka join).

As to-many relations consist of ID values, all supported types can be used. In theory, different ID types can be used in the same to-many relation. However, it is usually good practice to stick to a single ID type per MongoDB collection if possible.
