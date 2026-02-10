---
description: >-
  To set up ObjectBox Sync Server to your needs, there are various configuration
  options, which are presented on this page.
---

# Configuration

There are two approaches to configure ObjectBox Sync Server:

* command line parameters (CLI): simple/quick approach for basic settings (limitations apply)
* configuration file (JSON): recommended for complex settings and required for sync filters and clusters

Note that both approaches can be [combined](configuration.md#combining-cli-and-file-configuration) (CLI parameters take precedence over file configuration).

## Configuration via command line (CLI)

Running the Sync Server from the command line is a simple way to get started. It's a good idea to look at the output of running `sync-server --help` (your output may vary, e.g. when using a newer version of the Sync Server).

<details>

<summary>Sync Server CLI Help Output (click to expand)</summary>

```
sync-server --help
001-16:12:08.9830 [INFO ] [SvSyAp] Starting ObjectBox Sync Server version 6 (protocol version: 8, core: 5.1.0-2026-01-19 (SyncServer, http, graphql, admin, tree, dlog, cluster, backup, lmdb, VectorSearch, SyncMongoDb))
ObjectBox Sync Server
Usage:
  sync-server [OPTION...]

      --admin-bind arg          host/IP and port the admin http server 
                                should listen on (default: 
                                http://127.0.0.1:9980)
      --admin-threads arg       number of the worker threads used by admin 
                                http server (default: 4)
      --admin-off               do not start the admin http server
      --async-tx-slot arg       If async DB TXs are "too fast", this adds a 
                                delay to fill up the slot (default: 3000)
      --auth-obx-admin          Enable ObjectBox Admin Users database for 
                                authentication
      --auth-required arg       Comma-separated list of authentication 
                                methods (credential types) required for 
                                clients to connect (default: "")
  -b, --bind arg                host/IP and port the sync server should 
                                listen on (default: "")
  -c, --conf arg                configuration file path (default: 
                                sync-server-config.json)
      --cert arg                certificate file path (default: "")
      --cluster-id arg          cluster ID to enable cluster mode for 
                                servers (default: "")
      --debug                   enable debug logs
      --fixed-follower          the server never becomes the leader of the 
                                cluster
      --fixed-leader            make the server the (only!) leader of the 
                                cluster (danger: read docs carefully!)
  -d, --db-directory arg        directory where the database is stored 
                                (default: objectbox)
      --db-max-size arg         database size limit; use a number with a 
                                unit (K/M/G/T), e.g. 256G (default: 
                                104857600K)
  -h, --help                    show help
      --jwt-public-key-url arg  URL to the public key for JWT token 
                                validation (default: "")
      --jwt-claim-aud arg       Expected audience claim in JWT token 
                                (default: "")
      --jwt-claim-iss arg       Expected issuer claim in JWT token 
                                (default: "")
  -m, --model arg               schema model file to load (JSON) (default: 
                                "")
      --mongo-url arg           MongoDB Sync Connector: URL to the MongoDB 
                                instance (default: "")
      --mongo-db arg            MongoDB Sync Connector: name of the primary 
                                MongoDB database to sync (default: "")
      --mongo-initial-import    MongoDB Sync Connector: automatically 
                                triggers the full sync/import from MongoDB
      --no-stacks               disable stack traces when logging errors
      --unsecured-no-authentication
                                [UNSECURE] allow connections without 
                                authentication
      --workers arg             number of workers for the main task pool 
                                (default is hardware dependent, e.g. 3 * 
                                CPU "cores") (default: 0)
      --restore-backup arg      restores the DB to the given backup file 
                                (by default, restoration takes place only 
                                if no DB exist)
      --backup-overwrites-db    forces the restoration of the backup even 
                                if the DB already exists (danger: 
                                overwrites the db permanently!)
  -v, --version                 just prints the version and then exits 
                                immediately

```

</details>

More details about the options can be found in the section on the configuration file. Just note that the naming convention is different (e.g. `dbMaxSize` instead of `db-max-size`), but both refer to the same underlying option.

## Configuration file

In the long run, you should store the configuration in a JSON file. This is the preferred choice if our options are getting more complex.
Also, you can check in the configuration file into version control.

Note that some options are only available in the config file (not the CLI):

* [Cluster](sync-cluster.md)
* [Sync Filters](sync-filters.md)
* [Individual debug log flags](#developer-and-debug-options)

By default, the configuration file is read from `sync-server-config.json` in the current working directory. To use a different location, supply it via the `--conf <path-to-config>` option.

Some options have a default value, so if you are OK with the default, there is no need to specify it.

Example file for a local development setup (not intended for production use as auth is disabled):

```json
{
  "dbDirectory": "objectbox",
  "dbMaxSize": "100G",
  "modelFile": "objectbox-model.json",
  "bind": "ws://0.0.0.0:9999",
  "adminBind": "http://127.0.0.1:9980",
  "_note": "unsecuredNoAuthentication should not be used in production",
  "unsecuredNoAuthentication": true,
  "debugLog": true
}
```

{% hint style="info" %}
Start JSON keys with underscore (`_`) to add comments or to temporarily disable a setting.
These keys are exempt from validation and will be ignored by the Sync Server.

Example: `"_debug": true` and `"_note1": "my comment"` are ignored.
{% endhint %}

### Primary options

* `dbDirectory` directory where the database is stored (default: "objectbox").
* `dbMaxSize` database size limit; use a number with a unit, e.g. 256G (default: 100G)&#x20;
  * `K` for kibibytes, i.e. 1024 bytes
  * `M` for mebibytes, i.e. 1024 kibibytes
  * `G` for gibibytes, i.e. 1024 mebibytes
  * `T` for tebibytes, i.e. 1024 gibibytes
* `modelFile` schema (model) file to create the database with or to use for a schema update
* `bind` Sync server will bind on this URL (scheme, host and port). It should look like `ws://hostname:port`, for example `ws://127.0.0.1:9000`. You can also bind to a specific IP address on the server machine by providing the exact address, as given by `ifconfig` or `ip addr`, e.g. `ws://192.168.0.125:9999`.
* `adminBind` HTTP server (admin/web UI) will bind on this URL (schema, host and port combination).

### Developer and debug options

* `unsecuredNoAuthentication` allows connections without any authentication. Note: this is unsecure and should only be used to simplify test setups.
* `debugLog` enable debug logs with `true`
* `noStacks` disable stack traces when logging errors (default: `false`)

When using debug logs, advanced users can enable additional logs for internal components (e.g. ObjectBox support may ask you to enable specific logs).
This is done using boolean flags in the `log` JSON object (all default to `false` when omitted).

- **transactionRead**: Log the lifecycle of read transactions (begin/commit/abort).
- **transactionWrite**: Log the lifecycle of write transactions and commits to help diagnose write-related issues.
- **queries**: Log executed queries to aid in understanding which lookups are performed at runtime.
- **queryParameters**: Log parameter values bound to queries. May include sensitive data.
- **asyncQueue**: Log asynchronous operations.
- **cacheHits**: Log cache hits and misses to evaluate cache effectiveness (note: only a few metadata items are cached).
- **cacheAll**: Log all cache operations (puts/gets/evictions); very verbose and intended for deep diagnostics.
- **tree**: Log special tree data models.
- **exceptionStackTrace**: Attempt to include stack traces for certain internal error logs (Linux-only, experimental).
- **threadingSelfTest**: Run a quick threading self-test at startup and log its progress and results.
- **wal**: Enable detailed write-ahead logging (WAL, not used by default) debug output.
- **idMapping**: Log how IDs are mapped between local and global spaces during synchronization.
- **syncFilterVariables**: Log values of sync filter variables per client (e.g. derived from JWT or the login message).
  May include sensitive data.

Example to enable sync-related debug logs (this quickly gets excessive; don't do this by default):

```json
{
  "debugLog": true,
  "log": {
    "idMapping": true,
    "syncFilterVariables": true
  }
}
```

### Authentication options

* `auth.jwt` JWT is the primary method for authentication. See the [JWT authentication page](jwt-authentication.md) for details.

### Sync filter expressions

* `syncFilters` this JSON object contains all filter expressions.
  Each filter has the type as key and a string value as the expression.
  Details are available in the [sync filters](sync-filters.md) page.

### Sync history size limit

The Sync Server maintains a sync history (sync logs), which is used to synchronize clients that reconnect after being offline.
By default, this history grows without limit, which can cause the database to grow indefinitely.
To prevent this, you can configure a maximum history size.
Once the limit is reached, old history logs are automatically deleted.

{% hint style="info" %}
Sync clients that were offline for a longer time may no longer be able to synchronize via delta sync. which is powered by the sync history.
In that case, these Sync clients will sync from scratch (full sync); any outgoing data will still be sent to the server.
{% endhint %}

* `historySizeMaxKb` maximum size (in kibibytes) of the sync TX log history.
  Once this size is reached, old sync logs are deleted to stay below the limit.
  Default: `0` (no limit).
* `historySizeTargetKb` target size (in kibibytes) when cleaning up old TX logs.
  When the maximum size is reached, old sync logs are deleted until this target size is reached.
  This allows the Sync Server to reserve some space for future sync logs and thus "delays" the next cleanup. 
  The value must be lower than `historySizeMaxKb`.
  Default: `0` (same as `historySizeMaxKb`, i.e. delete just enough to stay below the limit).

{% hint style="info" %}
It's highly recommended to set both values with `historySizeTargetKb` significantly lower than `historySizeMaxKb`.
This ensures that the Sync Server does the cleanup only occasionally, which is more efficient.
{% endhint %}

Example configuration to limit history to 5 GB, cleaning up to 4.5 GB (thus triggering cleanup every ~500 MB of sync logs):

```json
{
  "historySizeMaxKb": 5242880,
  "historySizeTargetKb": 4718592
}
```

{% hint style="info" %}
When initially setting a limit to an existing database well above the limit, the database size will not decrease.
The newly available space inside the database is reserved for future data.
Nevertheless, the database file should not grow any further once a limit has been set and reached.
This is unless the "active data" grows, for example, by inserting more and/or larger objects. 
{% endhint %}

### Backup and restore (CLI only)

These options are available only via command line arguments (not via JSON config).

* `--restore-backup <file>` restores the database from the given backup file.
  By default, restoration only takes place if no database exists yet.
* `--backup-overwrites-db` forces the restoration of the backup even if a database already exists.
  **Danger:** this permanently overwrites the existing database.

### Advanced options

* `adminThreads` number of threads the HTTP server uses (default: 4). A low number is typically enough as it's for admins only. You may need to increase if running in some cloud setups that keep the connections active (e.g. Kubernetes).
* `auth.sharedSecret` enables the shared secret authentication.
  Can be a plain string (the secret) or an object with `value` (the secret) and `required` (boolean; if `true`, clients must provide a shared secret to connect). Example as object:
  ```json
  "sharedSecret": { "value": "my-secret", "required": true }
  ```
* `auth.google.clientIds` a list of GoogleAuth client IDs (strings). The enclosing `auth.google` object also accepts a `required` boolean (if `true`, clients must provide Google credentials).
* `auth.obxAdmin` enables ObjectBox Admin users for sync authentication (e.g. for small deployments and tests). Can be `true` or an object with a `required` boolean (if `true`, clients must provide Admin user credentials). Example as object:
  ```json
  "obxAdmin": { "required": true }
  ```
* `asyncTxSlot` if asynchronous DB transactions are "too fast", this adds a delay (in microseconds) to fill up the transaction slot. This can reduce the maximum amount of transactions and thus disk usage (default: 3000).
* `certificatePath` Supply a SSL certificate directory to enable SSL. This directory must contain the files `cert.pem` and `key.pem`.
* `workers` sets the number of concurrent workers for the main task pool (default is hardware dependent, e.g. 3 times the number of CPU cores).

## Clusters
To set up a cluster, please refer to the [cluster](sync-cluster.md) page for specific configuration options.

## Authentication

Authentication settings for clients are required; the Sync Server won't start without them. If you try, it should look something like this:

```
$ ./sync-server --model=objectbox-model.json
...
001-13:05:07.3526 [ERROR] [SySvAp] Runtime error: Authenticator must be set before starting
001-13:05:07.4524 [INFO ] [SvSync] Stopped (port 0)
Authenticator must be set before starting
```

{% hint style="info" %}
During development on your private network, you can disable authentication altogether using the option `--unsecured-no-authentication`. This allows all clients, which know the server's URL, to connect without additional checks.

_Warning:_ it should be obvious that this setting is not intended for production usage.
{% endhint %}

For production usage, please refer to the [JWT authentication](./jwt-authentication.md) page on how to authenticate your clients.

Other authentication methods are mentioned above in the configuration overview, i.e. Google Authentication with client IDs, shared secret, Admin users.
Typically, we recommend using JWT, but there may be occasions where you need to use other authentication methods. Let the ObjectBox team know about your use case and requirements. E.g. it is possible to define multiple authenticators.

## Combining CLI and file configuration

You can mix both approaches, i.e. have a configuration file and use command line (CLI) options. In this case, CLI options have precedence over the options in the JSON config file. Thus, you can store your base configuration in a file, and override or add settings by providing command line arguments.
