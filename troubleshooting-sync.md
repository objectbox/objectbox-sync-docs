---
description: >-
  Something is not working? This guide helps to identify typical problems
  quickly.
---

# Troubleshooting Sync

## How to reach the Sync Server

Sync Clients must specify how to reach the Sync Server. In a test setting, both my be running on the same machine. In this case, you can use ws://127.0.0.1 as the destination; 127.0.0.1 is the IP address of localhost. If it's separate machines, you need to exchange 127.0.0.1 with an reachable IP address of the server, or, some valid DNS name.

{% hint style="info" %}
Using Android emulator? You can use 10.0.2.2 to reach the host (the machine running the emulator). Thus, specify "ws://10.0.2.2" in your client if you run the Sync Server on the same machine. For details on Android emulator networking, see [here](https://developer.android.com/studio/run/emulator-networking).
{% endhint %}

## Check the network connection

If it looks like data is not synchronized, usually the first thing to check is the network connection between the devices. Usually it's helpful to start the Sync server with the admin web app enabled, so you can e.g. check the connection using the HTTP server URL in the standard browser of clients.

{% hint style="info" %}
See [Sync Server configuration](objectbox-sync-server.md) on how to enable HTTP and options.
{% endhint %}

1. Using a standard web browser, can you reach the Sync host on port 9980? E.g. first try it on the machine running Sync server via [http://127.0.0.1:9980](http://127.0.0.1:9980). The ObjectBox Admin web app should show up. If this fails, check the server's configuration.
2. Try to reach the Sync port (9999 by default) using a web browser (or a tool cURL): [http://127.0.0.1:9999](http://127.0.0.1:9999). You should see a short plain text response if this connection is fine.
3. To check that the hostname is correctly registered, try to connect to the Sync Server using a web browser. You should be able to reach the following addresses: [http://your-hostname.com:9980](http://your-hostname.com:9980) (the ObjectBox Admin web app) or [http://your-hostname.com:9999](http://your-hostname.com:9999) (the Sync endpoint). If the pages are loaded and the browser doesn't hang, then your hostname was resolved correctly. You can further investigate hostname issues by using command line tools like `nslookup`.
4. Next, if the client runs on another machine, check the same ports from client's machine in a web browser. Of course, you need to exchange 127.0.0.1 with an reachable IP address of the server, or, some valid DNS name.

If one of those steps fail, you need to check your network configuration. Like any networking application, ObjectBox Sync relies on a functioning network.

## Enable debug logging

The network connection seems fine? OK, let's get additional information! The Sync server comes with a switch to turn on debug logging. Logs go to standard output and are typically very sparse. Debug logs on the other hand provide you with a lot of information. Once you get used to the amount of information, you will learn to identify problems. For example, a client got disconnected? The debug logs usually tell why.

{% hint style="info" %}
In the ObjectBox Browser, you can enable debug logs in the "Status" page. See [Sync Server configuration](objectbox-sync-server.md) for details.
{% endhint %}

## IDs do not match across devices

You may notice that IDs of objects stored on one device may not always match the IDs on another device. Well, that's not a bug, but a feature. :slight\_smile:  Check the [docs on Object ID mapping](advanced/object-ids.md) and the possibility to use global IDs instead.

## Other hiccups

A checklist of other likely issues:

* [ ] Do you have the latest versions running?
* [ ] Does the server have the latest version of the data model?
* [ ] Does the client version "match" the server version? This is fine most of the times, unless we announced breaking changes during a beta phase.

## Contact us

The ObjectBox team is here to help you. If you already investigated a bit (e.g. "hey, this debug log there looks odd, no?") it will help to get issues resolved quickly. In any case, do not hesitate to reach out! :heart:&#x20;
