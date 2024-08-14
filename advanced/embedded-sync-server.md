---
description: How to set up an ObjectBox Sync server that is embedded in your application.
---

# Embedded Sync Server

{% hint style="warning" %}
This page refers to the **embedded** sync server, **not the standalone** sync server.\
Usually, you want to use the [standalone server](../objectbox-sync-server.md).
{% endhint %}

{% hint style="info" %}
Free Data Sync trials are currently available for [Standalone Servers](https://sync.objectbox.io/objectbox-sync-server) only.&#x20;

However, for commercial use cases, we do offer embedded servers in all of the ObjectBox language bindings ([Java](https://docs.objectbox.io/), [Kotlin](https://docs.objectbox.io/), [C/C++](https://cpp.objectbox.io/), [Flutter/Dart](https://docs.objectbox.io/), [Go](https://golang.objectbox.io/), [Swift](https://swift.objectbox.io/)).
{% endhint %}

## Use a Sync server library

### Java (Android/Linux)

By now, you were likely in touch with the ObjectBox team and were given Sync Server library artifacts. To use them in a Gradle project they have to be included as a local binary dependency. And the ObjectBox plugin has to be prevented from adding conflicting dependencies.

Copy the AAR and JAR files to the `<module_name>/libs` directory (the path is relative to the `build.gradle` file), then modify `build.gradle`:

{% tabs %}
{% tab title="Groovy" %}
```groovy
// Prevent the ObjectBox plugin from adding dependencies without Sync server.
configurations {
    all {
        exclude group: "io.objectbox", module: "objectbox-android"
        exclude group: "io.objectbox", module: "objectbox-linux"
    }
}

dependencies {
    // Add any .aar and .jar file from <module_name>/libs as a dependency.
    implementation fileTree(dir: "libs", include: ["*.aar", "*.jar"])
}

apply plugin: "io.objectbox.sync"
```
{% endtab %}

{% tab title="Kotlin" %}
```kotlin
// Prevent the ObjectBox plugin from adding dependencies without Sync server.
configurations {
    all {
        exclude(group = "io.objectbox", module = "objectbox-android")
        exclude(group = "io.objectbox", module = "objectbox-linux")
    }
}

dependencies {
    // Add any .aar and .jar file from <module-dir>/libs as a dependency.
    implementation(fileTree(mapOf("dir" to "libs", "include" to listOf("*.aar", "*.jar"))))
}

apply(plugin = "io.objectbox.sync")
```
{% endtab %}
{% endtabs %}

## Start a Sync server

Use `Sync.server(boxStore, url, authenticatorCredentials)` to start a Sync server using a `boxStore` . The server binds to the address and port given in `url`.

When using `wss` as the protocol of the `url` a TLS encrypted connection is established. Use `certificatePath(path)` to supply a `path` to a certificate in PEM format. Use `ws` instead to turn off transport encryption (insecure, only use for testing!).

`authenticatorCredentials` are required to authenticate clients. It is possible to add more than one set of allowed credentials.

{% tabs %}
{% tab title="Java" %}
```java
SyncServer syncServer = Sync.server(
        boxStore,
        "wss://0.0.0.0:9999" /* Use ws for unencrypted traffic. */,
        SyncCredentials.sharedSecret("<secret>")
)                                // Builder...
.certificatePath(certPath)        // Server PEM certificate
.authenticatorCredentials(cred2) // Additional credentials
.buildAndStart();
```
{% endtab %}

{% tab title="C++" %}
```cpp
// Developer options; use wss and real credentials in production...
obx::SyncServer server(std::move(storeOptions), "ws://0.0.0.0:9999");
server.setCredentials(obx::SyncCredentials::none());
server.start();
obx::Store& store = server.store();
```
{% endtab %}
{% endtabs %}

During `buildAndStart()` the server will start and become ready to accept connections from clients. Read below for more configuration options you can use before starting the connection.&#x20;

## Client authentication

These are the currently supported options to authenticate clients:

### Shared secret

```java
SyncCredentials credentials = SyncCredentials.sharedSecret("<secret>");
```

This can be any pre-shared secret string or a byte sequence.

### Google Sign-In

Not available, yet.

### No authentication (insecure)

{% hint style="danger" %}
Never use this option to serve an app shipped to customers. It is inherently insecure and allows anyone to access the sync server.
{% endhint %}

```java
SyncCredentials credentials = SyncCredentials.none();
```

For development and testing it is often easier to just have no authentication at all to quickly get things up and running.

## Manually start

Using the example above, the server automatically binds to the given address and port and starts listening for clients. It is also possible to just build the server and then start it once your code is ready to.

```java
// Just build the server.
SyncServer syncServer = Sync.server(...).build();

// Start now.
syncServer.start();
```

Note that a started server can not be started again. Stop and close an existing server and build a new one instead.

## Advanced

### Listening to incoming data changes

For advanced use cases, it might be useful to know exactly which objects have changed during an incoming sync update. This is typically not necessary, as observing a box or a query may be easier.

To listen to these incoming data changes:

```java
SyncChangeListener changeListener = syncChanges -> {
    for (SyncChange syncChange : syncChanges) {
        // This is equal to Example_.__ENTITY_ID.
        long entityId = syncChange.getEntityTypeId();
        // The @Id values of changed and removed entities.
        long[] changed = syncChange.getChangedIds();
        long[] removed = syncChange.getRemovedIds();
    }
};
// Set the listener when building the server.
syncBuilder.changeListener(changeListener);
// Or set the listener later.
syncServer.setSyncChangeListener(changeListener);

// Calling again replaces an existing listener.
syncServer.setSyncChangeListener(changeListener);
// Remove an existing listener.
syncServer.setSyncChangeListener(null);
```

On each sync update received on the server, the listener is called with an array of "Sync Change" objects, one for each affected entity type. It includes a list of affected object IDs - the ones that were put or removed in the incoming update.

### Adding peer servers

{% hint style="info" %}
Before using peer servers, please reach out to the ObjectBox team.
{% endhint %}

It is possible to have multiple sync servers for redundancy and load balancing where one or more secondary servers connect as special clients to a primary server.

To add the primary server when building a secondary server:

```java
syncBuilder.peer(primaryServerUrl, SyncCredentials.sharedSecret("<secret>"));
```
