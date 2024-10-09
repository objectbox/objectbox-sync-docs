---
description: An overview of the Sync Server mechanisms and capabilities.
---

# Sync Server Evaluation

## Introduction

_<mark style="color:purple;">Capability of the sync server to handle data synchronization between devices.</mark>_

The ObjectBox Sync Server is the main component that comes into play for the ObjectBox Sync feature. It is responsible for handling multiple connected clients and for making sure they all share the same state (i.e. equal database).

Also the Sync Server, in addition to the clients, is provided with a **local database** which is kept up-to-date with the clients' updates. This is usually a _passive_ database, in the sense that it's meant to hold the state of the network and it's not directly modified by the user. Nevertheless nothing stops you from editing it as it was a sync client database (see the [Embedded Sync Server](advanced/embedded-sync-server.md) setup).&#x20;

When a Sync Client connects and logins, the Sync Server subscribes it for receiving new data updates. These are **push updates**, and thus are efficiently performed without involving any prior request by the client. Push updates are also [**pipelined**](#user-content-fn-1)[^1], which means they are sent in burst without waiting for single ACKs.

_<mark style="color:purple;">Determination as to how sync operates in various conflict scenarios.</mark>_

The Sync Server activity ensures a consistent data history. A "last write wins" policy is employed to make sure the sync server holds a linear history.

### **Fault tolerance**

_<mark style="color:purple;">How well does the client <-> sync server model work for various scenarios mimicking real world usage.</mark>_

ObjectBox Sync Server, as well as other ObjectBox components, is internally tested with a large suite of unit- and integration-tests. This helps us putting it in several real world scenarios to check its resilience.\
However, we don't exclude the possibility of not having covered specific use cases; and we kindly invite you to report any issue to the ObjectBox team.

Common scenarios could be:

* **A client goes offline**: It would still be able to commit changes to its local database. These changes are enqueued in the sync queue and will be eventually sent when the connection is (re-)established. The sync server is responsible for aligning the sync client's state with its state.
* **The Sync Server goes offline**: Synchronization wouldn't work anymore, every client would still write to its local database and enqueue changes to the sync queue. Once the sync server is back online,  it will work to reach a commonly agreed state. To better tolerate this scenario you may be interested at [ObjectBox Sync Cluster](sync-cluster.md) solution.

Moreover:&#x20;

* **Reliable transport layer**: Sync messages are carried over a TCP transport layer which guarantees a reliable communication. We also provide an additional reliability layer by using per-transaction ACK messages; to make sure the client correctly performed the operation.
* **Use of **_**heartbeat**_** packets**: Every client periodically sends an _heartbeat_ packet, in this way the sync server is readily able to notice when a client dies and act subsequently.

## Performance

_<mark style="color:purple;">Speed and efficiency of data synchronization between devices via the sync server.</mark>_

<table data-view="cards" data-full-width="false"><thead><tr><th align="center"></th></tr></thead><tbody><tr><td align="center">Delta synchronization<br><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td></tr><tr><td align="center">Push updates<br><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td></tr><tr><td align="center">Custom binary protocol<br><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td></tr><tr><td align="center">Pipelining<br><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td></tr></tbody></table>

Sync servers leverage several features to provide a resource-efficient and fast data synchronization:

* **Delta synchronization**: Instead of exchanging complete data, it only deals with changes (less data).
* **Push updates**: As soon as a new data update is received, it broadcasts to all connected clients. Without waiting for the latter to request it.
* **Pipelining**: Multiple pushes are grouped together and sent in burst, without waiting for single ACKs.
* **Custom binary protocol**: Above the transport layer (of your choice, default WebSockets), we've implemented a custom binary protocol aimed at representing messages efficiently.

## Security

_<mark style="color:purple;">Security measures implemented during data synchronization between devices.</mark>_

_<mark style="color:purple;">How complete and potentially expandable is the security model.</mark>_

<table data-view="cards"><thead><tr><th align="center"></th></tr></thead><tbody><tr><td align="center">WebSocket Secure (wss)<br><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td></tr><tr><td align="center">Sync Client authentication<br><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td></tr></tbody></table>

By default, the ObjectBox Sync protocol is carried over the WebSocket protocol. We also support secure communication by using **WebSocket Secure** (wss; i.e. WebSocket over TLS).

The Sync Server also provides different **authentication** methods for Sync Clients that can be either set to: **shared secret** or **Google sign-in**.

In general, our code base is extendable; both for the transport layer and authentication method. The ObjectBox Team is open-minded for your suggestions and eventually add support for further protocols or authentication methods.

## Troubleshooting

_<mark style="color:purple;">Quality and availability of development tools provided</mark>_

<table data-view="cards"><thead><tr><th align="center"></th></tr></thead><tbody><tr><td align="center"><p>Admin UI</p><p><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></p></td></tr><tr><td align="center"><p>Debug logging</p><p><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></p></td></tr><tr><td align="center">ObjectBox support<br><span data-gb-custom-inline data-tag="emoji" data-code="2705">✅</span></td></tr></tbody></table>

You can troubleshoot and monitor the sync server activity using [ObjectBox Admin](objectbox-sync-server.md#admin-web-ui).

Sync Server Admin UI is provided with additional pages that aren't featured in the standard Admin UI. These pages will give you a first impression whether your sync server is correctly configured and to identify any malfunction:

* **Schema Versions**: A page that shows loaded schemas and permits you to switch the currently enabled schema (clients having incompatible schemas won't be able to connect).
* **Sync Statistics**: To have a general view over the activity of the sync server.
* **Sync History**: To troubleshoot the sync history.
* **Sync Cluster (requires Cluster feature)**: Information regarding the [Object Box Cluster](sync-cluster.md) setup for the current peer.

To go more in detail, you may be interested in enabling **Logging**, as [described here](objectbox-sync-server.md#logging).

If you can't figure out what's wrong in your setup, just contact us! :slight\_smile:

[^1]: 
