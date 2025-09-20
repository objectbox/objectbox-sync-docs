---
description: >-
  ObjectBox Sync uses filters to enable partial syncing so that each user gets only the data they need.
---

# Sync Filters

Unless you want to replicate all data to all clients, you want to use sync filters.
For each user, sync filters select the data that is synchronized to the user (client).
This enables "user-specific sync".

{% hint style="info" %}
Sync filters are generally available since ObjectBox 5, i.e. Sync Server version 2025-09-16.
Older clients must be updated to ObjectBox 5 to use sync filters.
{% endhint %}

## Configuration

Sync filters are configured on the server side.
For each type of your data model, you can configure a filter expression (or "rule").
This is done in the Sync Server JSON configuration file (there are no CLI parameters for this for good reasons).
While it's a good idea to keep the configuration file in a version control system, e.g., git, it's especially important when you add sync filters.

### Add filter expressions to the JSON configuration

The JSON configuration file is typically named `sync-server-config.json`.
For general details and other configuration options, please check the [configuration](configuration.md) page.

All sync filters are defined in the `syncFilters` JSON object.
Filters are defined per data type (from your ObjectBox data model) and the keys are the type names.
The value is a string and contains the filter expression.

The JSON configuration is best illustrated by an example:

```json
{
  "syncFilters": {
    "Category": "name == 'public'",
    "Person": "age >= 18",
    "Customer": "email == $auth.email"
  }
}
```

This configuration contains three sync filters for the types `Category`, `Person`, and `Customer`.
The filter expression for `Category` references the property `name` (part of the `Category` type)
and selects only categories with the name "public" for synchronization.
Similarly, the filter expression for `Person` selects only persons who are at least 18 years old.

The `Customer` filter filters on the `email` property and uses a variable called `$auth.email` as its operand.
Typically, sync filters use variables as these allow for user-specific sync.
Variables start with a `$` character.
In this case, it refers to an authentication variable, which represents the Sync user's email address.

## Filter expressions

Filter expressions provide a compact and flexible way to query and filter data in ObjectBox Sync.
They use a simple syntax that is similar to many programming languages and SQL.

A **filter expression** consists of **conditions** that can be combined using **logical operators**.
The basic structure of a condition has three parts:

```
propertyName operator value
```

Simple examples:

```
name == "John"
age > 25
```

### Property names

The first part of a filter condition is the "property name", which refers to a property (aka member/field) in your data objects (aka type defined in your ObjectBox data model).
For example, consider a `Person` type defined in your ObjectBox data model that has a `name` and `age` property.
Now, when defining a filter expression for the `Person` type, you can refer to `name` and `age` as property names.

### Operators

Filter expressions can use the following operators for all value types:

| Operator | Description           | Example                |
|----------|-----------------------|------------------------|
| `==`     | Equals                | `name == "Alice"`      |
| `!=`     | Not equals            | `status != "inactive"` |
| `>`      | Greater than          | `age > 18`             |
| `<`      | Less than             | `price < 100.0`        |
| `>=`     | Greater than or equal | `score >= 80`          |
| `<=`     | Less than or equal    | `quantity <= 50`       |

For string values, the following operators are additionally available:

| Operator | Description             | Example                   |
|----------|-------------------------|---------------------------|
| `==~`    | Case-insensitive equals | `name ==~ "JOHN"`         |
| `^=`     | Starts with             | `email ^= "admin"`        |
| `*=`     | Contains                | `description *= "urgent"` |
| `$=`     | Ends with               | `filename $= ".pdf"`      |

### Values (operands)

The third and last part of a filter condition is the value or operand.
It defines the value to which the property is compared.
If it's a match, i.e., the condition is considered "true", then the object is included in the sync.

Operands can either be literals (fixed values) or variables (dynamic values).
Supported literal types are strings, integers, and floating-point values.
The literal type must match the property type, e.g., the `name` property can only have string values.
If there's a mismatch, a configuration error will occur when the Sync Server parses the sync filters.

#### Literal values

Strings can be enclosed in either double quotes (`"`) or single quotes (`'`):

```
name == "John Doe"
title == 'Software Engineer'
```

