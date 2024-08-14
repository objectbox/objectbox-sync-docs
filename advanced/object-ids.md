---
description: >-
  ObjectBox Sync offers local and global ID spaces. Understand the implications
  and what's best for your use case.
---

# Object IDs and Sync

## Default Behavior: ID mapping

Let's say we have a shared to-do list app on two devices connected via ObjectBox Sync. On Device A, Alice inserts a new task "Buy milk" and Bob on device B inserts another task "Feed the cat". Using the default ID mechanism, ObjectBox keeps assigning IDs starting from 1. Let's also assume device B is currently offline and thus does not sync the data just yet. In that case, each device has only its local object as illustrated by the following table:

| <p>Tasks on device A</p><p>ID:text</p> | <p><em>Tasks on device B</em></p><p><em>ID:text</em></p> |
| -------------------------------------- | -------------------------------------------------------- |
| 1:"Buy milk"                           | _1:"Feed the cat"_                                       |

As you can see, the two tasks have the same ID 1 **locally**. Now, what happens if both devices sync each others data? As the tasks are distinct (different from each other), one may assume that both devices each have two tasks. And this is exactly what happens. The table now looks like this:

| <p>Tasks on device A</p><p>ID:text</p> | <p><em>Tasks on device B</em></p><p><em>ID:text</em></p> |
| -------------------------------------- | -------------------------------------------------------- |
| 1:"Buy milk"                           | _1:"Feed the cat"_                                       |
| 2:"Feed the cat"                       | _2:"Buy milk"_                                           |

{% hint style="info" %}
Each ObjectBox Sync client has its own **local ID space**.
{% endhint %}

Each device added a task with the next locally available ID (her it's ID 2 for both). Thus IDs are local to the device (or more accurately per store) and may differ from device to device while addressing the same object.

{% hint style="info" %}
Under the hood, ObjectBox Sync uses a global addressing scheme and **ID mapping** mechanisms. This is transparent to you.
{% endhint %}

### Object Relations and IDs

ObjectBox expresses relations between objects using (object) IDs. When object IDs get mapped, so do the IDs used in relations. On the local device, this is transparent to you.

**Example:** let's say tasks are organized into folders. This is a one-to-many relation in which the `Task` object has a reference to its `Folder` object it is contained in. On one device, we have a "Shopping list" folder with ID 23, and a task "Broccoli" with ID 47. To make the "Broccoli" task part of the "Shopping list" folder, let's assume that there is a `folderId` property in the `Task` type, which would carry the value 23. Since IDs on another device will be different (mapped), you will see also the relations mapped to different IDs. The following table shows the same Task object on two separate devices with example ID values:

| Device | Task: ID | Task: text | Task: folderId |
| ------ | -------- | ---------- | -------------- |
| A      | 47       | Broccoli   | 23             |
| _B_    | _81_     | _Broccoli_ | _104_          |

{% hint style="warning" %}
IDs used in relations are automatically mapped. Do not reference objects using IDs in non-relation properties (e.g. using a long integer, or in a textual list, embedded JSON etc.).
{% endhint %}

## Shared Global IDs

Local IDs with an internal ID mapping as illustrated in the previous section are the default in ObjectBox. As a rule of thumb, you should stick to ID mapping, e.g. to avoid ID collisions causing unrelated objects to overwrite each other.

{% hint style="danger" %}
When in doubt, use the default (ID mapping).\
Using shared global IDs incorrectly may cause data being lost.
{% endhint %}

However, if you can somehow ensure unique 64 bit IDs over all devices, you can opt to use "shared global IDs". (Again, this doesn't change IDs to a GUID-like type - ObjectBox always addresses objects with a 64 bit ID.) An example could be base data, that an single instance is managing.

On the positive side, shared global IDs do not require additional ID mapping information and thus are a bit more efficient.

Shared global IDs are a property of entity type. Thus you can specify the ID behavior selectively for types, e.g. have some types with the default ID mapping and other types with shared local IDs.

To enable shared global IDs for a type, use this annotation on the type (class) definition in your code:

{% tabs %}
{% tab title="Java" %}
```java
@Sync(sharedGlobalIds = true)
```
{% endtab %}

{% tab title="Dart" %}
```dart
@Sync(sharedGlobalIds: true)
```
{% endtab %}

{% tab title="Swift" %}
```
// objectbox: sync = { "sharedGlobalIds": true }
```
{% endtab %}
{% endtabs %}

{% hint style="danger" %}
You define the ID behavior for a type once when you introduce a type.\
You cannot change it later.
{% endhint %}
