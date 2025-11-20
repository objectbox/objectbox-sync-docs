---
description: >-
  Read on for some practical hints on how to sync with MongoDB efficiently and
  robustly.
---

# Performance & Best Practices

## Transactions

When doing multiple database write operations at once, you should always use [transactions](https://docs.objectbox.io/transactions). For example, it's **much more efficient** to do 10 operations in a single transaction than doing these 10 operations in 10 separate transactions. This is a general rule applying to most databases and is especially true for ObjectBox and even more so for ObjectBox Sync.

Inside an ObjectBox transaction, you can write large quantities of objects in any order: ObjectBox is known for its extremely high CRUD performance and you likely won't run into bottlenecks. But when syncing to MongoDB, you may want to consider some technicalities of MongoDB for the best results. Thus, to avoid surprises later, use transactions (on the ObjectBox client) and consider the following rules inside a transaction:

* Most importantly, try to **avoid switching object types** for write operations often.\
  MongoDB is faster for consecutive operations of the same type (collection).\
  Example: instead of writing 100 pairs of `Person` and `Address` in a loop, first write all 100 `Person` objects and then all 100 `Address` objects.
* If possible, keep `put` operations separate from `remove` operations.\
  Example: let's say we replace 100 `Address` objects with new ones. Instead of deleting one `Address` and inserting a new `Address` in a loop, first remove all 100 `Address` objects before inserting the 100 new `Address` objects.
* The more objects you process, the more important the above recommendations get. You will most likely get away with breaking the rules with a few dozen objects without any consequence. But when processing several thousand objects in the "wrong" order, the consequences may become notable. Changes will likely be applied to MongoDB with notable delays (e.g. several seconds). In extreme cases, you may even run into MongoDB transaction timeout errors (60 seconds is the MongoDB default).

{% hint style="info" %}
**Background info:** ObjectBox is an embedded database and has practically **zero latency** for write operations within a transaction. On the other hand, MongoDB, like many databases that operate on a network, has a significant latency per operation caused by networking and internal processing. The latency is typically in the millisecond range. It only becomes noticeable when doing lots of operations, e.g. with a thousand operations, milliseconds literally become seconds. Thus, it's important to keep the number of operations low for optimal MongoDB performance. This can be achieved by considering the guidelines above: the ObjectBox Sync Connector will handle the technical details.
{% endhint %}
