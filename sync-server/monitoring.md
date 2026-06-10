---
description: >-
  Monitor ObjectBox Sync Server in production using its Prometheus metrics
  endpoint, visualize metrics with Grafana, and set up alerting to get notified
  when something needs your attention.
---

# Monitoring and Alerting

ObjectBox Sync Server exposes its runtime metrics in the [Prometheus text format](https://prometheus.io/docs/instrumenting/exposition_formats/).
This allows you to integrate the Sync Server into a standard monitoring stack:
[Prometheus](https://prometheus.io/) scrapes and stores the metrics,
[Grafana](https://grafana.com/) visualizes them in dashboards,
and either of the two can actively alert you (e.g. via email or Slack) when something goes wrong.

{% hint style="info" %}
For a quick look at live server statistics without any external tooling,
you can also use the "Sync Statistics" page of the [Admin web UI](./#admin-web-ui).
The Prometheus endpoint is the right choice for continuous monitoring in production:
long-term storage, custom dashboards, and alerting.
{% endhint %}

## The metrics endpoint

The metrics endpoint is part of the admin HTTP server (the same server that serves the Admin web UI) and is available at the path `/api/sync/prometheus`.
For example, with the default developer admin configuration (`adminBind` set to `http://127.0.0.1:9980`), the metrics URL is `http://127.0.0.1:9980/api/sync/prometheus`.
You can verify it works by opening it in a browser or using curl:

```shell
curl http://127.0.0.1:9980/api/sync/prometheus
```

This returns the current metric values in plain text, for example:

```
obx_uptime 6231 1781430000000
# HELP obx_messages Number of messages exchanged
# TYPE obx_messages counter
obx_messages{type="recv"} 6824 1781429999641
obx_messages{type="sent"} 7012 1781429999641
...
```

{% hint style="warning" %}
The metrics endpoint currently does not require authentication.
Since it shares the host and port with the Admin web UI, apply the same precautions:
do not expose the admin port to untrusted networks.
Typically, you bind it to localhost or an internal network interface only,
and let Prometheus scrape it from within that network.
{% endhint %}

{% hint style="info" %}
Metric values are sampled from the internal statistics collector, which updates once per second.
Each metric line includes an explicit timestamp (milliseconds since epoch) matching the time the values were sampled.
{% endhint %}

## Available metrics

All metrics are prefixed with `obx_`.
Most are **counters**:
values that only ever increase ("total number of X since server start") and reset to zero when the server restarts.
In Prometheus, you usually look at counters through `rate()` or `increase()` to get "X per second"
or "X in the last N minutes".
**Gauges** in contrast represent a current value that can go up and down
(e.g. the number of currently connected clients).

### General

* `obx_uptime` (counter): server uptime in seconds.
  A value lower than the previous one indicates a server restart.

### Clients and connections

* `obx_connected_clients` (gauge): number of currently connected sync clients.
* `obx_connects` (counter): total number of client connections established.
* `obx_login_successes` (counter): total number of successful client logins (including authentication).
* `obx_heartbeats_received` (counter): total number of heartbeats received from clients.
* `obx_client_failures{type="..."}` (counter): failures related to clients, by `type` label:
  * `login`: general login failures
  * `login_auth_unavailable`: an authentication component was unavailable
  * `login_user_bad_credentials`: clients supplied bad credentials
  * `login_user_no_permission`: authenticated users lacked the permission to connect
  * `msg_sent`: errors while sending messages
  * `heartbeat`: clients disconnected due to missing heartbeats
  * `disconnect`: processing was aborted because the client disconnected
* `obx_errors{type="..."}` (counter): server-side errors, by `type` label:
  * `protocol`: protocol errors, e.g. offending clients
  * `in_handler`: errors inside message handlers

### Messages and data exchange

* `obx_messages{type="recv"|"sent"}` (counter): number of sync protocol messages received from/sent to clients.
* `obx_message_bytes{type="recv"|"sent"}` (counter): number of bytes received/sent via messages
  (measured at the application level; network-level numbers may differ).
* `obx_full_syncs` (counter): number of full syncs performed
  (clients synchronizing from scratch rather than via delta sync).

### Transactions (sync data flow)

* `obx_txs_applied{from="client"|"local"}` (counter): number of transactions applied to the server database,
  split by origin: received from sync clients vs. initiated locally on the server.
* `obx_client_tx_ops_applied` (counter): total number of operations (e.g. puts and removes)
  inside applied client transactions.
* `obx_client_tx_bytes_applied` (counter): total size in bytes of applied client transactions.
* `obx_skipped_tx_dups` (counter): transactions skipped because they were already applied before
  (duplicates, e.g. after reconnects).
* `obx_txs_sent{type="..."}` (counter): transactions sent to clients, by `type` label:
  * `historic`: from the sync history, e.g. to catch up reconnecting clients
  * `historic_merged`: additional transactions merged into historic update messages
  * `new`: "live" updates pushed to connected clients
* `obx_async_db_commits` (counter): database commits done by the asynchronous transaction queue.
* `obx_client_txs_behind` (gauge): how many transactions the most-behind connected client is behind
  the current server state.
* `obx_tx_history_sequence` (counter): the current sequence number of the transaction log history.
* `obx_tx_log_age` (histogram): age of incoming transaction logs when they are stored on the server,
  i.e. the time (in seconds) between a transaction being created at its source and it being applied here.
  This is an indicator of end-to-end sync latency; e.g. high values can point to clients that were offline
  for a while submitting old data, or to a server falling behind.
  Buckets: 0.1, 1, 10, 60 seconds, 1 hour, 1 day, +Inf.

### Server internals

* `obx_queue_length{type="tasks"|"async"}` (gauge): length of internal queues:
  `tasks` is the main worker pool queue, `async` is the asynchronous database transaction queue.
  Persistently growing values indicate the server cannot keep up with the load.
* `obx_task_counts{type="completed"|"failed"|"continued"}` (counter):
  number of internal tasks completed, failed, and continued (rescheduled).
* `obx_task_time{place="...",priority="..."}` (histogram): time (in seconds) tasks spent `in_queue` (waiting)
  and `processing` (executing), per task priority (`low_throttle`, `low_fail`, `regular`, `regular_quick`, `high`).
  Useful to detect server overload: increasing queue times mean tasks wait longer before being processed.
* `obx_cache{from="..."}` (counter): hits and misses of internal ID-mapping caches
  (`global_ids_hits`/`global_ids_misses`, `peer_ids_hits`/`peer_ids_misses`,
  `peer_local_ids_hits`/`peer_local_ids_misses`).
* `obx_cache_size{from="global_ids"|"peer_ids"}` (gauge): number of objects in the internal ID-mapping caches.

### Cluster

The following values are available when running a [Sync Cluster](sync-cluster.md):

* `obx_cluster_peer_state` (gauge): current cluster role of this server:
  0 = unknown (e.g. not started), 1 = leader, 2 = follower, 3 = candidate (an election is in progress).
* `obx_connected_peers` (gauge): number of currently connected cluster peers.
* `obx_forwarded_messages{type="recv"|"sent"}` (counter): messages forwarded between cluster peers
  (e.g. writes forwarded from followers to the leader).

### MongoDB connector

The following values are available when using the [MongoDB Sync Connector](../mongodb-sync-connector/README.md):

* `obx_mongodb_changes{type="..."}` (counter): changes received from the MongoDB change stream, by `type` label:
  * `by_others`: changes made by other applications, to be synced
  * `by_us`: changes the Sync Server itself wrote to MongoDB
  * `filtered_out`: changes not relevant for sync, e.g. unknown collections
  * `unknown_operation`: change stream operations that are not supported
  * `skipped_without_doc`: changes skipped because no document was attached
* `obx_mongodb_errors{type="..."}` (counter): errors in the MongoDB connector, by source:
  * `mongodb`: errors interacting with MongoDB
  * `objectbox`: general errors on the ObjectBox side
  * `objectbox_change_prepare` and `objectbox_change_apply`:
    errors while preparing/applying incoming changes to ObjectBox
* `obx_mongodb_warnings` (counter): total number of warnings issued by the MongoDB connector.
* `obx_mongodb_connector_state` (gauge): current connector state:
  0 = created, 1 = running, 2 = connected, 3 = failure, 4 = stopped.
* `obx_mongodb_connector_running` (gauge): 1 if the connector thread is running, 0 otherwise.
  A simple flag to alert on a stopped connector.
* `obx_mongodb_full_sync_active` (gauge): 1 while a full sync with MongoDB is in progress, 0 otherwise.
* `obx_mongodb_initial_import_required` (gauge): 1 if the initial import from MongoDB has not been done yet,
  0 otherwise.

## Hooking up Prometheus

To let Prometheus scrape the Sync Server, add a scrape job to your Prometheus configuration (`prometheus.yml`).
Note that `metrics_path` must be set, as the Sync Server does not use the default `/metrics` path:

```yaml
scrape_configs:
  - job_name: objectbox-sync-server
    metrics_path: /api/sync/prometheus
    scrape_interval: 10s
    static_configs:
      - targets:
          - "localhost:9980"  # host:port of the Sync Server admin HTTP server
```

After reloading Prometheus, the target should show up as "UP" on the Prometheus status page (Status → Targets).
You can then explore the metrics in the Prometheus expression browser,
e.g. by querying `obx_connected_clients` or `rate(obx_messages[5m])`.

{% hint style="info" %}
If you run the Sync Server in Docker (e.g. via Docker Compose alongside Prometheus),
make sure the admin HTTP server is reachable from the Prometheus container:
bind it to a non-localhost interface inside the container (e.g. `--admin-bind 0.0.0.0:9980`)
and use the container/service name as the target (e.g. `sync-server:9980`).
Do not publish the admin port to the public network.
{% endhint %}

## Visualizing with Grafana

Once Prometheus collects the metrics, add Prometheus as a data source in Grafana
(Connections → Data sources → Prometheus, then enter the Prometheus server URL).
You can then build a Sync Server dashboard. Useful starter panels:

* **Connected clients** (`obx_connected_clients`) - the most basic health indicator of your sync deployment.
* **Sync activity** - transactions applied per second: `rate(obx_txs_applied[5m])`,
  optionally split by the `from` label.
* **Network throughput** - bytes per second: `rate(obx_message_bytes[5m])`, split by the `type` label (recv/sent).
* **Errors and failures** - `increase(obx_errors[5m])` and `increase(obx_client_failures[5m])`, split by `type`.
  In a healthy system, these stay at or near zero.
* **Server load** - queue lengths (`obx_queue_length`) and task queue waiting time, e.g. the 95th percentile:
  `histogram_quantile(0.95, rate(obx_task_time_bucket{place="in_queue"}[5m]))`.
* **Uptime** (`obx_uptime`) - drops to zero indicate restarts.

If you use the MongoDB Sync Connector, also add `obx_mongodb_connector_running` (should constantly be 1)
and `rate(obx_mongodb_changes[5m])` to see data flowing in from MongoDB.

## Alerting

Dashboards are great for analysis, but you do not want to stare at them all day.
Both Prometheus (via [Alertmanager](https://prometheus.io/docs/alerting/latest/overview/))
and [Grafana Alerting](https://grafana.com/docs/grafana/latest/alerting/) can evaluate alert rules
and notify you actively, e.g. via email, Slack, PagerDuty, or a webhook.
Which one to use is mostly a matter of preference:
if you already run Grafana, its built-in alerting is the quickest way to get notifications;
Alertmanager is the classic choice in Prometheus-centric setups.

The general pattern for counters is: alert when the counter *increased* during a recent time window,
i.e. when errors are *recurring* -
a single hiccup (e.g. one failed login due to a typo) usually does not warrant a notification.

### Example 1: Recurring MongoDB connector errors

When the MongoDB Sync Connector repeatedly fails (e.g. MongoDB is down or misconfigured),
you want to know about it quickly - data is not being synchronized in the meantime.
The following Prometheus alert rules fire when the connector is not running,
or when errors keep occurring over a 15-minute window:

```yaml
groups:
  - name: objectbox-sync-server
    rules:
      - alert: MongoDbConnectorNotRunning
        expr: obx_mongodb_connector_running == 0
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "MongoDB connector is not running on {{ $labels.instance }}"
          description: "The MongoDB Sync Connector thread has stopped; data is not being synchronized with MongoDB."

      - alert: MongoDbConnectorErrors
        expr: increase(obx_mongodb_errors[15m]) > 3
        labels:
          severity: warning
        annotations:
          summary: "Recurring MongoDB connector errors ({{ $labels.type }}) on {{ $labels.instance }}"
          description: >-
            {{ $value }} MongoDB connector errors of type {{ $labels.type }} in the last 15 minutes.
            Check the Sync Server logs for details.
```

### Example 2: Spike in client login failures

A sudden burst of login failures can indicate a misconfigured client release,
expired credentials (e.g. an outdated JWT signing key), or someone probing your server.
This rule fires when there are more than 10 login failures within 5 minutes:

```yaml
      - alert: SyncClientLoginFailures
        expr: sum by (instance) (increase(obx_client_failures{type=~"login.*"}[5m])) > 10
        labels:
          severity: warning
        annotations:
          summary: "Many sync client login failures on {{ $labels.instance }}"
          description: >-
            More than 10 client login failures in the last 5 minutes.
            Check client credentials and the authentication setup.
```

### More alerting ideas

Depending on your deployment, also consider alerting on:

* **Server restarts:** `resets(obx_uptime[1h]) > 0` detects (repeated) restarts;
  combine with `for:` to catch crash loops.
* **Server errors:** `increase(obx_errors[15m]) > 0` -
  protocol and handler errors should be rare; recurring ones deserve a look.
* **Overload:** `obx_queue_length` staying high or growing for several minutes means
  the server cannot keep up with the load.
* **Cluster without a leader:** in a [cluster setup](sync-cluster.md),
  a cluster should always have exactly one leader;
  alert when `count(obx_cluster_peer_state == 1) < 1` for more than a minute.
* **No connected clients:** `obx_connected_clients == 0` during hours when you expect activity
  may indicate a network or certificate issue in front of the server.

To set up the same alerts in Grafana instead,
create an alert rule (Alerting → Alert rules → New alert rule) with the same PromQL expression as the query,
and attach a notification policy (contact point) such as email or Slack.
