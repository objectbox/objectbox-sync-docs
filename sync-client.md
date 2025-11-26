---
description: >-
  How to create an ObjectBox Sync client and connect to an ObjectBox Sync
  server.
---

# Sync Client

{% hint style="info" %}
Prefer to look at example code? Check out [our Sync examples repository](https://github.com/objectbox/objectbox-sync-examples).
{% endhint %}

## ObjectBox Sync enabled library

The standard ObjectBox (database) library does not include ObjectBox Sync (but may provide Sync **API interfaces**, to allow compiling).

{% hint style="info" %}
If you have not used ObjectBox before, please also be aware of documentation for the standard (non-sync) edition of ObjectBox (the ObjectBox DB) for your programming language ([Java/Kotlin](https://docs.objectbox.io/), [Swift](https://swift.objectbox.io/), [C and C++](https://cpp.objectbox.io/), [Go](https://golang.objectbox.io/)). You are currently looking at the documentation specific to ObjectBox Sync, which does not cover ObjectBox basics.
{% endhint %}

To get the ObjectBox Sync client library follow the instructions for your programming language:

{% tabs %}
{% tab title="Java/Kotlin (JVM, Android)" %}
Follow the [Getting Started](https://docs.objectbox.io/getting-started) page instructions. Then change the applied Gradle plugin to the sync variant:

```groovy
// This automatically adds the native dependency:
apply plugin: "io.objectbox.sync"  // instead of "io.objectbox"
```

This will automatically add the Sync variant for your platform.

If needed, e.g. to publish a JVM app that supports multiple platforms or to add Linux ARM support, add the libraries manually:

<pre class="language-groovy"><code class="lang-groovy"><strong>// Android
</strong><strong>implementation("io.objectbox:objectbox-sync-android:$objectboxVersion")
</strong>
<strong>// JVM
</strong>implementation("io.objectbox:objectbox-sync-linux:$objectboxVersion")
implementation("io.objectbox:objectbox-sync-macos:$objectboxVersion")
implementation("io.objectbox:objectbox-sync-windows:$objectboxVersion")
// JVM Linux on ARM (not added automatically)
implementation("io.objectbox:objectbox-sync-linux-arm64:$objectboxVersion")       
implementation("io.objectbox:objectbox-sync-linux-armv7:$objectboxVersion")
</code></pre>
{% endtab %}

{% tab title="Swift" %}
{% hint style="info" %}
This gives you specific information about how to get the Sync-enabled version of ObjectBox. Please also check our [general installation and update ](https://swift.objectbox.io/install)docs for in-depth information.
{% endhint %}

We may distribute ObjectBox Sync for Swift in our **Cocoapods** staging repository (details will be provided by the ObjectBox team). In that case, these are some typical lines to put in your Podfile (please check the version, there might be a newer one available):

```
target 'MyCoolSyncProject' do
    use_frameworks!
    pod 'ObjectBox', '4.4.0-sync'
end

```
{% endtab %}

{% tab title="Dart/Flutter" %}
See the [Getting Started](https://docs.objectbox.io/getting-started) instructions for Flutter or Dart and note the different instructions for Sync (different Flutter library, increasing Android minSdkVersion, install script parameter).
{% endtab %}

{% tab title="C/C++" %}
```bash
bash <(curl -s https://raw.githubusercontent.com/objectbox/objectbox-c/main/download.sh) --sync
```

Or use [CMake's FetchContent](https://cmake.org/cmake/help/latest/module/FetchContent.html) to get ObjectBox headers and library ready to use in your project:

{% code title="CMakeLists.txt" %}
```cmake
include(FetchContent)
FetchContent_Declare(
    objectbox
    GIT_REPOSITORY https://github.com/objectbox/objectbox-c.git
    GIT_TAG        v4.3.1 # Or a newer sync-enabled version
)

FetchContent_MakeAvailable(objectbox)

add_executable(myapp main.cpp)
target_link_libraries(myapp objectbox-sync)
```
{% endcode %}
{% endtab %}

{% tab title="Go" %}
```bash
bash <(curl -s https://raw.githubusercontent.com/objectbox/objectbox-go/main/install.sh) --sync
```
{% endtab %}

{% tab title="Others" %}
Please reach out to the ObjectBox team.
{% endtab %}
{% endtabs %}

Now it is time to **verify** the setup using a flag telling if Sync is available; for example, simply log the result:

{% tabs %}
{% tab title="Java" %}
```java
import io.objectbox.sync.Sync;

String syncAvailable = Sync.isAvailable() ? "available" : "unavailable";
System.out.println("ObjectBox Sync is " + syncAvailable);
```
{% endtab %}

{% tab title="Kotlin" %}
```kotlin
import io.objectbox.sync.Sync

val syncAvailable = if (Sync.isAvailable()) "available" else "unavailable"
Log.d(App.TAG, "ObjectBox Sync is $syncAvailable")
```
{% endtab %}

{% tab title="Swift" %}
```swift
let isSyncAvailable = Sync.isAvailable()
print("ObjectBox Sync is \(isSyncAvailable ? "available" : "unavailable")")
```
{% endtab %}

{% tab title="Dart/Flutter" %}
```dart
final isSyncAvailable = Sync.isAvailable();
print('ObjectBox Sync is ${isSyncAvailable ? "available" : "unavailable"}');
```
{% endtab %}

{% tab title="C++" %}
```cpp
#include <iostream>
#include "objectbox-sync.hpp"

// ...
bool isSyncAvailable = obx::Sync::isAvailable();
std::cout << "ObjectBox Sync is " << (isSyncAvailable ? "available" : "unavailable") << std::endl;
```
{% endtab %}

{% tab title="C" %}
```c
#include <stdio.h>
#include "objectbox-sync.h"

// ...
bool hasSync = obx_has_feature(OBXFeature_Sync);
printf("ObjectBox Sync is %s\n", hasSync ? "available" : "unavailable");
```
{% endtab %}

{% tab title="Go" %}
```go
import "fmt"
import "github.com/objectbox/objectbox-go/objectbox"

// ...
var syncAvailable = "unavailable"
if objectbox.SyncIsAvailable() {
    syncAvailable = "available"
}
fmt.Printf("ObjectBox Sync is %s\n", syncAvailable)
```
{% endtab %}

{% tab title="Others" %}
```
// Depending on the platform something like:
// bool isAvailable = Sync.isAvailable();
// print("ObjectBox Sync is " + (isAvailable ? "available" : "unavailable"));
```
{% endtab %}
{% endtabs %}

## Enable your Objects for ObjectBox Sync

ObjectBox Sync allows you to define which objects are synced and which are not. This is done at an object type level (a "class" in many programming languages). By default, an object (type) is local only: objects are kept in the database on the local device and do not get synced to other devices.

To enable sync for an object type, you add a **"sync" annotation** to the type definition. This is typically the entity source file, or, if you are using ObjectBox Generator, the FlatBuffers schema file:

{% tabs %}
{% tab title="Java" %}
```java
@Sync
@Entity
public class User {
    // ...
}
```
{% endtab %}

{% tab title="Kotlin" %}
```kotlin
@Sync
@Entity
data class User(
        // ...
)
```
{% endtab %}

{% tab title="Swift" %}
```swift
// objectbox: sync
class User: Entity {
    // ...
}
```
{% endtab %}

{% tab title="Dart/Flutter" %}
```dart
@Entity
@Sync
class User {
    // ...
}
```
{% endtab %}

{% tab title="C/C++ (using Generator)" %}
```cpp
/// objectbox: sync
table User {
    // ...
}
```
{% endtab %}

{% tab title="Go" %}
```go
// `objectbox:"sync"`
type User struct {
    // ...
}
```
{% endtab %}
{% endtabs %}

Once the sync annotation is set on the intended types, you need to rebuild (e.g. Java/Kotlin) or trigger the ObjectBox generator (e.g. C and C++). This activates a "sync flag" in the metamodel (e.g. the model JSON file is updated).

{% hint style="info" %}
At this point, it is not allowed to change a non-synced object type to a synced one. This would raise questions on how to handle pre-existing data, e.g. should it be deleted, synced (how exactly? using how many transactions? ...), or kept locally until objects are put again? We welcome your input on your use case if this is a scenario you encounter.

Additionally, there may only be relations between sync-enabled or non-sync entities, not across this boundary.
{% endhint %}

If you already have a non-synced type that you now want to sync (see also the info box above), these are the typical options you have:

1. If you are still in development, add the sync annotation and wipe your database(s) to start fresh with that new data model.
2. "Replace" the entity type using a new UID (check schema changes docs for the ObjectBox binding you are using). You can keep the type name; to ObjectBox it will be a different type as the UID is different. This will delete all existing data in that type.
3. Have a second, synced, object type and migrate your data in your code following your rules.

## Start the Sync Client

Create a Sync client for your Store and start it. It connects to a given sync server URL using some form of credentials to authenticate with the server. A minimal setup can look like this:

{% tabs %}
{% tab title="Java" %}
```java
SyncClient syncClient = Sync.client(
        boxStore, 
        "ws://127.0.0.1" /* Use wss for encrypted traffic. */, 
        SyncCredentials.none()
).buildAndStart(); // Connect and start syncing.
```
{% endtab %}

{% tab title="Kotlin" %}
```kotlin
val syncClient = Sync.client(
        boxStore,
        "ws://127.0.0.1" /* Use wss for encrypted traffic. */,
        SyncCredentials.none()
).buildAndStart() // Connect and start syncing.
```
{% endtab %}

{% tab title="Swift" %}
```swift
let client = try Sync.makeClient(store: store, urlString: "ws://127.0.0.1:9999",
                                 credentials: SyncCredentials.makeNone())
try client.start()
```
{% endtab %}

{% tab title="Dart/Flutter" %}
```dart
final syncClient = Sync.client(
        store,
        'ws://127.0.0.1:9999', // wss for SSL, ws for unencrypted traffic
        SyncCredentials.none());
syncClient.start(); // connect and start syncing
```
{% endtab %}

{% tab title="C++" %}
```cpp
std::shared_ptr<obx::SyncClient> syncClient = obx::Sync::client(
    store, 
    "ws://127.0.0.1:9999",  // wss for SSL, ws for unencrypted traffic
    obx::SyncCredentials::none()
);
syncClient->start();  // connect and start syncing
```
{% endtab %}

{% tab title="C" %}
```c
OBX_sync* sync_client = obx_sync(store, "ws://127.0.0.1:9999");  // wss for SSL
obx_sync_credentials(sync_client, OBXSyncCredentialsType_NONE, NULL, 0);
obx_sync_start(sync_client);  // connect and start syncing
```
{% endtab %}

{% tab title="Go" %}
```go
syncClient, err := objectbox.NewSyncClient(
		store,
		"ws://127.0.0.1", // wss for SSL, ws for unencrypted traffic
		objectbox.SyncCredentialsNone())

if err == nil { // Corrected: check if err is nil before starting
		err = syncClient.Start() // Connect and start syncing.
}
if err != nil {
    // Handle error, e.g., log it
    fmt.Printf("Error starting sync client: %v\n", err)
}
```
{% endtab %}
{% endtabs %}

{% hint style="info" %}
The example uses ws://127.0.0.1 for the server endpoint. This is the IP address of localhost and assumes that you run the server and client(s) on the same machine. If it is separate machines, you need to exchange 127.0.0.1 with a reachable IP address of the server, or some valid DNS name.

Using Android emulator? You can use 10.0.2.2 to reach the host (the machine running the emulator). [Details](https://developer.android.com/studio/run/emulator-networking)
{% endhint %}

Sync client is started by calling `start()` or `buildAndStart()`. It will then try to connect to the server, authenticate and start syncing. Read below for more configuration options you can use before starting the connection.

Once the client is logged in, the server will push any changes it has missed. The server will also push any future changes while the client remains connected. This [sync updates behavior](sync-client.md#controlling-sync-updates-behavior) can be configured.

All of this happens asynchronously. To observe these events (log in, sync completed, …) read below on how to [configure an event listener](sync-client.md#listening-to-events).

The client will now also push changes to the server for each Store transaction.

Should the client get disconnected, e.g. due to internet connection issues, it will automatically try to reconnect using an exponential back-off. Once the connection succeeds, data synchronization resumes.

{% hint style="warning" %}
Always close the client **before** closing the store. Closing the store with a still running sync client results in undefined behavior (e.g. crashes). Keep in mind that it typically is fine to **leave the sync client and store open**; once the application exits, they will be automatically closed properly.  
{% endhint %}

### Sync filter client variables

Sync clients may provide variables for sync filters, see [sync filters](sync-server/sync-filters.md) and specifically the [the section on client variables](sync-server/sync-filters.md#client-variables) for general information.

The client APIs to add sync filter variables take name/value pairs (both strings) and look like this:

{% tabs %}
{% tab title="Java" %}
```java
SyncClient syncClient = Sync.client(...)
                            .filterVariable("name", "value")
                            .buildAndStart(); 
```
{% endtab %}

{% tab title="Kotlin" %}
```kotlin
val syncClient = Sync.client(...)
                     .filterVariable("name", "value")
                     .buildAndStart()
```
{% endtab %}

{% tab title="Swift" %}
```swift
let client = try Sync.makeClient(store: store, urlString: "ws://127.0.0.1:9999",
                                 credentials: SyncCredentials.makeNone(),
                                 filterVariables: ["name": "value"])
try client.start()
```
{% endtab %}

{% tab title="Dart/Flutter" %}
```dart
final syncClient = Sync.client(store, 'ws://127.0.0.1:9999', SyncCredentials.none()
                               filterVariables: {"name": "value"});
syncClient.start();
```
{% endtab %}

{% tab title="C++" %}
```cpp
// Init as before: std::shared_ptr<obx::SyncClient> syncClient = obx::Sync::client(...);
syncClient->putFilterVariable("name", "value");
syncClient->start();  // connect and start syncing
```
{% endtab %}

{% tab title="C" %}
```c
// Init as before: OBX_sync* sync_client = obx_sync(...); // plus credentials
obx_sync_filter_variables_put(sync_client, "name", "value");
obx_sync_start(sync_client);  // connect and start syncing
```
{% endtab %}

{% tab title="Go" %}
```go
// coming soon
```
{% endtab %}
{% endtabs %}

### Drop-off, send-only clients

For some use cases, a client should only report data and thus only send updates without ever receiving any data. We call those "drop-off clients". Technically, from an API perspective, these clients do not request updates from the server. Because requesting updates is the default, the sync client API has to be configured to do "manual" updates to actually disable updates from the server. This configuration has to happen before the client starts.

```cpp
// C++; create syncClient as above, but do not start() just yet
syncClient->setRequestUpdatesMode(OBXRequestUpdatesMode_MANUAL);
syncClient->start();
```

### Secure Connection

When using `wss` as the protocol in the server URL a TLS encrypted connection is established. Use `ws` instead to turn off transport encryption (insecure, not recommended; e.g. only use for testing).

## Authentication options

There are currently multiple supported options for authenticating clients with a Sync server.

### JWT authentication

Clients can be authenticated using tokens in JWT (JSON web token) format. The general process is outlined in the [server-side JWT documentation](sync-server/jwt-authentication.md). Your client application typically will use a JWT authentication provider SDK to get a token in JWT format. This token is then set as a credential using the ObjectBox Sync client API:

{% tabs %}
{% tab title="Java" %}
```java
String idToken = "<your_jwt_id_token>"; // Get from JWT authentication provider
SyncCredentials credential = SyncCredentials.jwtIdToken(idToken);
// Options for other types of JWT are available:
// jwtAccessToken(token), jwtRefreshToken(token), jwtCustomToken(token)
```
{% endtab %}

{% tab title="Kotlin" %}
```kotlin
val idToken: String = "<your_jwt_id_token>" // Get from JWT authentication provider
val credential = SyncCredentials.jwtIdToken(idToken)
// Options for other types of JWT are available:
// jwtAccessToken(token), jwtRefreshToken(token), jwtCustomToken(token)
```
{% endtab %}

{% tab title="Swift" %}
```swift
let idToken: String = "<your_jwt_id_token>" // Get from JWT authentication provider
let credential = SyncCredentials.makeJwtIdToken(idToken)
// Options for other types of JWT are available:
// makeJwtAccessToken(...), makeJwtRefreshToken(...), makeJwtCustomToken(...)
```
{% endtab %}

{% tab title="Dart/Flutter" %}
```dart
String idToken = "<your_jwt_id_token>"; // Get from JWT authentication provider
SyncCredentials credential = SyncCredentials.jwtIdToken(idToken);
// Options for other types of JWT are available:
// jwtAccessToken(token), jwtRefreshToken(token), jwtCustomToken(token)
```
{% endtab %}

{% tab title="C++" %}
```cpp
std::string idToken = "<your_jwt_id_token>"; // Get from JWT authentication provider
obx::SyncCredentials credential = obx::SyncCredentials::jwtIdToken(idToken);
// Options for other types of JWT are available:
// obx::SyncCredentials::jwtAccessToken(token), obx::SyncCredentials::jwtRefreshToken(token), obx::SyncCredentials::jwtCustomToken(token)
```
{% endtab %}

{% tab title="C" %}
```c
const char* idToken = "<your_jwt_id_token>"; // Get from JWT authentication provider
// Assuming obx_sync_credentials_jwt_id_token exists or similar mechanism
obx_sync_credentials_jwt(sync_client, OBXSyncJwtTokenType_ID_TOKEN, idToken, strlen(idToken));
// Other token types would use different OBXSyncJwtTokenType enum values.
// The exact C API for JWT might vary; consult specific C API docs or headers.
```
{% endtab %}

{% tab title="Go" %}
```go
idToken := "<your_jwt_id_token>" // Get from JWT authentication provider
credential := objectbox.SyncCredentialsJwtId([]byte(idToken))
```
{% endtab %}
{% endtabs %}

### Shared secret

This can be any pre-shared secret string or a byte sequence.

{% tabs %}
{% tab title="Java" %}
```java
SyncCredentials credential = SyncCredentials.sharedSecret("<your_secret>");
```
{% endtab %}

{% tab title="Kotlin" %}
```kotlin
val credential = SyncCredentials.sharedSecret("<your_secret>")
```
{% endtab %}

{% tab title="Swift" %}
```swift
let credential = SyncCredentials.makeSharedSecret("<your_secret>")
```
{% endtab %}

{% tab title="Dart/Flutter" %}
```dart
// use a string
final credential = SyncCredentials.sharedSecretString("<your_secret>");

// or a byte vector
final secret = Uint8List.fromList([0, 46, 79, 193, 185, 65, 73, 239, 15, 5]);
final credentialBytes = SyncCredentials.sharedSecretUint8List(secret);
```
{% endtab %}

{% tab title="C++" %}
```cpp
// use a string
obx::SyncCredentials cred = obx::SyncCredentials::sharedSecret("your_secret_string");

// or a byte vector
std::vector<uint8_t> secret = {0, 46, 79, 193, 185, 65, 73, 239, 15, 5, 189, 186};
obx::SyncCredentials cred = obx::SyncCredentials::sharedSecret(std::move(secret));
```
{% endtab %}

{% tab title="C" %}
```c
// use a string
const char* secretStr = "your_secret_string";
obx_sync_credentials(sync_client, 
    OBXSyncCredentialsType_SHARED_SECRET, 
    secretStr, 
    strlen(secretStr)
);

// or a byte vector
uint8_t secretBytes[] = {0, 46, 79, 193, 185, 65, 73, 239, 15, 5, 189, 186};
obx_sync_credentials(sync_client, 
    OBXSyncCredentialsType_SHARED_SECRET, 
    secretBytes, 
    sizeof(secretBytes)
);
```
{% endtab %}

{% tab title="Go" %}
```go
// use a string
credStr := objectbox.SyncCredentialsSharedSecret([]byte("your_secret_string"))

// or a byte vector
secretBytes := []byte{0, 46, 79, 193, 185, 65, 73, 239, 15, 5, 189, 186}
credBytes := objectbox.SyncCredentialsSharedSecret(secretBytes)
```
{% endtab %}
{% endtabs %}

### Google Sign-In

The ObjectBox Sync server supports authenticating users using their Google account. This assumes [Google Sign-In](https://developers.google.com/identity/sign-in/android/start-integrating) is integrated into your app and it has [obtained the user's ID token](https://developers.google.com/identity/sign-in/android/backend-auth).

{% tabs %}
{% tab title="Java" %}
```java
SyncCredentials credential = SyncCredentials.google(account.getIdToken());
```
{% endtab %}

{% tab title="Kotlin" %}
```kotlin
val credential = SyncCredentials.google(account.getIdToken())
```
{% endtab %}

{% tab title="Swift" %}
_Coming soon!_
{% endtab %}

{% tab title="Dart/Flutter" %}
```dart
// use a string
SyncCredentials credential = SyncCredentials.googleAuthString("<secret>");

// or a byte vector
Uint8List secret = Uint8List.fromList([0, 46, 79, 193, 185, 65, 73, 239, 15, 5]);
SyncCredentials credential = SyncCredentials.googleAuthUint8List(secret);
```
{% endtab %}

{% tab title="C++" %}
_Coming soon!_
{% endtab %}

{% tab title="C" %}
```c
obx_sync_credentials(sync_client, 
    OBXSyncCredentialsType_GOOGLE_AUTH, 
    googleIdToken, 
    strlen(googleIdToken)
 );
```
{% endtab %}

{% tab title="Go" %}
```go
// use a string
var cred = objectbox.SyncCredentialsGoogleAuth([]byte("string"))

// or a byte vector
var secret = []byte{0, 46, 79, 193, 185, 65, 73, 239, 15, 5, 189, 186}
var cred = objectbox.SyncCredentialsGoogleAuth(secret)
```
{% endtab %}
{% endtabs %}

### No authentication (unsecure)

{% hint style="danger" %}
Never use this option in an app shipped to customers. It is inherently insecure and allows anyone to connect to the sync server.
{% endhint %}

For development and testing, it is often easier to just have no authentication at all to quickly get things up and running.

{% tabs %}
{% tab title="Java" %}
```java
SyncCredentials credential = SyncCredentials.none();
```
{% endtab %}

{% tab title="Kotlin" %}
```kotlin
val credential = SyncCredentials.none()
```
{% endtab %}

{% tab title="Swift" %}
_Coming soon!_
{% endtab %}

{% tab title="Dart/Flutter" %}
```java
SyncCredentials credential = SyncCredentials.none();
```
{% endtab %}

{% tab title="C++" %}
```cpp
obx::SyncCredentials credential = obx::SyncCredentials::none();
```
{% endtab %}

{% tab title="C" %}
```c
obx_sync_credentials(sync_client, OBXSyncCredentialsType_NONE, NULL, 0)
```
{% endtab %}

{% tab title="Go" %}
```go
var cred = objectbox.SyncCredentialsNone()
```
{% endtab %}
{% endtabs %}

## Manually start

In the Java and Kotlin example above, the sync client automatically connects to the server and starts to sync. It is also possible to just build the client and then start to sync once your code is ready to.

{% tabs %}
{% tab title="Java" %}
```java
// Just build the client.
SyncClient syncClient = Sync.client(...).build();

// Start now.
syncClient.start();
```
{% endtab %}

{% tab title="Kotlin" %}
```kotlin
// Just build the client.
val syncClient = Sync.client(...).build()

// Start now.
syncClient.start()
```
{% endtab %}
{% endtabs %}

Note that a started sync client can not be started again. Stop and close an existing one and build a new one instead.

## Listening to events

The sync client supports listening to various events, e.g. if authentication has failed or if the client was disconnected from the server. This enables other components of an app, like the user interface, to react accordingly.

{% tabs %}
{% tab title="Java" %}
It's possible to set one or more specific listeners that observe some events, or a general listener that observes all events. When building a Sync client use:

* `loginListener(listener)` to observe login events.
* `completedListener(listener)` to observe when synchronization has completed.
* `connectionListener(listener)` to observe connection events.
* `listener(listener)` to observe all of the above events. Use `AbstractSyncListener` and only override methods of interest to simplify your listener implementation.

See the description of each listener class and its methods for details.

Note that listeners can also be set or removed at any later point using `SyncClient.setSyncListener(listener)` and related methods.

```java
SyncLoginListener loginListener = new SyncLoginListener() {
    @Override
    public void onLoggedIn() {
        // Login succesful.
    }

    @Override
    public void onLoginFailed(long syncLoginCode) {
        // Login failed. Returns one of SyncLoginCodes.
    }
};

SyncCompletedListener completedListener = new SyncCompletedListener() {
    @Override
    public void onUpdatesCompleted() {
        // A sync has completed, client is up-to-date.
    }
};

SyncConnectionListener connectListener = new SyncConnectionListener() {
    @Override
    public void onDisconnected() {
        // Client disconnected from the server.
        // Depending on the configuration it will try to re-connect.
    }
};

// Set listeners when building the client.
SyncClient syncClient = Sync.client(...)
  .loginListener(loginListener)
  .completedListener(completedListener)
  .connectionListener(connectListener)
  .build();
  
// Set (or replace) a listener later.
syncClient.setSyncLoginListener(listener);

// Remove an existing listener.
syncClient.setSyncConnectionListener(null);
```
{% endtab %}

{% tab title="Kotlin" %}
It's possible to set one or more specific listeners that observe some events, or a general listener that observes all events. When building a Sync client use:

* `loginListener(listener)` to observe login events.
* `completedListener(listener)` to observe when synchronization has completed.
* `connectionListener(listener)` to observe connection events.
* `listener(listener)` to observe all of the above events. Use `AbstractSyncListener` and only override methods of interest to simplify your listener implementation.

See the description of each listener class and its methods for details.

Note that listeners can also be set or removed at any later point using `SyncClient.setSyncListener(listener)` and related methods.

```kotlin
val loginListener: SyncLoginListener = object : SyncLoginListener {
    override fun onLoggedIn() {
        // Login succesful.
    }

    override fun onLoginFailed(syncLoginCode: Long) {
        // Login failed. Returns one of SyncLoginCodes.
    }
}

val completedListener = SyncCompletedListener {
    // A sync has completed, client is up-to-date.
}

val connectListener = object : SyncConnectionListener {
    override fun onDisconnected() {
        // Client disconnected from the server.
        // Depending on the configuration it will try to re-connect.
    }
}

// Set listeners when building the client.
val syncClient = Sync.client(...)
  .loginListener(loginListener)
  .completedListener(completedListener)
  .connectionListener(connectListener)
  .build()
  
// Set (or replace) a listener later.
syncClient.setSyncLoginListener(listener)

// Remove an existing listener.
syncClient.setSyncConnectionListener(null)
```
{% endtab %}

{% tab title="Swift" %}
It's possible to set one or more specific listeners that observe some events, or a general listener that observes all events. The SyncClient protocol offers the following properties to attach listeners:

* `loginListener` to observe login events.
* `completedListener` to observe when synchronization has completed.
* `connectionListener` to observe connection events.
* `listener` to observe all of the above events.

There is a protocol for each listener type. Note that listeners can also be set or removed at any later point by setting the listener property to `nil`.

By implementing a listener protocol and setting the matching property in SyncClient, you are called back. Let's have a look at the available listener protocols for details:

```swift
/// Listens to login events.
public protocol SyncLoginListener {
    /// Called on a successful login.
    /// 
    /// At this point the connection to the sync destination was established and
    /// entered an operational state, in which data can be sent both ways.
    func loggedIn()

    /// Called on a login failure with a `result` code specifying the issue.
    func loginFailed(result: SyncCode)
}

/// Listens to sync completed events.
public protocol SyncCompletedListener {
    /// Called each time a sync was "completed", in the sense that the client 
    /// caught up with the current server state. The client is "up-to-date".
    func updatesCompleted()
}

/// Listens to sync connection events.
public protocol SyncConnectionListener {
    /// Called when connection is established; happens before an actual login
    func connected()

    /// Called when the client is disconnected from the sync server, e.g. due to a network error.
    /// 
    /// Depending on the configuration, the sync client typically tries to reconnect automatically,
    /// triggering a `SyncLoginListener` again.
    func disconnected()
}

/// Listens to all possible sync events. See each protocol for detailed information.
public protocol SyncListener: SyncLoginListener, SyncCompletedListener, SyncChangeListener, SyncConnectionListener {

}
```
{% endtab %}

{% tab title="Dart/Flutter" %}
It's possible to listen to sync-related events on the client. Use the following `SyncClient` getters to connect to a stream:

* `Stream<SyncLoginEvent> get loginEvents` - such as logged-in, credentials-rejected.
* `Stream<void> get completionEvents` to observe when synchronization has completed.
* `Stream<SyncConnectionEvent> get connectionEvents` to observe connection events.

Note that these streams don't buffer events so unless you're subscribed, no events are collected. Additionally, don't forget to cancel the subscription when you don't care about the information anymore, to free up resources.

```dart
final client = Sync.client(...);
final subscription = client.loginEvents.listen((SycnLoginEvent event) { 
  if (event == SyncLoginEvent.loggedIn) print('Logged in successfully');
});

client.start();

...

// don't forget unsubscribe if you don't care about the events anymore
subscription.cancel();
```
{% endtab %}

{% tab title="C++" %}
```cpp
struct LoginListener : public obx::SyncClientLoginListener {
    void loggedIn() noexcept override;
    void loginFailed(OBXSyncCode code) noexcept override;
};

auto loginListener = std::make_shared<LoginListener>();
syncClient->setLoginListener(loginListener);

// there can be only one listener of a given type, so calling again with a 
// different callback changes the listener (un-assigns the previous one)
syncClient->setLoginListener(...);

// reset (remove) a listener
syncClient->setLoginListener(nullptr);
```
{% endtab %}

{% tab title="C" %}
```c
void login_listener(void* arg) {
    (*(int*) arg)++;
}

void main() {
    ...
    int login_listener_arg = 0;
    obx_sync_listener_login(sync_client, login_listener, &login_listener_arg);
}

// there can be only one listener of a given type, so calling again with a 
// different callback changes the listener (un-assigns the previous one)
obx_sync_listener_login(sync_client, ..., ...);

// reset (remove) a listener
obx_sync_listener_login(sync_client, NULL, NULL);
```
{% endtab %}

{% tab title="Go" %}
```go
syncClient.SetLoginListener(func() { println("Logged-in") })

// there can be only one listener of a given type, so calling again with a 
// different callback changes the listener (un-assigns the previous one)
syncClient.SetLoginListener(func() { ... })

// reset (remove) a listener
syncClient.SetLoginListener(nil)
```
{% endtab %}
{% endtabs %}

## Advanced

### Listening to incoming data changes

For advanced use cases, it might be useful to know exactly which objects have changed during an incoming sync update. This is typically not necessary, as observing a box or a query may be easier.

On each sync update received on the client, the listener is called with an array of "Sync Change" objects, one for each affected entity type. It includes a list of affected object IDs - the ones that were put or removed in the incoming update.

{% tabs %}
{% tab title="Java" %}
Use `changeListener(changeListener)` when building the client and pass a `SyncChangeListener` to receive detailed information for each sync update. Or set or remove it at any later point using `SyncClient.setSyncChangeListener(changeListener)`.

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
// Set the listener when building the client.
syncBuilder.changeListener(changeListener);
// Or set the listener later.
syncClient.setSyncChangeListener(changeListener);

// Calling again replaces an existing listener.
syncClient.setSyncChangeListener(changeListener);
// Remove an existing listener.
syncClient.setSyncChangeListener(null);
```
{% endtab %}

{% tab title="Kotlin" %}
Use `changeListener(changeListener)` when building the client and pass a `SyncChangeListener` to receive detailed information for each sync update. Or set or remove it at any later point using `SyncClient.setSyncChangeListener(changeListener)`.

```kotlin
val changeListener = SyncChangeListener { syncChanges ->
    for (syncChange in syncChanges) {
        // This is equal to Example_.__ENTITY_ID.
        val entityId = syncChange.entityTypeId
        // The @Id values of changed and removed entities.
        val changed = syncChange.changedIds
        val removed = syncChange.removedIds
    }
}
// Set the listener when building the client.
syncBuilder.changeListener(changeListener)
// Or set the listener later.
syncClient.setSyncChangeListener(changeListener)

// Calling again replaces an existing listener.
syncClient.setSyncChangeListener(changeListener)
// Remove an existing listener.
syncClient.setSyncChangeListener(null)
```
{% endtab %}

{% tab title="Swift" %}
_Coming soon!_
{% endtab %}

{% tab title="Dart/Flutter" %}
Use `Stream<List<SyncChange>> get changeEvents` on the SyncClient to receive detailed information for each sync update. Make sure to cancel the subscription when you don't need the information anymore to clear up resources.

```dart
final subscription = client.changeEvents
    .listen((List<SyncChange> event) => event.forEach((change) {
          print('${change.entity}(${change.entityId}) '
              'puts=${change.puts} removals=${change.removals}');
        }));
        
// For connects and disconnects subscribe to client.connectionEvents

// For login status, subscribe to client.loginEvents

// For sync completion, subscribe to client.completionEvents

// ...don't forget unsubscribe if you don't care about the events anymore
subscription.cancel();
```
{% endtab %}

{% tab title="C++" %}
```cpp
/// Sample listener collecting all puts and removals
class StatsCollector {
    struct EntityChanges {
        std::vector<obx_id> puts;
        std::vector<obx_id> removals;
    };
    std::unordered_map<obx_schema_id, EntityChanges> statsPerEntity;

    /// Receives changes on the object instance, forwarded by the static forward().
    void onChanges(const OBX_sync_change_array* changes) {
        for (size_t i = 0; i < changes->count; i++) {
            const OBX_sync_change& change = changes->list[i];
            EntityChanges& stats = statsPerEntity[change.entity_id];
            if (change.puts) collect(change.puts, stats.puts);
            if (change.removals) collect(change.puts, stats.removals);
        }
    }

    /// Update given vector by adding all ids from current change list.
    void collect(const OBX_id_array* ids, std::vector<obx_id>& targetVector) {
        targetVector.reserve(targetVector.size() + ids->count);
        for (size_t i = 0; i < ids->count; i++) {
            targetVector.push_back(ids->ids[i]);
        }
    }

public:
    /// Just forwards the C-callback to the instance of this class.
    static void forward(void* arg, const OBX_sync_change_array* changes) {
        static_cast<StatsCollector*>(arg)->onChanges(changes);
    }
};


void main() {
    ...
    StatsCollector collector;
    syncClient->setChangeListener(StatsCollector::forward, &collector);
}
```
{% endtab %}

{% tab title="C" %}
```c
void on_puts(void* arg, obx_schema_id entity_id, const OBX_id_array* ids) {
   //...
}

void on_removals(void* arg, obx_schema_id entity_id, const OBX_id_array* ids) {
    //...
}

void change_listener(void* arg, const OBX_sync_change_array* changes) {
    for (size_t i = 0; i < changes->count; i++) {
        const OBX_sync_change* change = &changes->list[i];
        if (change->puts) {
            on_puts(arg, change->entity_id, change->puts);
        }
        if (change->removals) {
            on_removals(arg, change->entity_id, change->removals);
        }
    }
};

void main() {
    ...
    obx_sync_listener_login(sync_client, change_listener, &change_listener_arg);
}
```
{% endtab %}

{% tab title="Go" %}
```go
syncClient.SetChangeListener(func(changes []*objectbox.SyncChange) {
		fmt.Printf("received %d changes\n", len(changes))
		for i, change := range changes {
			fmt.Printf("change %d: %v\n", i, change)

			// change.EntityId is a "model-entity-id", e.g. we can choose to process
			// only changes on Entity `User`, with the generated `UserBinding`:
			if change.EntityId == model.UserBinding.Id {
			  fmt.Printf("put user IDs %v\n", change.Puts)
			  fmt.Printf("deleted user IDs %v\n", change.Removals)
			}
		}
	})
```
{% endtab %}
{% endtabs %}

### Checking for outgoing changes

Sometimes you want to know if there are any ("outgoing") changes on the local device that are not yet synchronized to the server.
This is helpful to when you want to show the sync status in the user interface, or trigger some logic.
Technically, ObjectBox uses a message queue here and there's an API that gives you number of outgoing messages.
If this number reaches zero, it means that all changes done on this device have been synced (sent) to the server.
It's fine to call this API periodically, e.g. every second, if you want to know the current status.

{% tabs %}
{% tab title="Java" %}
```java
// Not yet available (coming soon)
```
{% endtab %}

{% tab title="Kotlin" %}
```kotlin
// Not yet available (coming soon)
```
{% endtab %}

{% tab title="Swift" %}
```swift
// Not yet available (coming soon)
```
{% endtab %}

{% tab title="Dart/Flutter" %}
```dart
var count = syncClient.outgoingMessageCount();
```
{% endtab %}

{% tab title="C++" %}
```cpp
uint64_t count = syncClient.outgoingMessageCount();
```
{% endtab %}

{% tab title="C" %}
```c
uint64_t count;
obx_err err = obx_sync_outgoing_message_count(sync, 0, &count)
```
{% endtab %}

{% tab title="Go" %}
```go
// Not yet available
```
{% endtab %}
{% endtabs %}

### Listeners concurrency

Some events may be issued in parallel, from multiple background threads. To help you understand when and how you need to take care of concurrency (e.g. use mutex/atomic variables), we've grouped the sync listeners to these two groups:

* [State listeners](sync-client.md#listening-to-events) - listening to login success/failure, connection status, sync complete.
* [Data change listener](sync-client.md#listening-to-sync-updates) - listening to incoming data changes.

There can be only one event executed at any single moment from a listener in a single group. You can imagine this as if there were two parallel threads, one could only issue "state" events, the other only "data change" events.

### Controlling sync updates behavior

By default, after the Sync client is logged in, its database is updated from the server and the client will automatically subscribe for any future changes. For advanced use cases, like unit testing, it is possible to control when the client receives data updates from the server.

To change the default behavior, configure the "Request Updates Mode" before starting the client connection. Three modes are available:

* **automatic** (default): receives updates on login and subscribes for future updates.
* **automatic, but no pushes:** receives updates on login but doesn't subscribe for future updates.
* **manual:** no automatic updates on login or on any updates in the future.

When using one of the non-default modes, synchronization can be controlled after login during application runtime by requesting and cancelling updates using the client:

{% tabs %}
{% tab title="Java" %}
```java
SyncClient syncClient = syncBuilder
        // Turn off automatic sync updates.
        .requestUpdatesMode(RequestUpdatesMode.MANUAL)
        .build();

// Wait for login attempt, proceed if logged in.
syncClient.awaitFirstLogin(20 * 1000 /* ms */);
if (syncClient.isLoggedIn()) {
    // Turn on automatic sync updates.
    syncClient.requestUpdates();
    
    // Turn off automatic sync updates, cancel ongoing sync.
    syncClient.cancelUpdates();
    
    // Request one-time update.
    // Will update client with latest data.
    syncClient.requestUpdatesOnce();
}
```
{% endtab %}

{% tab title="Kotlin" %}
```kotlin
val syncClient = syncBuilder
        // Turn off automatic sync updates.
        .requestUpdatesMode(RequestUpdatesMode.MANUAL)
        .build()

// Wait for login attempt, proceed if logged in.
syncClient.awaitFirstLogin(20 * 1000 /* ms */)
if (syncClient.isLoggedIn()) {
    // Turn on automatic sync updates.
    syncClient.requestUpdates()
    
    // Turn off automatic sync updates, cancel ongoing sync.
    syncClient.cancelUpdates()
    
    // Request one-time update.
    // Will update client with latest data.
    syncClient.requestUpdatesOnce()
}
```
{% endtab %}

{% tab title="Swift" %}
_Coming soon!_
{% endtab %}

{% tab title="Dart/Flutter" %}
```dart
final client = Sync.client(...);

client.setRequestUpdatesMode(SyncRequestUpdatesMode.manual);
client.start(); // Connect but don't synchronize yet.

// Turn on sync updates and subscribe for pushes.
client.requestUpdates(subscribeForFuturePushes: true);

// Cancel ongoing synchronization & unsubscribe from future updates.
client.cancelUpdates();

// Alternatively, catch up with the server but don't subscribe for future.
// You can call this instead of subscribing to do one-time updates as needed.
client.requestUpdates(subscribeForFuturePushes: false);
```
{% endtab %}

{% tab title="C++" %}
```cpp
std::shared_ptr<obx::SyncClient> syncClient = obx::Sync::client(store, ...);

syncClient->setRequestUpdatesMode(OBXRequestUpdatesMode_MANUAL);
syncClient->start();  // Connect but don't synchronize yet.

// Turn on sync updates and subscribe for pushes.
syncClient->requestUpdates(true);

// Cancel ongoing synchronization & unsubscribe from future updates.
syncClient->cancelUpdates();

// Alternatively, catch up with the server but don't subscribe for future.
// You can call this instead of subscribing to do one-time updates as needed.
syncClient->requestUpdates(false);
```
{% endtab %}

{% tab title="C" %}
```cpp
OBX_sync* sync_client = obx_sync(store, ...);
obx_sync_credentials(sync_client, ...);

obx_sync_request_updates_mode(sync_client, OBXRequestUpdatesMode_MANUAL);
obx_sync_start(sync_client);  // Connect but don't synchronize yet.

// Turn on sync updates and subscribe for pushes.
obx_sync_updates_request(sync_client, true);

// Cancel ongoing synchronization & unsubscribe from future updates.
obx_sync_updates_cancel(sync_client);

// Alternatively, catch up with the server but don't subscribe for future.
// You can call this instead of subscribing to do one-time updates as needed.
obx_sync_updates_request(sync_client, false);
```
{% endtab %}

{% tab title="Go" %}
```go
syncClient, err := objectbox.NewSyncClient(...)

syncClient.SetRequestUpdatesMode(objectbox.SyncRequestUpdatesManual)
syncClient.Start()  // Connect but don't synchronize yet.

// Turn on sync updates and subscribe for pushes.
syncClient.RequestUpdates(true)

// Cancel ongoing synchronization & unsubscribe from future updates.
syncClient.CancelUpdates()

// Alternatively, catch up with the server but don't subscribe for future.
// You can call this instead of subscribing to do one-time updates as needed.
syncClient->requestUpdates(false)
```
{% endtab %}
{% endtabs %}
