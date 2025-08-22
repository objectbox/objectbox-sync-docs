---
description: >-
  Offline-first out-of-the-box Data Sync for the ObjectBox database. Seamless,
  bi-directional, selective data flows across devices, offline as well as
  online, is simplified with ObjectBox Data Sync.
---

# Data Synchronization

Welcome to the official documentation for **ObjectBox Sync**!

{% hint style="info" %}
To learn more about the ObjectBox **database**, have a look at its [website](https://objectbox.io/offline-first-mobile-database/).
{% endhint %}

In a nutshell, here are the **three steps to start with ObjectBox Sync**:

1. Set up your data model using one of the [ObjectBox Sync Client](sync-client.md) language bindings (Java, Dart, Swift, C, ...) to get a data model JSON file.
2. [Start the server](sync-server/) using the data model file.
3. Point your sync client to the server URL to start syncing.

Please use the navigation on the left for more detailed information.

{% hint style="info" %}
Prefer to look at example code? Check out [our examples repository](https://github.com/objectbox/objectbox-sync-examples).
{% endhint %}

What follows is an overview of how the Sync feature works.

## Sync Architecture

<figure><img src=".gitbook/assets/Sync Architecture for Docs.jpg" alt="ObjectBox Sync Architecture Diagram"><figcaption><p>Figure 1: ObjectBox Sync Architecture Overview</p></figcaption></figure>

## Sync Concepts

Typically you **interact with your local ObjectBox database**. It does not matter if the device is online or offline. You get and put objects using the regular ObjectBox APIs. If you are interested in details on how this is done, please refer to the language binding of your choice:\
[Java/Kotlin](https://docs.objectbox.io/), [Swift](https://swift.objectbox.io/), [Go](https://golang.objectbox.io/), [C++](https://cpp.objectbox.io/), [Dart/Flutter](https://github.com/objectbox/objectbox-dart) (beta), [Python](https://github.com/objectbox/objectbox-python) (alpha).

The same APIs apply to synced objects, e.g. you use the same `put` call on a synced object as you would do for any (non-synced) object. Under the hood however, ObjectBox will synchronize those objects to their destination device, e.g. some server. Thus, those objects will become available outside of originating device.

### Online, Offline, :person\_shrugging:

When you write applications with ObjectBox Sync, it does not matter if the device is online or offline. You work with the objects that you have at hand and let ObjectBox Sync manage the synchronization process. But what does this entail?

So, let's look a bit behind the scenes. Whenever you change data (on sync-enabled types), ObjectBox **tracks these changes** and stores them safely in an **outgoing queue**. In the background, ObjectBox Sync tries to connect to the data synchronization destination (Sync server). If the connection was successfully established, the outgoing queue is "processed". This means that enqueued data is sent, and once the sync destination acknowledges the receipt, that piece of data can be safely removed from the queue.

When disconnected, Sync clients will **periodically try to reconnect** in the background. By default, this is done using increasing backoff intervals. While details may change, the backoffs should stay similar to this sequence \[seconds]: 0.5, 1, 2, 4, 8, 15, 30, 30, 60. This closely resembles an exponential backoff, but also ensures not to delay a (re-)connection attempt for longer than one minute.

### Delta synchronization

When you look at typical REST applications, an often used pattern is that clients request all data from the server. This happens regardless of any previous interaction, often because it is a simple approach and avoids complex caching strategies (of course you are aware of the 3 hard problems in software: cache invalidation and off-by-one errors). Needless to say that this is not the most resource-efficient setup as it involves redundant data processing and sub-optimal network traffic.

ObjectBox Sync does not follow the request-response paradigm. Instead, it **pushes changes**. This has several advantages like significantly reducing traffic while using less computing resources. Also, this enables "real-time" data updates out of the box.

### Networking

ObjectBox Sync exchanges **messages** over the network. You do not interact with messages directly, but it is good to remember that; e.g., you may see some message-related charts in Sync statistics.

**WebSockets** is the standard protocol ObjectBox Sync uses to exchange messages. It borrows some advantages from HTTP for the handshake (e.g., usually plays nice with firewalls), while providing TCP-like properties. Thus, unlike HTTP, WebSockets enables fast two-way push communication. It also scales nicely: we have tested with hundreds of thousands of concurrent clients connected to a single ObjectBox Sync server.

While WebSockets is a great match for ObjectBox Sync for most cases, we are not strictly bound to it. Internally, we have a network abstraction layer, which allows us to quickly adapt to special networking requirements like supporting LoRaWAN or other non-IP based protocols. Reach out to us if you are interested.

### Robust data synchronization

Sync is tightly integrated with the ObjectBox database. When you put an object in the database, this always happens inside a [database transaction](https://en.wikipedia.org/wiki/Database_transaction). This is great to ensure that your data is always consistent. A notable feature of ObjectBox Sync is that it uses **the same database transaction** for metadata used by synchronization. Thus, this high level of consistency extends to Sync, as Sync metadata cannot diverge from the actual data.

OK, this may sound a bit abstract, so let's look at an example. Let's say device A is constantly computing data based on a never-ending stream of sensor data. Also, that computed data is synced to an edge gateway B. Now at any point in time, device A suddenly loses power. Don't worry, your data is safe and consistent. Transactions ensure that the state on device A is consistent with what will be synchronized to gateway B. ObjectBox takes care of all that; no matter if A and B were connected to each other or whatever the synchronization state was at the point when the power went out. Once device A boots up again, ObjectBox will synchronize data to gateway B from the point it was interrupted.

## Future Sync

Our vision of providing data where it's needed, when it's needed, goes way beyond what we have already implemented. We encourage you to contact us and be part of that exciting journey. We will listen to where you want to go; let us provide the infrastructure so you can focus on your core product.
