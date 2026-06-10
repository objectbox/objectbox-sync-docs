---
description: >-
  How to use ObjectBox Mesh Sync to synchronize Sync clients directly with each
  other without a central Sync Server connection.
---

# Mesh Sync

Mesh Sync lets ObjectBox Sync clients synchronize directly with nearby peers (peer-to-peer, P2P).
It is intended for offline-first apps where devices may meet locally and exchange changes.
Typically, Mesh Sync is complementing the regular Sync Server by providing local sync while no Internet is available.

{% hint style="info" %}
ObjectBox Mesh Sync is currently available as a **preview for Android** (Java/Kotlin and Flutter/Dart).
More platforms will follow; let us know if you are interested.
Please also note that the APIs are still subject to change until the final release.
For a list of current limitations, see [Current Limitations](#current-limitations).
{% endhint %}

## Overview

<figure><img src=".gitbook/assets/mesh-sync.png" alt="ObjectBox Mesh Sync Overview"><figcaption><p>Figure 1: ObjectBox Mesh Sync Overview</p></figcaption></figure>

Mesh Sync forms a local mesh network of devices to synchronize data between them.
It can use different technology stacks, such as Bluetooth (classic and BLE), Wi-Fi (LAN and Wi-Fi Aware) and others.
This allows data to move across devices even if not every device is directly connected to every other device.

Mesh Sync starts and stops together with the `SyncClient` and can coexist with regular Sync Server synchronization.

## Code: Initializing Mesh Sync

These minimal examples create the normal `SyncClient`, attach a mesh configuration and start syncing.
Use the same mesh identifier on all apps/devices that should join the same mesh.

{% tabs %}
{% tab title="Java" %}
```java
import io.objectbox.android.sync.MeshConfig;
import io.objectbox.sync.Sync;
import io.objectbox.sync.SyncClient;
import io.objectbox.sync.SyncCredentials;

SyncClient syncClient = Sync.client(boxStore)
        .url("ws://sync.example.com:9999")
        .credentials(SyncCredentials.none())
        .build();

MeshConfig.builder(context)
        .serviceId("io.objectbox.example.sync.tasks")
        .build()
        .applyTo(syncClient);

syncClient.start();
```
{% endtab %}

{% tab title="Kotlin" %}
```kotlin
import io.objectbox.android.sync.MeshConfig
import io.objectbox.sync.Sync
import io.objectbox.sync.SyncCredentials

val syncClient = Sync.client(boxStore)
        .url("ws://sync.example.com:9999")
        .credentials(SyncCredentials.none())
        .build()

MeshConfig.builder(context)
    .serviceId("io.objectbox.example.sync.tasks")
    .build()
    .applyTo(syncClient)

syncClient.start()
```
{% endtab %}

{% tab title="Dart/Flutter" %}
```dart
import 'package:objectbox/objectbox.dart';
import 'package:objectbox_sync_flutter_libs/objectbox_sync_flutter_libs.dart'
    show createMeshConfig;

final mesh = await createMeshConfig('io.objectbox.example.sync.tasks');

final syncClient = SyncClient(
  store,
  ['ws://sync.example.com:9999'],
  [SyncCredentials.none()],
  mesh: mesh,
);

syncClient.start();
```
{% endtab %}

{% tab title="C++" %}
```cpp
#include "objectbox-sync.hpp"

obx::MeshOptions meshOptions("io.objectbox.example.sync.tasks");

// Provided by a platform SDK or custom transport integration.
meshOptions.registerNetwork(networkSharedPtr);

std::shared_ptr<obx::SyncClient> syncClient = obx::Sync::client(store)
    .url("ws://sync.example.com:9999")
    .credentials(obx::SyncCredentials::none())
    .mesh(std::move(meshOptions))
    .build();

syncClient->start();
```

Note: The C and C++ APIs expose the underlying mesh options, but a platform transport must be registered before creating the Sync client.
Do not use `obx_mesh_opt_network_internal()` directly unless your platform SDK or integration provides the required transport handle.
{% endtab %}

{% tab title="C" %}
```c
#include "objectbox-sync.h"

OBX_sync_options* sync_opt = obx_sync_opt(store);
obx_sync_opt_add_url(sync_opt, "ws://sync.example.com:9999");

OBX_mesh_options* mesh_opt = obx_mesh_opt("io.objectbox.example.sync.tasks");

// Provided by a platform SDK or custom transport integration.
obx_mesh_opt_network_internal(mesh_opt, network_shared_ptr);

// obx_sync_opt_mesh() consumes mesh_opt, including when an error occurs.
obx_sync_opt_mesh(sync_opt, mesh_opt);

OBX_sync* sync_client = obx_sync_create(sync_opt);
obx_sync_credentials(sync_client, OBXSyncCredentialsType_NONE, NULL, 0);
obx_sync_start(sync_client);
```

Note: The C and C++ APIs expose the underlying mesh options, but a platform transport must be registered before creating the Sync client.
Do not use `obx_mesh_opt_network_internal()` directly unless your platform SDK or integration provides the required transport handle.

{% endtab %}
{% endtabs %}

## Setup

Keep the regular ObjectBox Sync plugin and setup from [Sync Client](sync-client.md#objectbox-sync-enabled-library).

For Android, Mesh Sync requires the Sync-enabled ObjectBox Android runtime and Google Nearby Connections.

{% tabs %}
{% tab title="Android Kotlin DSL" %}
You still use the latest official ObjectBox version, and add the preview runtime dependency explicitly.
The direct `objectbox-sync-android-db` dependency is an override for the transitive native runtime while Mesh Sync is in preview.

```kotlin
dependencies {
    implementation("io.objectbox:objectbox-sync-android-db:6.0.0-preview1")
    implementation("com.google.android.gms:play-services-nearby:19.3.0")
}
```
{% endtab %}

{% tab title="Android Groovy" %}
You still use the latest official ObjectBox version, and add the preview runtime dependency explicitly.
The direct `objectbox-sync-android-db` dependency is an override for the transitive native runtime while Mesh Sync is in preview.

```groovy
dependencies {
    implementation "io.objectbox:objectbox-sync-android-db:6.0.0-preview1"
    implementation "com.google.android.gms:play-services-nearby:19.3.0"
}
```
{% endtab %}

{% tab title="Dart/Flutter" %}
Use the preview ObjectBox Dart package that contains Mesh Sync support.

```yaml
dependencies:
  objectbox: ^6.0.0-preview.1
```
{% endtab %}
{% endtabs %}

## Permissions

Mesh Sync may use Bluetooth, Wi-Fi and location-related Android permissions for discovery and connections.

{% tabs %}
{% tab title="Android XML" %}

Declare the required permissions in `AndroidManifest.xml`.

```xml
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <!-- Permissions required by Object Mesh Sync -->
    <uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />
    <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
    <uses-permission android:name="android.permission.ACCESS_WIFI_STATE" />
    <uses-permission android:name="android.permission.CHANGE_WIFI_STATE" />
    <uses-permission android:name="android.permission.BLUETOOTH" />
    <uses-permission android:name="android.permission.BLUETOOTH_ADMIN" />
    <uses-permission android:name="android.permission.BLUETOOTH_ADVERTISE" />
    <uses-permission android:name="android.permission.BLUETOOTH_CONNECT" />
    <uses-permission
        android:name="android.permission.BLUETOOTH_SCAN"
        android:usesPermissionFlags="neverForLocation" />
    <uses-permission
        android:name="android.permission.NEARBY_WIFI_DEVICES"
        android:usesPermissionFlags="neverForLocation" />
</manifest>
```
{% endtab %}
{% endtabs %}

### Runtime Permissions

Request all runtime permissions before starting Mesh Sync.
On modern Android versions this typically includes nearby devices, Bluetooth scan/connect/advertise and location permissions.
Location services may also need to be enabled on the device for discovery to work reliably.

{% tabs %}
{% tab title="Android (Kotlin/Java)" %}
Use the standard procedure to [request runtime permissions](https://developer.android.com/training/permissions/requesting) within the app.
{% endtab %}
{% tab title="Dart/Flutter" %}
In Dart, `createMeshConfig()` requests the required runtime permissions from the user via the system UI (you still need to define them in `AndroidManifest.xml`).
Alternatively, you can also implement your own permission request logic, and pass `false` to the `requestPermissions` parameter to prevent requesting runtime permissions.
Note that `createMeshConfig()` will only request runtime permissions if they are not already granted.
{% endtab %}
{% endtabs %}


## Configuration

The mesh identifier controls which peers can discover each other.
Peers with different identifiers ignore each other.
Use different identifiers to isolate sync groups.

| Option                            | Default  | Description                                                                       |
|-----------------------------------|----------|-----------------------------------------------------------------------------------|
| `meshId`                          | Required | Mesh network identifier.                                                          |
| `maxConnectionCount`              | `3`      | Maximum number of simultaneous peer connections.                                  |
| `backoffMillis`                   | `10000`  | Delay before retrying a failed connection.                                        |
| `evictionBackoffMillis`           | `30000`  | Delay between peer evictions when a full peer makes room for a newcomer.          |
| `randomSeed`                      | `0`      | Random seed; `0` uses the current time.                                           |
| `requestTimeoutMillis`            | `5000`   | Timeout for requesting a missing sync log from a peer before trying another peer. |
| `advertisingDelayMillis`          | `2000`   | Delay before advertising starts after Mesh Sync starts.                           |
| `connectDelayMillis`              | `1000`   | Minimum delay between outgoing connection attempts.                               |
| `initialDiscoveryDurationSeconds` | `30`     | Duration of the first discovery phase; `0` means it does not stop by time.        |
| `discoveryDurationSeconds`        | `15`     | Duration of later discovery phases; `0` means they do not stop by time.           |
| `discoveryPauseSeconds`           | `45`     | Pause between discovery phases.                                                   |
| `discoveryPauseJitterSeconds`     | `15`     | Random positive or negative jitter applied to the discovery pause.                |
| `txLogBatchSizeKb`                | `100`    | Soft payload size cap for batching sync logs into a single transfer.              |
| `txLogBatchMaxCount`              | `1000`   | Maximum number of sync logs to batch into one transfer.                           |

The default `maxConnectionCount` of `3` is a good starting point for most meshes.
A value of `4` may improve fault tolerance, but it increases radio activity.
Values above `4` are usually not recommended.
A value of `1` creates pairs and is not a real mesh topology.

Set configuration options using the API for your language.
The following examples show how to configure a mesh and set `maxConnectionCount` to `4` where the current API exposes it.

{% tabs %}
{% tab title="Java" %}
The Java preview API currently exposes Android Nearby options such as `serviceId`, but not `maxConnectionCount`.

```java
MeshConfig.builder(context)
        .serviceId("io.objectbox.example.sync.tasks")
        .build()
        .applyTo(syncClient);
```
{% endtab %}

{% tab title="Kotlin" %}
The Kotlin preview API currently exposes Android Nearby options such as `serviceId`, but not `maxConnectionCount`.

```kotlin
MeshConfig.builder(context)
    .serviceId("io.objectbox.example.sync.tasks")
    .build()
    .applyTo(syncClient)
```
{% endtab %}

{% tab title="Dart/Flutter" %}
```dart
final mesh = createMeshConfig(
  'io.objectbox.example.sync.tasks',
  maxConnectionCount: 4,
);
```
{% endtab %}

{% tab title="C++" %}
```cpp
obx::MeshOptions meshOptions("io.objectbox.example.sync.tasks");
meshOptions.maxConnectionCount(4);
```
{% endtab %}

{% tab title="C" %}
```c
OBX_mesh_options* mesh_opt = obx_mesh_opt("io.objectbox.example.sync.tasks");
obx_mesh_opt_max_connection_count(mesh_opt, 4);
```
{% endtab %}
{% endtabs %}

If several devices start at the same time, give discovery and connection setup a little time.
Mesh Sync intentionally staggers advertising and outgoing connection attempts to reduce radio contention.

## Diagnostics

The running mesh can report its state and connected peer count.
Important states are `Created`, `Discovering`, `FullyConnected`, `Stopped` and `Dead`.
Useful counters include discovered peers, connected peers, failed connection attempts, sent and received messages, received sync logs and applied sync logs.

{% tabs %}
{% tab title="Dart/Flutter" %}
```dart
final mesh = syncClient.mesh;
if (mesh != null) {
  print(mesh.stateString());
  print(mesh.connectedPeerCount());
  print(mesh.stats(MeshStats.txLogsApplied));
}
```
{% endtab %}

{% tab title="C++" %}
```cpp
obx::Mesh mesh = syncClient->mesh();
if (mesh.isAttached()) {
    std::cout << mesh.stateString() << std::endl;
    std::cout << mesh.connectedPeerCount() << std::endl;
    std::cout << mesh.statsU64(OBXMeshStats_txLogsApplied) << std::endl;
}
```
{% endtab %}

{% tab title="C" %}
```c
OBX_mesh* mesh = obx_sync_mesh(sync_client);
if (mesh) {
    printf("%s\n", obx_mesh_state_string(mesh));
    printf("%zu\n", obx_mesh_connected_peer_count(mesh));

    uint64_t applied = 0;
    obx_mesh_stats_u64(mesh, OBXMeshStats_txLogsApplied, &applied);
    printf("Applied sync logs: %llu\n", (unsigned long long) applied);
}
```
{% endtab %}
{% endtabs %}

## Current Limitations

Mesh Sync is currently in public preview.
Until the final release, we'll finalize the API and plan to address the following limitations.  

* Only works on Android (Mesh Sync has a network abstraction layer that is currently only implemented for Android) 
* Transactions are limited to ~ 1000 KB (compressed); larger ones (e.g., containing larger phtotos/videos) are ignored.
* Mesh Sync data is kept in memory only; it's not persisted to disk.
* No expiration of data; there will be a setting to limit the time and/or size of the data that is synced to the mesh.
* No optimized interaction with the Sync Server yet; e.g.:
  * Only the peer of the original edit syncs that data to the server.
    In the future, any peer having the data can sync it to the server.
  * Changes from the server are not synced to the mesh.
* Java/Kotlin API is very limited
* Advertising is only initiated once on startup; if that fails, e.g. due to missing permissions, Mesh Sync will not retry.
* TBD: Peer authentication; currently there's no auth between peers other than the mesh ID.
* TBD: permission handling details
* TBD: the mesh ID (required at construction time) is the only mechanism to form sync groups.
* TBD: clarify if Nearby dependency shall already be included by the lib or needs to be added by the user.

## Related Pages

- [Sync Client](sync-client.md)
- [Troubleshooting Sync](troubleshooting-sync.md)
