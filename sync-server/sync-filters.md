---
description: >-
  ObjectBox Sync uses filters to enable partial syncing so that each user is
  getting only the data they need.
---

# Sync Filters

Unless you want to replicate all data to all clients, you want to use sync filters.
For each user, sync filters select the data that is synchronized to the user (client).
This enables "user-specific sync".

## Configuration

Sync filters are configured on the server side.
For each type of your data model, you can configure a filter expression (or "rule").
This is done in the Sync Server JSON configuration file (there are no CLI parameters for this for good reasons).
While it's anyway a good idea to keep the configuration file in a version control system, e.g. git, it certainly is when you add sync filters.

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

This configuration contains 3 sync filters for the types `Category`, `Person` and `Customer`.
The filter expression for `Category` references the property `name` (part of the `Category` type)
and selects only categories with the name "public" for synchronization.
Similarly, the filter expression for `Person` selects only Persons that are at least 18 years old.

The `Customer` filters on the `email` property and uses a variable called `$auth.email` as its operand.
Typically, sync filters use variables as these allow for user-specific sync.
Variables start with a `$` character.
In this case it refers to an authentication variable, which represents the Sync user's email address.

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
For example consider a `Person` type defined in your ObjectBox data model that has a `name` and `age` property.
Now, when defining a filter expression for the `Person` type, you can refer to `name` and `age` as property names.

### Operators

Filter expression can use the following operators for all value types:

| Operator | Description           | Example                |
|----------|-----------------------|------------------------|
| `==`     | Equals                | `name == "Alice"`      |
| `!=`     | Not equals            | `status != "inactive"` |
| `>`      | Greater than          | `age > 18`             |
| `<`      | Less than             | `price < 100.0`        |
| `>=`     | Greater than or equal | `score >= 80`          |
| `<=`     | Less than or equal    | `quantity <= 50`       |

For string values the following operators are additionally available:

| Operator | Description             | Example                   |
|----------|-------------------------|---------------------------|
| `==~`    | Case-insensitive equals | `name ==~ "JOHN"`         |
| `^=`     | Starts with             | `email ^= "admin"`        |
| `*=`     | Contains                | `description *= "urgent"` |
| `$=`     | Ends with               | `filename $= ".pdf"`      |

### Values (operands)

The third and last part or a filter condition, is the value or operand.
It defines the value to which the property is compared.
If it's a match, i.e. the condition is considered "true", then the object is included in the sync.

Operands can either be literals (fixed values) or variables (dynamic values).
Supported literal types are strings, integers and floating point values.
The literal type must match the property type, e.g. the `name` property can only have string values.
If there's a mismatch, an configuration error will occur when the Sync Server parses the sync filters. 

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

Literal numbers can be integers and floating point values:
```
age == 25
price >= 19.99
```

#### Variables

Variables are provided by the Sync Server to allow filtering based on user-specific data.
To refer to these variables you use a dollar sign (`$`) followed by the variable name.

```
email == $auth.email
```

Currently, the only source where variables are defined are ObjectBox Sync authenticators.
More accurately, only the JWT authenticator provides variables as of now.
Sync clients can use JWTs to authenticate with the Sync Server; see [JWT authentication](./jwt-authentication.md) for details.
If successful, the Sync Server will set the JWT's claims as variables that can be used in the filter expressions.
For example, JWTs typically have an "email" claim, which is then exposed as a variable using the "auth." prefix as "auth.email".

Let's say you want group users into teams.
Check with your JWT provider how to add custom claims to your JWTs.
Also, at the JWT provider side, assign users to teams.
Then, you can use a filter expression like `team == $auth.team` to enable group-based sync.

Note: future versions of ObjectBox Sync will have additional variables.
If the JWT-based variables 

### Logical Operators

In filter expressions, you can use the logical operators to combine conditions.

`AND` combines conditions where both must be true. AND has higher precedence than OR.

```
age >= 18 AND status == "active"
```

`OR` combines conditions where at least one must be true. OR has lower precedence than AND.

```
category == "urgent" OR priority > 5
```

#### Precedence and Grouping

Use parentheses to control the order of evaluation:

```
(age >= 18 AND age <= 65) OR status == "premium"
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

## Current limitations

Sync filters are still in beta.
They have a few known limitations that will be addressed in one of the next versions:

* When sync filter expressions changed, it's not yet handled.
  Clients may still keep old data previously synced by old filters.
  In a new version, we will likely enforce a complete sync from scratch when filters change
  so that clients have consistent data.
* It's possible to change the value of a property, which is used in a sync filter expression.
  For example, consider a property `team` that is used in a sync filter expression.
  One client changes the team from "blue" to "green".
  The server now correctly syncs the change to "team green" clients.
  However, it is not yet deleted from "team blue" clients.
* JWT claims are only the first variables available to sync filter expressions.
  We are currently collecting customer requirements to add more variables and user information.
  Check with the ObjectBox to ensure that your needs are covered.
