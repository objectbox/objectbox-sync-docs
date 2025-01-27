---
description: >-
  To setup ObjectBox Sync Server to your needs, there are various configuration
  options, which are presented on this page.
---

# Sync Server Configuration

There are two approaches to configure ObjectBox Sync Server:

* command line parameters (CLI): simple/quick approach for most settings
* configuration file (JSON): recommended for complex settings and required for clusters

Note that both approaches can be [combined](sync-server-configuration.md#combining-cli-and-file-configuration).

## Configuration via command line (CLI)

Running the Sync Server from the command line is simple way to get started. It's a idea to look at the output of running `sync-server --help` (your output may vary, e.g. when using a newer version of the Sync Server).

<details>

<summary>Sync Server CLI Help Output (click to expand)</summary>

```
sync-server --help
001-16:12:08.9830 [INFO ] [SvSyAp] Starting ObjectBox Sync Server version 5 (protocol version: 6, core: 4.0.3-2025-01-24 (SyncServer, http, graphql, admin, tree, dlog, cluster, backup, lmdb, VectorSearch, SyncMongoDb))
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

```

</details>

More details about the options can be found in the section on the configuration file. Just note that the naming convention is different (e.g. `dbMaxSize` instead of `db-max-size`), but both refer to the same underlying option.

## Configuration file

Alternatively, you can choose to provide the configuration in a JSON file. This is the preferred choice if the options are getting more complex (e.g. you can checkin the configuration file into version control). Also, it's the only way to configure a [cluster](sync-cluster.md).

By default, the configuration file is read from `sync-server-config.json` in the current working directory. To use a different location, supply it via the `--conf <path-to-config>` option.

Some options have a default value, so if you are OK with the default, there is no need to specify it.

The available options are:

```javascript
{
    "dbDirectory": "objectbox",
    "dbMaxSize": "100G",
    "modelFile": "",
    "bind": "ws://0.0.0.0:9999",
    "adminBind": "http://127.0.0.1:9980",
    "adminThreads": 4,
    "certificatePath": "",
    "auth": {
        "sharedSecret": "",
        "google": {
            "clientIds": []
        }
    }
}
```

* `dbDirectory` directory where the database is stored (default: "objectbox").
* `dbMaxSize` database size limit; use a number with a unit, e.g. 256G (default: 100G)&#x20;
  * `K` for kibibytes, i.e. 1024 bytes
  * `M` for mebibytes, i.e. 1024 kibibytes
  * `G` for gibibytes, i.e. 1024 mebibytes
  * `T` for tebibytes, i.e. 1024 gibibytes
* `modelFile` schema (model) file to create the database with or to use for a schema update
* `bind` Sync server will bind on this URL (schema, host and port). It should look like `ws://hostname:port`, for example `ws://127.0.0.1:9000`. You can also bind to a specific IP address on the server machine by providing the exact address, as given by `ifconfig` or `ip addr`, e.g.  `ws://192.168.0.125:9999`.
* `adminBind` HTTP server (admin/web UI) will bind on this URL (schema, host and port combination).
* `adminThreads` number of threads the HTTP server uses (default: 4). A low number is typically enough as it's for admins only. You may need to increase if running in some cloud setups that keep the connections active (e.g. Kubernetes).
* `certificatePath` Supply a SSL certificate directory to enable SSL. This directory must contain the files `cert.pem` and `key.pem`.
* `auth.sharedSecret` if not empty, enables the shared secret authentication with the given key
* `auth.google.clientIds` a list of GoogleAuth client IDs (strings)
* `unsecured-no-authentication`: allow connections without authentication (note: this is unsecure and shall only be used to simplify test setups.

{% hint style="info" %}
To **setup a cluster**, please refer to the [cluster](sync-cluster.md) page for specific configuration options.
{% endhint %}

## Combining CLI and file configuration

You can mix both approaches, i.e. have a configuration file and use command line (CLI) options. In this case, CLI options have precedence over the options in the JSON config file. Thus, you can store your base configuration in a file, and override or add settings by providing command line arguments.
