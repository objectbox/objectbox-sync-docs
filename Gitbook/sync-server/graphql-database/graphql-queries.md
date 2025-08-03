---
description: How to use queries to get data from the ObjectBox GraphQL database
---

# GraphQL Queries

### Query Name

The name of a GraphQL query is similar but not equal to the corresponding database entity type:

* for ObjectBox entities starting from a capital letter (e.g. TestEntity), the GraphQL query name has the first character in lowercase (testEntity);
* for ObjectBox entities starting form a lowercase letter, the GraphQL query is called `query_typeName` (so, e.g. the query for testEntity is `query_testEntity`).

### Query arguments

#### Simple query all

Get all objects of a given type by querying without any arguments.

```
query getAll {
  testEntity {
    id
  }
}
```

#### Query by ID

To select specific objects, you can query by ID(s) by simply supplying an array to the `ids` argument.

```
query getById {
  testEntity(ids: [1,2]) {
    id
    simpleString
    simpleInt
  }
}
```

#### Filters

Use filters to query with more complicated query conditions. The query will only return objects matching all given conditions. Note that querying by ID is significantly more efficient, so prefer to use that if the local object IDs are known (e.g. from previous queries).

Example using a filter to find all objects with a simpleString property equlal to `banana`.

```
query getByString {
  testEntity(filter: {simpleString: {eq: "banana"}}) {
    id
    simpleShort
    simpleByte
  }
}
```

**Query Conditions for different property types**&#x20;

Each property type has its own set of query conditions. These are listed in the box below.

{% tabs %}
{% tab title="Bool" %}
Properties of type `Bool` only have one query condition:

* `eq`: equals a given bool value (true or false)
{% endtab %}

{% tab title="Int, Int64 & Date" %}
The following query conditions apply to properties of type `Int`, `Int64` and `Date` (`simpleByte`, `simpleShort` and `simpleInt`, `simpleLong`, `simpleDate`):

* `eq`- short for "equal to". Filters objects by a property value that must be equal to the given value.
* `neq`- short for "not equal to". Filters objects by a property value that must be different from the given value.
* `lt`- short for "less than". Filters objects by a property value that must be less than the given value.
* `lte` - short for "less than or equal to". Filters objects by a property value that must be less than or equal to the given value.
* `gt` - filters objects by a property value that must be greater than the given value.
* `gte` - filters objects by a property value that must be greater than or equal to the given value.
{% endtab %}

{% tab title="String" %}
Property of type `String`  has all query conditions of `Int` and these in addition:

* `contains` - filters objects by a property value that must contain the given value (substring).
* `startsWith` - filters objects by a property value that must start with the given value (substring).
* `endsWith` - filters objects by a property value that must end with the given value (substring).
{% endtab %}
{% endtabs %}

#### Pagination

Pagination is supported via `offset` and `first` arguments.

* `offset` - return objects starting at the given offset (0-based, e.g. 1 will skip the first object and start at the second).
* `first` - return only the first n objects (limits the number of returned objects).

```
query get {
 testEntity(first: 2, offset: 3)  { id }
}
```

