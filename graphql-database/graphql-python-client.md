---
description: Client access to the ObjectBox GraphQL database server
---

# GraphQL Python Client

### Install the client

Install a GraphQL client like "python-graphql-client":

```
pip install python-graphql-client
```

### Run the ObjectBox server

Your ObjectBox Sync Server also comes with a native GraphQL server, making ObjectBox a GraphQL database that clients  can query.

Note that the port used for GraphQL is different than the one used for Sync.

### Get the session ID

In order to make GraphQL requests, you must first obtain a session ID.

Make an empty plain HTTP POST request to `/api/v2/sessions` in order to receive a session ID. E.g. using the [requests](https://pypi.org/project/requests/) library:

```
import requests

url = 'http://localhost:8081/api/v2/sessions'

print(requests.post(url).text)
```

### GraphQL requests

Now everything is ready for you to do the GraphQL requests. Note that the session ID you found in the previous step must be passed to all GraphQL requests. You can provide it via e.g. using argparse. It's passed via the standard `Authorization` header (see example below).

Here is a simple example of using the client to read all existing objects from the database.

```
from python_graphql_client import GraphqlClient
import requests

url = 'http://localhost:8081/api/v2/sessions'
token = requests.post(url).text
header = {
    'Authorization': 'Bearer ' + token[1:-1]
}

client = GraphqlClient(endpoint="http://localhost:8081/api/graphql", headers = header)

# Read existing objects
read = """
query getAll {
  testEntity {
    id
    simpleInt
    simpleString
  }
}
"""

# Synchronous request
data = client.execute(query=put)
print(data)
```

