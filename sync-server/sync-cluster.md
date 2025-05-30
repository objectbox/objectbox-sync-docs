---
description: ObjectBox Sync Cluster for high availability and scalability
---

# Sync Cluster

The ObjectBox Sync Cluster distributes the Sync load among multiple Sync Servers. This setup has two main advantages over a single server setup. First, more servers can be added to scale along e.g. a growing number of clients. Second, availability increases because there's no single point of failure. In case of failure, other servers take over.

## Scalability: Serving Millions

ObjectBox Sync allows you to start quickly and scale with increasing loads. There are two ways to scale:

* **Vertical scaling:** switch to more powerful machines (VMs, cloud instances, etc.). ObjectBox is designed for efficiency and uses a tiny fracture of resources compared to other systems. Accordingly, some vertical scaling (adding computing resources) gets you a very long way. Typically, you want to have fast NVMe drives for the database directory. Depending on your use case, CPU and RAM can have significant effects too.
* **Horizontal scaling:** add more cluster nodes to divide the work. Additional nodes empower serving more clients. Because an ObjectBox cluster node has all information locally, it serves data to clients without contacting other nodes. Thus, the scaling is practically linear.

### Read vs. Write

Within a cluster, ObjectBox Sync has a strictly consistent approach. This is achieved by different node types. By default, a cluster node is a "follower". All follower nodes get new data from the "leader" node. Once that happens, all followers can propagate the new data to their clients (read). When clients have new data (write), a follower will forward the data to the leader. Thus, the leader can take care of consistency since it can coordinate all incoming data. A great side effect of this is that the leader can batch data together, making data updates very efficient.

## Prerequisites

You need to get the Sync Server executable / Docker from ObjectBox. It must also contain the "Cluster" feature (when in doubt, just try it and/or check the Admin UI web app).

## Cluster setup

Typical cluster setups consist of an odd number of servers. For example, three Sync Servers can form a cluster that can compensate one server to be down.

Some general notes:

* Model: all servers need to operate the same model file

### Configuration

The base configuration of the Sync Server is described [here](configuration.md#configuration-file). Using the same configuration file, these are the Cluster specific options:

```json
{
    // ... Standard config as described in "ObjectBox Sync Server" goes here
    
    "clusterId": "myCluster",
    "serversToConnect": [
        {
            "uri": "ws://1.2.3.4:5678",
            "credentialsType": "SHARED_SECRET",
            "credentials": "securePassword"
        },
        {
            "uri": "ws://1.2.3.5:6789",
            "credentialsType": "SHARED_SECRET",
            "credentials": "securePassword"
        }
    ]
}
```

* `clusterId`: an identifier for the cluster. It's an arbitrary string and has to be the same on all servers involved in a cluster.
* `serversToConnect`: for each server, the other servers of the cluster must be specified here. Each entry can specify the following fields:
  * `uri` (required): the URI of the Sync Server; which has to be a WebSocket URI
  * `credentialsType` is required (unless you are using unsecuredNoAuthentication) and should be `SHARED_SECRET_SIPPED`.
  * `credentials` (required): given `credentialsType`, this is actual secret.

{% hint style="info" %}
**Note:** while most of the options can be specified either in the Sync Server command line and in the JSON file, the `serversToConnect` options is JSON file only. Thus, if you want to configure clustering for your Sync Server, please use a JSON configuration file as [described here](./#configuration-file).
{% endhint %}

## Overview of the clustering architecture

The ObjectBox clustering mechanism roughly implements the [Raft consensus algorithm](https://en.wikipedia.org/wiki/Raft_\(algorithm\)).

When establishing the cluster, it elects a leader node that is responsible for the Sync History, while other nodes will be identified as followers. The leader election is performed using a voting system: the candidate node that gathers the majority of votes becomes the leader.

A peer can therefore be in 3 different states: **leader**, **follower** or **candidate** (only during election).

After the leader is elected, it starts sending heartbeats to the follower nodes to notify them of its availability. When the followers stop receiving heartbeats from the leader (e.g. because the leader is down), the election takes place again.

The Sync Client changes are sent either to a follower node or to a leader node. If it's a follower node, the changes are not processed and forwarded to the leader node. The leader node synchronizes its followers to make sure they all share the same state and commits the changes to its own Sync History.

### Visualize the cluster activity

The Sync Cluster page of ObjectBox Admin web app helps you to visualize the Cluster activity and possibly debug your configuration and the network connection.

<figure><img src="../.gitbook/assets/image.png" alt=""><figcaption><p>Sync Cluster page from Admin UI</p></figcaption></figure>

In the top panel of the Admin app, you will find general information on the current Sync Server:

<figure><img src="../.gitbook/assets/image (1).png" alt=""><figcaption><p>General information of the Sync Server</p></figcaption></figure>

Below the Admin app top panel, follow two tables that show the peers of the current Sync Server.

The first table lists all the **client** peers: these are the other Sync Server(s) that are connected to the current one. In the image, we can see that the current Sync Server has other two Sync Server(s) connected to it.

<figure><img src="../.gitbook/assets/image (2).png" alt=""><figcaption><p>Client peers table</p></figcaption></figure>

While the second table lists the **connected peers**:

<figure><img src="../.gitbook/assets/image (3).png" alt=""><figcaption><p>Connected peers table</p></figcaption></figure>
