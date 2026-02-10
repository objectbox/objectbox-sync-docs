---
description: >-
  Something is not working? This guide helps to identify typical problems
  quickly.
---

# Troubleshooting Sync

## How to reach the Sync Server

Sync Clients specify the URL of the Sync Server. In a test setting, both may be running on the same machine. In this case, you can use ws://127.0.0.1 as the destination; 127.0.0.1 is the IP address of localhost. If it's separate machines, you need to exchange 127.0.0.1 with an reachable IP address of the server, or, some valid DNS name.

{% hint style="info" %}
Using Android emulator? You can use 10.0.2.2 to reach the host (the machine running the emulator). Thus, specify "ws://10.0.2.2" in your client if you run the Sync Server on the same machine. For details on Android emulator networking, see [here](https://developer.android.com/studio/run/emulator-networking).
{% endhint %}

## Check the network connection

If it looks like data is not synchronized, usually the first thing to check is the network connection between the devices. Usually it's helpful to start the Sync server with the admin web app enabled, so you can e.g. check the connection using the HTTP server URL in the standard browser of clients.

{% hint style="info" %}
See [Sync Server configuration](sync-server/) on how to enable HTTP and options.
{% endhint %}

1. Using a standard web browser, can you reach the Sync host on port 9980? E.g. first try it on the machine running Sync server via [http://127.0.0.1:9980](http://127.0.0.1:9980). The ObjectBox Admin web app should show up. If this fails, check the server's configuration.
2. Try to reach the Sync port (9999 by default) using a web browser (or a tool cURL): [http://127.0.0.1:9999](http://127.0.0.1:9999). You should see a short plain text response if this connection is fine.
3. To check that the hostname is correctly registered, try to connect to the Sync Server using a web browser. You should be able to reach the following addresses: [http://your-hostname.com:9980](http://your-hostname.com:9980) (the ObjectBox Admin web app) or [http://your-hostname.com:9999](http://your-hostname.com:9999) (the Sync endpoint). If the pages are loaded and the browser doesn't hang, then your hostname was resolved correctly. You can further investigate hostname issues by using command line tools like `nslookup`.
4. Next, if the client runs on another machine, check the same ports from client's machine in a web browser. Of course, you need to exchange 127.0.0.1 with an reachable IP address of the server, or, some valid DNS name.

If one of those steps fail, you need to check your network configuration. Like any networking application, ObjectBox Sync relies on a functioning network.

## Check the logs

Sync Server has two kind of logs: standard logs that go to standard output and "log events" that are persisted in the database.

### Enable debug logging

{% hint style="info" %}
Debug logging is available for standard logs (not log events). You need access to the **standard output** of the Sync Server. This may be straight-forward for most configurations, but may be "hidden" for some setups. For example, when running with Docker Compose, you may need to run `docker compose logs` or something like `docker compose logs -f --tail=50 sync-server` to follow Sync Server logs.
{% endhint %}

The network connection seems fine? Then let's get additional information to the logs. The Sync server comes with a switch to turn on debug logging. Logs go to standard output and are typically very sparse. Debug logs on the other hand provide you with a lot of extra information, which can help you to diagnose problems. For example, a client got disconnected? The debug logs usually tell why.

There are three ways to enable debug logs (see also [Sync Server configuration](sync-server/configuration.md)):

* Use the Admin UI on the "Status" page to find switch to enable debug logging. Note: since this requires the Sync Server to be already running, this will not log while the server starts. 
* Use the `--debug` CLI argument when starting the server.
* In the server configuration file, add `"debugLog": true`. If the server is running, you need to restart it to apply the change.

### Log events

Unlike standard logs, "log events" capture important events and are persisted to be available across server restarts. Thus, these may give additional context for issues that span multiple restarts. You can check them using the Admin UI on the "Log Events" page.

{% hint style="info" %}
You can export log events to a file using the download link at the bottom of the page.
{% endhint %}

### Client logs

While the server logs are the first thing to check, the client logs can also help to diagnose certain issues. Sync clients log only sparsely, e.g. when problems occur. So when you don't see anything in the client logs, it's likely a connection problem, which are covered here too, or the issue can be found on the server side. The client logs go to standard output or logcat on Android.

## System utilities inside the Docker container

If you are familiar with Linux utilities, you can use them directly inside the Docker Sync Server container.
Starting with version 2025-07-17 of the Docker container, these packages are pre-installed:
iputils, iproute, procps-ng, strace, lsof, and nmap-ncat.

### Attach to a running container

Example to "attach" to a running Sync Server container:

```bash
docker ps # Copy the container ID for objectboxio/sync-server-trial
docker exec -it --user 0 <container-id> /bin/bash # root shell
# or, if you do not want to run as root:
 docker exec -it <container-id> /bin/bash # non-root
```

### Pre-installed commands

Then you are inside the running container. For starters, try these commands:

* `top`: shows system info and the running processes;
  you should see the Sync Server process with process ID (PID) 1 and "sync-server" as the command.
  Also, since you "attached" to the container you should see a "bash" and a "top" process.
* `ss -ltnp`: show listening sockets; at "Local Address:Port" you should see 0.0.0.0:9999 and 0.0.0.0:9980.
  The IP address 0.0.0.0 tells that it listens on all interfaces. 9999 is the Sync endpoint, 9980 is the Admin UI.
* `ping 8.8.8.8`: ping Google's DNS server to check if container can reach the Internet.

### Install additional packages

The base image is a Rocky Linux container, so you can use `microdnf` to install additional packages.
To do so, ensure that you have a root shell using `--user 0` for the docker `exec command` (see above).
For example, to install the bind-utils package to get `dig` and `nslookup` commands: `microdnf install -y bind-utils`.
(Note: bind-utils comes with larger dependencies and thus is not pre-installed.)

## Clients do not connect

If Sync clients do not connect to the server, please doublecheck the [Sync Client setup](sync-client.md), specifically: 

* You are using a sync-enabled library of the ObjectBox SDK.
* The URL to the Sync Server is correct (see above to ensure the URL is reachable).

## Clients connect but do not sync

Can you see the clients connecting to the server in the (debug) logs, but no data is synchronized?
Double check that your entity types are sync enabled. If they are not, ObjectBox will store the objects only locally.
Follow this checklist:

* Did you add a "sync annotation" for the types you want to sync? The [Sync Client setup](sync-client.md) page has the details for the ObjectBox API of the programming language you are using.     
* Ensure that the generated files data model are up-to-date. Hint: in the model JSON file you should see `"flags": 2` for the entity types you want to sync (`2` is actually a bit flag that enables sync). 
* Ensure that the up-to-date model JSON is also used for the server config.

## IDs do not match across devices

You may notice that IDs of objects stored on one device may not always match the IDs on another device. Well, that's not a bug, but a feature. :slight\_smile:  Check the [docs on Object ID mapping](data-model/object-ids.md) and the possibility to use global IDs instead.

## MongoDB-specific issues

Please check the page [MongoDB Sync Connector](mongodb-sync-connector/README.md) and its subpage for MongoDB-specific issues and troubleshooting. Typical issues include the MongoDB user configuration, and not triggering the initial "Full Sync".

## Sync slows down

If you notice that sync performance degrades over time, check for both conditions apply to you:

* Remove operations are used regularly in your app
* Sync filters are enabled

### Symptoms

* Sync takes longer than expected, particularly when catching up after being offline.
* Server debug logs show that an unusual amount of messages are sent to clients. 
* You may see log entries like: `Did not remove object because no local ID mapping found for <ID>`.
  These are expected but should decrease over time with the setting below.

### Cause

"Legacy" remove operations do not contain sufficient data for sync filters.
This results in clients processing many unnecessary remove transactions.

### Solution

Ensure you have the latest Sync client version and enable the `RemoveWithObjectData` [sync flag](sync-client.md#sync-flags).
This flag includes the full object data with remove operations, allowing the server to filter them out based on sync filter conditions.
Also, ensure to have an up-to-date Sync server version.

{% hint style="info" %}
**Performance improvements are gradual.** The benefits depend on the overall client population running the updated version. Old clients without the flag will still indirectly slow down new ones, as the server cannot filter remove operations for them. Once a significant portion of clients are updated, sync performance should improve noticeably.
{% endhint %}

## Sync server database keeps growing

You may notice that the Sync Server database keeps growing over time.
This typically happens if you have a lot of data changes ongoing, even if the data volume in the current "visible database" does not grow.
The most likely cause is the accumulation of sync history logs.

### Cause

The Sync Server maintains a history of history logs to synchronize clients that reconnect after being offline.
By default, **there is no size limit** on this history, so it grows indefinitely as new transactions are processed.
Over time, this can consume significant disk space.

### Solution

Configure a maximum history size using the `historySizeMaxKb` and `historySizeTargetKb` options in your JSON configuration file.
Once the limit is reached, the Sync Server automatically deletes old TX logs.

For details on these options, see the [configuration page](sync-server/configuration.md#sync-history-size-limit).

### Trade-off

Limiting the history size means that clients that have been offline for a very long time may no longer find their last synced transaction in the history.
In that case, the server triggers a full sync for the client, re-sending all current data.
Choose a history size that balances disk usage with the expected offline duration of your clients.

{% hint style="info" %}
You can monitor the database size using standard file system tools (e.g. `du -sh` on the database directory) or the Admin UI.
If the database is already very large, the size will decrease gradually as old TX logs are cleaned up after setting the limit.
{% endhint %}

## Other hiccups

A checklist of other likely issues:

* [ ] Do you have the latest versions running?
* [ ] Does the server have the latest version of the data model?
* [ ] Does the client version "match" the server version? Typically, Sync Server updates are maintain backward compatibility for clients. But to be safe, check if any breaking changes were announced in the release notes.

## Still having trouble?

We try to provide common troubleshooting tips on this page. If this did not help with your issue, please let us know. The ObjectBox team is here to help you. Here's a checklist to provide us with relevant information, so we can efficiently help you in the best possible way:

* [ ] Let us know the server and client version you are running (are these up-to-date?).
* [ ] Describe the steps that have led to the problem. Does this reproduce the issue? 
* [ ] Attach the server debug logs (from standard output) at the time of the problem and a bit before that. See above on how to enable debug logs.
* [ ] Check the log events in the Admin UI. Ensure that all relevant log events are visible on the page: you can navigate through log events and set the number of events displayed per page. Then, download the log events via the download link at the bottom of the page. Attach this file for us.
* [ ] If it affects Sync clients: check the client logs (standard output or logcat on Android) and attach them for us.
* [ ] Is there anything else you consider noteworthy? What could be related to the issue? Was there a recent change on your side?

In any case, do not hesitate to reach out! :heart:&#x20;