Escape sequences are supported using backslash (`\`):

```
message == "He said \"Hello\""
path == 'C:\\Users\\John'
```

Literal numbers can be integers and floating-point values:
```
age == 25
price >= 19.99
```

#### Variables

Variables can be used in sync filter expressions.
Sync filter variables are resolved when a client logs in using client-specific values.
Thus, variables enable user-specific data sync.

Variables are referenced using a dollar sign (`$`) followed by the variable name:

```
email == $auth.email
```

If the variable name includes special characters, you use the braces syntax, e.g. `${variable}`:

```
myProperty == ${auth.https://example.com/custom-claim}
```

{% hint style="info" %}
Note that variable names do not support escape sequences, e.g. the backslash has no special meaning.
{% endhint %}

#### Auth variables

"Auth" variables are defined by ObjectBox Sync Server authenticators when a client logs in.
At this point, only the JWT authenticator provides variables.
It is used when Sync clients provide JWTs to authenticate; see [JWT authentication](./jwt-authentication.md) for details.
Once the JWT has been validated, the Sync Server sets the JWT's claims as sync variables using the "auth." prefix.
For example, JWTs typically have an "email" claim, which is then exposed as a variable named "auth.email".

Let's say you want to group users into teams.
Check with your JWT provider how to add custom claims to your JWTs.
Also, at the JWT provider side, assign users to teams.
Then, you can use a filter expression like `team == $auth.team` to enable group-based sync.

Note: future versions of ObjectBox Sync will have additional variables.
If the JWT-based variables are not sufficient for your use case, please contact ObjectBox support.

#### Client variables

ObjectBox Sync Clients can also define variables for sync filters.
Before logging in, the client API allows to add variables using key/value pairs (strings).
These are sent to the Sync Server with the login request and can be used in sync filter expressions using the `client.` prefix.

For example, assume we want to group data into teams and allow clients can freely choose a team.
Let's say a client adds a filter variable "team" with value "red" before logging in.
A filter expression `team == $client.team` would then match only objects where the `team` property is "red" for this client.

{% hint style="warning" %}
Client variables are by definition provided by clients.
Given a certain effort, an attacker could forge requests to provide arbitrary values.
The server has no way to verify the values.
Thus, avoid client variables for security- or business-critical matters.
{% endhint %}

### Logical Operators

In filter expressions, you can use the logical operators to combine conditions.

`AND` combines two conditions where both must be true. `AND` has higher precedence than `OR` (`AND` is evaluated first).

```
age >= 18 AND status == "active"
```

`OR` combines two conditions where at least one must be true. `OR` has lower precedence than `AND`.

```
category == "urgent" OR priority > 5
```

#### Precedence and Grouping

Without parentheses, `AND` has higher precedence than `OR`. 

Thus, the following two expressions are equivalent, e.g. requires the "premium" status or a combination of minimum age and score:
```
status == "premium" OR age >= 21 AND score >= 100 
```

```
status == "premium" OR (age >= 21 AND score >= 100) 
```

Use parentheses to control the order of evaluation; e.g. to (always) require a minimum score and either premium status or a minimum age:  
```
(status == "premium" OR age >= 21) AND score >= 100 
```

#### Complex Examples

Multiple conditions with different operators:

```
name ^= "John" AND age > 25 AND (status == "active" OR status == "pending")
```

String matching with case-insensitive comparison:

```
email $= "@company.com" AND department ==~ "ENGINEERING"
```

Numeric ranges and string patterns:

```
(price >= 10.0 AND price <= 100.0) AND description *= "sale"
```

## Performance

Since sync filters are used to create queries, especially when clients sync for the first time.
Thus, what makes a query performant also applies to sync filters.

Especially for equality conditions (`==`), it is highly recommended to use indexes for the properties used in the filter expressions (unless you only have a few objects of a type, e.g. less than a hundred).
This is done in the standard ObjectBox way, i.e. using the index annotation (`@Index` for most languages) on the property in the data model.

## Caveats

Sync filters have some caveats to be aware of (future versions may or may not address them):

* **Do not change values of properties used in Sync filters.** 
  If you rely on this, delete the object with the old value instead and insert a new object with the new value.
  For example, consider a property `team` that is used in a sync filter expression.
  One client changes the team from "blue" to "green".
  The server now correctly syncs the change to "team green" clients.
  However, it is not yet deleted from "team blue" clients that have synced before.
  Thus, use the delete and insert approach instead:
  the server will correctly remove the object from "team blue" clients.
* JWT claims are only the first variables available to sync filter expressions.
  We are collecting customer requirements to add more variables and user information.
  Check with the ObjectBox team to ensure that your needs are covered.
