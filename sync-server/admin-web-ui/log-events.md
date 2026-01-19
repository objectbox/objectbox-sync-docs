---
description: >-
  View important server-side events in the ObjectBox Admin web interface.
---

# Log Events

The **Log Events** page in the ObjectBox Admin web interface displays server-side log events, providing visibility into server operations, warnings, and errors.

![objectbox-admin-log-events.png](../../.gitbook/assets/objectbox-admin-log-events.png)

## Overview

Log events are stored persistently on the server and can be browsed through the Admin UI. Events are displayed in reverse chronological order (newest first) and include detailed information about server activity.

## Event Types

Each log event has a type indicating its severity:

| Type          | Description                                            |
|---------------|--------------------------------------------------------|
| **Debug**     | Diagnostic information useful for debugging            |
| **Info**      | General informational messages about normal operations |
| **Important** | Significant operational events worth noting            |
| **Warning**   | Potential issues that don't prevent operation          |
| **Error**     | Problems that affected an operation                    |
| **Crash**     | Critical failures                                      |

Events are color-coded in the UI for quick identification.

## Event Fields

Each log event contains the following information:

| Field              | Description                                                                               |
|--------------------|-------------------------------------------------------------------------------------------|
| **Timestamp**      | When the event occurred (nanosecond precision). Click to see full details including UUID. |
| **Type**           | Severity level of the event                                                               |
| **Message**        | Description of the event. Click to view the full message.                                 |
| **Component**      | The server component that generated the event                                             |
| **Peer ID**        | Identifier of the connected peer (if applicable)                                          |
| **Thread**         | Thread ID where the event occurred                                                        |
| **Subject**        | Additional context about what the event relates to                                        |
| **Stacktrace**     | Call stack at the time of the event (typically for errors)                                |
| **Parent ID**      | Reference to a related parent event                                                       |
| **Client ID**      | Client peer identifier (if applicable)                                                    |
| **Extra**          | Additional key-value pairs with context-specific information                              |
| **Server Version** | ObjectBox server version that generated the event                                         |

## Navigation

### Pagination

- **Newer** - Navigate to more recent events
- **Older** - Navigate to older events
- **Events per page** - Select how many events to display (10, 15, 20, 50, or 100)

### Jump to Date/Time

Click the calendar icon to open a date/time picker and jump directly to events from a specific point in time. This is useful for investigating issues that occurred at a known time.

### Refresh

Click the refresh button to reload the current view with the latest events.

## Viewing Details

Several fields may contain more information than can be displayed in the table:

- **Message** - Click to open a dialog with the full message text and a copy button
- **Stacktrace** - Click "View" to see the full stack trace with copy functionality
- **Parent ID** - Click "View" to see the parent event UUID
- **Client ID** - Click "View" to see the full client peer identifier
- **Extra** - Click "View" to see all additional key-value pairs in a table

## Downloading Events

Below the event table, a **Download** link allows you to download the currently displayed events as a JSON file.
The filename includes context about which events are included (e.g., `objectbox-events-from-<uuid>.json`).

## Tips

- Use the date/time picker to quickly navigate to events around a known incident time
- Check the **Extra** field for additional context that may help diagnose issues
- Stack traces are particularly useful for understanding error conditions
- The **Component** field helps identify which part of the server generated an event
- Events with the same **Parent ID** are related and can be traced together
