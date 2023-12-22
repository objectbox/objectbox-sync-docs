---
description: How-to use mutations to insert data into the ObjectBox GraphQL database
---

# GraphQL Mutations

Note: The GraphQL playground can also be used for mutations.

### How to write mutations

#### Mutation name

There are mutation operations for all entity types. For each entity, the following mutations are available: put\* and delete\*, where \* signifies entity name. So for a `TestEntity`, the available mutations are `putTestEntity`,  `deleteTestEntity`.&#x20;

#### Arguments

All ObjectBox GraphQL mutations require an argument. For put operations, we indicate the types and values of objects to put, while when deleting we indicate the ids of objects to be deleted, or use the `all` flag to delete all objects. Refer to the examples below to see how these have to be formatted in each case.

#### Rerurn ID(s)

Optionally, you can use the `returning` section to make your mutation return the ID(s) of object(s) that were put or deleted.

### Examples of mutations

#### Put new or existing object

To put an object into the ObjectBox database, use `putTestEntity` for an ObjectBox entity called TestEntity, providing the object's type and value inside an `input` argument. This works both for putting new objects and updating existing ones (in the latter case an `id` must be supplied).

```
mutation putOne {
  putTestEntity(
    input: {simpleBoolean: true}
  ) {
    returning {
      id
    }
  }
}
```

#### Put multiple objects

`input` can also be an array.

```
mutation putMultiple {
  putTestEntity(
    input: [
      {simpleString: "banana"}, 
      {simpleString: "orange"}, 
      {simpleString: "banana"}
      ]) {
    returning {
      id
    }
  }
}
```

#### Delete

Supply an array of IDs to be deleted.

```
mutation deleteById {
    deleteTestEntity(ids: [1, 3, 4, 42]) {
        id
    }
}
```

#### Delete all

To delete all objects, set the `all` argument to `true`.

```
mutation deleteAll {
    deleteTestEntity(all: true) {
        id
    }
}
```

####
